% The following function minimizes lammps for a small perturbation (vk)
% about an equilibrium configuration (step) and gives the forces at the 0th
% step, i.e it gives the forces generated due to the perturbation on an
% atom data file corresponding to "step"


function F=Min_Lammps_Perturb(Nfix,N,step)                ######## Nfix:

%------convert vk from3Nx1 to Nx3-----
%---this is the perturbance to be added to the atoms----
vchainx(:,1) = rand(N,1);   %will give an Nx1 vector
vchainy(:,1) = rand(N,1);   %will give an Nx1 vector
vchainz(:,1) = rand(N,1);   %will give an Nx1 vector


%----read the atoms data file, separate text and data-------
fname=sprintf('data.%d',step);
fid1=fopen(fname,'r');
C_text = textscan(fid1,'%s',17,'delimiter','\n');                        -----------Useless, skip the first 17 lines
C_atom = textscan(fid1,'%d %d %f %f %f %f %f %f',(N+Nfix),'delimiter','\n');   ------------- store data from 1 to 4000 in the file c_atom
fclose(fid1);


------------------------------------------------------------------------------------------------------------------------------------------
%----store the text and data from cells to matrices----
D_text(1:17,1)=C_text{1,1}(1:17,1);
D_atom1=C_atom{1,1}(1:(N+Nfix));   %atom ID, column vector, Nx1
D_atom2=C_atom{1,2};   %atom type (Nfix atoms are type 2)
indarry1=D_atom2(:,1)==1;     %Nx1,has 1's where ever atom type is 1 and 0 otherwise
indarry2=D_atom2(:,1)==2;     %Nx1,has 1's where ever atom type is 2 and 0 otherwise, indarry2 is equivalent to (~indarry1)
D_atom1_1=D_atom1(indarry1);
D_atom1_2=D_atom1(indarry2);
D_atom2_1=D_atom2(indarry1);
D_atom2_2=D_atom2(indarry2);
D_atom3i=C_atom{1,3};   %atom x-coordinate, Nx1
D_atom3_1=D_atom3i(indarry1); %(N+Nfix)x1 col vector, only has atom type 1 rows
D_atom3_2=D_atom3i(indarry2); %(Nfix)x1 col vector, only has atom type 2 rows
D_atom4i=C_atom{1,4};   %atom y-coordinate
D_atom4_1=D_atom4i(indarry1);
D_atom4_2=D_atom4i(indarry2);
D_atom5i=C_atom{1,5};   %atom z-coordinate (should be zero for 2D)
D_atom5_1=D_atom5i(indarry1);
D_atom5_2=D_atom5i(indarry2);
D_atom6i=C_atom{1,6};
D_atom6_1=D_atom6i(indarry1);
D_atom6_2=D_atom6i(indarry2);
D_atom7i=C_atom{1,7};
D_atom7_1=D_atom7i(indarry1);
D_atom7_2=D_atom7i(indarry2);
D_atom8i=C_atom{1,8};
D_atom8_1=D_atom8i(indarry1);
D_atom8_2=D_atom8i(indarry2);
D_Atype2=[double(D_atom1_2),double(D_atom2_2),D_atom3_2,D_atom4_2,D_atom5_2,D_atom6_2,D_atom7_2,D_atom8_2]; %(Nfix)x5 matrix or table, type 2 atoms
D_Atype1=[double(D_atom1_1),double(D_atom2_1),D_atom3_1,D_atom4_1,D_atom5_1,D_atom6_1,D_atom7_1,D_atom8_1]; %(N+Nfix)x5 matrix or table, type 1 atoms
D_Atype1=sortrows(D_Atype1); %The atom IDs will be arranged in the ascending order similar to the atoms positions file
D_Atype2=sortrows(D_Atype2);
[nrows,ncols]= size(D_atom1);
[ntext,col]=size(D_text);
D_atom=[D_Atype2;D_Atype1]; %(N+Nfix)x5 array, first 120 are fixed atoms
-------------------------------------------------------------------------------------------------------------------------------------------This section sorts atoms type, 2 first then 1

%----Add the pertubance to the (mobile) atom positions---
%---this is equivalent to checking the stability of the equilibrium of the atom positions----
D_atom1=      int32(D_atom(:,1));   %convert the atom IDs back to integers
D_atom2=      int32(D_atom(:,2));   %atom IDs
D_atom3(1:Nfix,1)=    D_atom(1:Nfix,3);
D_atom3(Nfix+1:(N+Nfix),1)=  D_atom(Nfix+1:(N+Nfix),3)+vchainx; %no perturbance applied to the first Nfix atoms at the bottom of the domain
D_atom4(1:Nfix,1)=    D_atom(1:Nfix,4);
D_atom4(Nfix+1:N+Nfix,1)=  D_atom(Nfix+1:N+Nfix,4)+vchainy; %no perturbance applied to the first Nfix atoms at the bottom of the domain
D_atom5(1:Nfix,1)=            D_atom(1:Nfix,5);  %no perturbance
D_atom5(Nfix+1:N+Nfix,1)=  D_atom(Nfix+1:N+Nfix,5)+vchainz;
D_atom6=            D_atom(:,6);
D_atom7=            D_atom(:,7);
D_atom8=            D_atom(:,8);
%---write the text and data to a new file, which will be input to LAMMPS------
fid2=fopen('modi.atoms','w');  %"modi"=> modifed, this file subjects the atoms in equilibrium, to a perturbance vk. Run Lammps to find out the instantaneous forces produced on atoms due to this perturbance.
for tex=1:ntext
    fprintf(fid2,'%s\n',D_text{tex});
end
for row=1:nrows
    fprintf(fid2, '%d %d %.15f %.15f %.15f %f %f %f\n', D_atom1(row),D_atom2(row),D_atom3(row),D_atom4(row),D_atom5(row),D_atom6(row),D_atom7(row),D_atom8(row));
end
fclose(fid2);

%---Read forces at 0th step from dump.forces------
F=Force_Vector_0th(N+Nfix); % F(2Nx1), forces on mobile atoms
end
