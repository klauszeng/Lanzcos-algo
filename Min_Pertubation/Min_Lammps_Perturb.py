## Min_Lammps_Perturb
import numpy as np
import os

def OMG(Nfix,N,step):

    ## This is the perturbance to be added to the atoms ---
    vchainx = np.random.rand(N,1)
    vchainy = np.random.rand(N,1)
    vchainz = np.random.rand(N,1)
    print(vchainx)
    ##read the atoms data file, separate text and data
    filename = "data." + str(step)
    f = open(filename,'r')
    i = 0
    
    ##file that holds for output
    w = open('modi.atoms.txt','w')
    
    ##extracting the first 17 lines
    while i < 17:
        line = f.readline()
        w.write(line)  ## transport lines
        i+=1

    

    ls = []
    ##extracting the rest lines as well as sumation xyz
    x=1
    
    for  i in range(0,4000):
        line = f.readline()
        sline = line.split()
        

        ## if state to distinguish atoms type. If 2, write to the file directly. If 1, store first then write after loop
        if int(sline[1]) == 2:
            w.write(' '.join(sline)+'\n')
            
        else:
            ## adding vchain x
            sline[2] = str(float(sline[2]) + float(vchainx[x-1]))
            ## adding vchain y
            sline[3] = str(float(sline[3]) + float(vchainy[x-1]))
            ## adding vchain z
            sline[4] = str(float(sline[4]) + float(vchainz[x-1]))
            
            ls.append(sline)

    for line in ls:
        w.write(' '.join(line)+'\n')
    
        
    f.close()
    w.close()
