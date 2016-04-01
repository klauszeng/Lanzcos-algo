import os
import numpy as np
from updatePosition import updatePosition
from dumpForceSort import dumpForceSort 

def MatvecLammps(vk, filename):
    updatePosition(vk, filename)


    #############################################
    #Run perturb1 to get dumpforce of modi.atoms1
    #Run perturb2 to get dumpforce of modi.atoms2
    #############################################

    os.system("lmp_serial -in in.perturb")##this gives f(x+0.01Vk)
    os.system("lmp_serial -in in.perturb1") ##this gives f(x)


    ##fx
    pos1 = dumpForceSort("dump.forces")  #not change
    pos2 = dumpForceSort("dump1.forces")
    ##subtrac
    Vo = np.subtract(pos1, pos2)/ 0.0001

    return Vo
