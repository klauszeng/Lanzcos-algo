%return the forces on atoms as F (2*Nx1) by reading the dump.forces file
%gives the forces at first timestep/iteration in the dump file
%i.e this function reads the first (Nt+9) lines of dump.forces
function F=Force_Vector_0th(Nt)
%----read the dump forces file, separate text and data-------
fid1=fopen('dump.forces','r'); %the input file here is the output of a nanoindentation minimization process run for several steps before dislocation
F_text = textscan(fid1,'%s',9,'delimiter','\n');
F_atom = textscan(fid1,'%d %d %f %f %f',Nt,'delimiter','\n');
fclose(fid1);
%----store the text and data from cells to matrices----
Ft_text(1:9,1)=F_text{1,1}(1:9,1);

F_atom1=F_atom{1,1};   %atom ID, column vector, Nx1
F_atom2=F_atom{1,2};   %atom type (Nfix atoms are type 2)
indarry1=F_atom2(:,1)==1;     %Nx1,has 1's where ever atom type is 1 and 0 otherwise
indarry2=F_atom2(:,1)==2;     %Nx1,has 1's where ever atom type is 2 and 0 otherwise, indarry2 is equivalent to (~indarry1)
F_atom1_1=F_atom1(indarry1);
F_atom1_2=F_atom1(indarry2);
F_atom2_1=F_atom2(indarry1);
F_atom2_2=F_atom2(indarry2);
F_atom3i=F_atom{1,3};   %atom x-force, Nx1
F_atom3_1=F_atom3i(indarry1);
F_atom3_2=F_atom3i(indarry2);
F_atom4i=F_atom{1,4};   %atom y-force, Nx1
F_atom4_1=F_atom4i(indarry1);
F_atom4_2=F_atom4i(indarry2);
F_atom5i=F_atom{1,5};   %atom z-force (should be zero for 2D)
F_atom5_1=F_atom5i(indarry1);
F_atom5_2=F_atom5i(indarry2);
F_Atype2=[double(F_atom1_2),double(F_atom2_2),F_atom3_2,F_atom4_2,F_atom5_2]; %(Nfix)x5 matrix or table, type 2 atoms
F_Atype1=[double(F_atom1_1),double(F_atom2_1),F_atom3_1,F_atom4_1,F_atom5_1]; %(N+Nfix)x5 matrix or table, type 1 atoms
F_Atype1=sortrows(F_Atype1); %The atom IDs will be arranged in the ascending order similar to the atoms positions file
F_Atype2=sortrows(F_Atype2);
Fo_atom=[F_Atype2;F_Atype1]; %(N+Nfix)x5 array, first Nfix are fixed atoms
Nfix=length(F_Atype2); %no. of fixed atoms
N=length(F_Atype1); %no. of free to move atoms
%--------------Build the 2Nx1 force vector (F)------------       
F(1:3:3*N,1)=Fo_atom(Nfix+1:N+Nfix,3); %x-component, the first Nfix fixed atoms are not considered, as they are force zero
F(2:3:3*N,1)=Fo_atom(Nfix+1:N+Nfix,4); %y-component
F(3:3:3*N,1)=Fo_atom(Nfix+1:N+Nfix,5); %z-component
end