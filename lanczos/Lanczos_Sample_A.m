%This is a sample code to run LANCZOS Algorithm and find out the minimum
%eigen value of a real symmetric matrix A.
clear
clc
format long
    N=800 ;
    %A=Problem.A;
    A = rand(N,N) ;     % A is a random square matrix
    A=0.5*(A+A') ;          % This steps makes A, a symmetric matrix
    vkm1 = rand(N,1) ;    % Arbitrary initial guess for LANCZOS vector
    vkm1 = vkm1/norm(vkm1); % Normalize it, this is q1 in the algorithm
    vk = A*vkm1 ;           % The first v is A*q (from algorithm)
    a(1) = vkm1'*vk ;       % alpha=q'*v
    
    vk = vk - a(1)*vkm1 ;   %update v=v-beta0*q0-alpha1*q1 (beta0, q0 = 0)
    b(1) = norm(vk) ;       %beta=b=norm(vk), from algorithm
    vk = vk/b(1) ;          %update vk as new qi (to be used in next iteration) by normalizing
    
    k=1;
    L(1,1)=0;
    DL=1;
    
    while DL > 0.001        %run iterations until eigen values converge i.e difference between eigen values from subsequent iterations is less than the specified tolerance (here 0.001)
        
        vkp1 = A*vk ;
        x(k)=max(vkp1);
        a(k+1) = transpose(vk)*vkp1  ;
        vkp1 = vkp1 - a(k+1)*vk - b(k)*vkm1 ; %same as vk=A*vk-a(k+1)*vk-b(k)*vkm1;
        y(k)=max(vkp1);
        vkm1 = vk ;               %this will be q(n-1) for next iteration
        z(k)=max(vkm1);
        b(k+1) = norm(vkp1) ;  %=norm(of current iteration's updated vk)
        vk = vkp1/b(k+1) ;
    %the above set of iterations find out a(i), b(i) which are the diagonal
    %and off diagonal terms of the tridiagonal matrix T (which is
    %equivalent to A, and has the same eigen values/vectors of A)
    %aij=qi'Aqj. In Lanczos method, we do not have to arrive at the entire
    %T, to find the eigens. Even part of T will give approximate eigens. In
    %this "while" loop, at every iteration, the size of T keeps increasing
    %and the eigen values are evaluated. This is done until we get
    %converging eigen values.
    
    %J will be T, if the iterations rum until full matrix
    %tridiagonalization, i.e for N iterations.
    s=length(b);
    J = diag(a) + diag(b(1:s-1),1) + diag(b(1:s-1),-1) ;
    %[Evec,Eval] = eig(J) ;
    L(1,k+1)=eigs(J,1,'sa');
    DL(k)=abs(L(1,k+1)-L(1,k));
    k=k+1;
end;
sl=length(L)
L(sl)
dl=length(DL);
DL(dl)