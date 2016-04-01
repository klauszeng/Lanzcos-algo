import os
import numpy as np
import matplotlib.pyplot as plt



def MatvecLammps(vk):
    ############################################
    #Read data.787 and get vectors also update postion
    #input: data.787
    #output: modi.atoms
    ############################################
    filename = "data.787"   
    dataRead = open(filename,'r')   
    modiAtoms1 = open("modi.atoms1","w")#this file stores Xa
    modiAtoms2 = open("modi.atoms2","w")#this file updates Xa by adding 0.01 x Vk
                                            ##    vk = np.random.rand(840,3) * 0.01
    #Copy the first 22 lines as they are
    for i in range(22):
        copy = dataRead.readline()
        modiAtoms1.write(copy)
        modiAtoms2.write(copy)
    ################################################
    ## This step copy all lines from file to dataList and sort by the index
    ################################################
    

    #extract data from the file to dataList and performed sort
    dataList = []
    
    for i in range(840):
        contents = dataRead.readline().split()
        ##content[0] is index, content[1] is atom type, content[3] = x, content[4] = y, content[5] = z, 
        dataList.append([int(contents[0]),contents[1], float(contents[2]),float( contents[3]), float(contents[4]), contents[5], contents[6], contents[7]])

    #Sort the list with Lambda function
    dataList.sort(key=lambda x:x[0])

    #################################################
    ## this step copys everything in the dataList into modi.atoms1 for lammps (no changes)
    #################################################
     #Execute write 
    for i in range(840):
        modiAtoms1.write(str(dataList[i][0]) + '\t' + str(dataList[i][1]) + '\t' + str(dataList[i][2]) + '\t' + str(dataList[i][3])
                        + '\t' + str(dataList[i][4]) + '\t' + str(dataList[i][5]) + '\t' + str(dataList[i][6]) + '\t' + str(dataList[i][7])+ '\n')

    #################################################
    ## this step performs addition first then write everything into modi.atoms2 (changes)
    ## and convert vk to the form 840 by 3
    #################################################
    #Execute write
    j = 0
    for i in range(840):
        if (dataList[i][1] == "1"):
            modiAtoms2.write(str(dataList[i][0]) + '\t' + str(dataList[i][1])
                            + '\t' + str((dataList[i][2] + vk[j] * 0.0001)[0])# x
                            + '\t' + str((dataList[i][3] + vk[720+j] * 0.0001)[0])#y
                            + '\t' + str(dataList[i][4]) + '\t' + str(dataList[i][5])
                            + '\t' + str(dataList[i][6]) + '\t' + str(dataList[i][7])+ '\n')
            j += 1
        else:
            modiAtoms2.write(str(dataList[i][0]) + '\t' + str(dataList[i][1])
                            + '\t' + str(dataList[i][2]) + '\t' + str(dataList[i][3])## x and y
                            + '\t' + str(dataList[i][4]) + '\t' + str(dataList[i][5])
                            + '\t' + str(dataList[i][6]) + '\t' + str(dataList[i][7])+ '\n')

    dataRead.close()
    modiAtoms1.close()
    modiAtoms2.close()
    
    #############################################
    #Run perturb1 to get dumpforce of modi.atoms1
    #Run perturb2 to get dumpforce of modi.atoms2
    #############################################
    
    os.system("lmp_serial -in in.perturb1")##this gives f(x+0.01Vk)
    print('1')
    os.system("lmp_serial -in in.perturb") ##this gives f(x)


    ##fx
    pos1 = dumpForceSort("dump.forces")  #not change
    pos2 = dumpForceSort("dump1.forces")
    ##subtrac
    Vo = np.subtract(pos1, pos2)/ 0.0001

    
    return Vo


def dumpForceSort(filename):
    dataRead = open(filename, "r")

    ## atomes type 1
    list1 = []
    
    ## atomes type 2
    list2 = []

    ##get rid of the first 9 lines
    for i in range(9):
        dataRead.readline()
        
    for line in dataRead.readlines():
        contents =  line.split()
        if contents[1] == '1':
            list1.append([float(contents[0]),contents[2], contents[3], contents[4]])
        elif contents[1] == '2':
            list2.append([float(contents[0]),contents[2], contents[3], contents[4]])
        else:
            break

    ##Sort
    list1.sort(key=lambda x:x[0])
    list2.sort(key=lambda x:x[0])
    ##creat list associate with x, y, z
    list1x=[]
    list1y=[]
    list1z=[]
    list2x=[]
    list2y=[]
    list2z=[]
    for element in list1:
        list1x.append( [float(element[1])])
        list1y.append( [float(element[2])])
        list1z.append( [float(element[3])])
    for element in list2:
        list2x.append( [float(element[1])])
        list2y.append( [float(element[2])])
        list2z.append( [float(element[3])])
        
##    outputlist = list2x +list1x +list2y + list1y + list2z+ list1z
    outputlist = list1x + list1y
##                         + list1z
    
    dataRead.close()
    return outputlist

###### work on this part
def lanczos_algo(N):
##    vkml = np.ones((N, 1))
    vkml = np.random.rand(N,1)
    vkml = np.divide(vkml, np.linalg.norm(vkml))
    vk = MatvecLammps(vkml)

    a = np.dot(np.transpose(vkml),vk)
    alist =[]
    alist.append(float(a))

    vk = np.subtract(vk, alist[0] * vkml) 
    b = np.linalg.norm(vk)
    blist = []
    blist.append(float(b))
    vk = np.divide(vk,blist[0])

    k = 1
    DL =1
    DLlist = []
    Llist = []
    Llist.append(0)

    while DL > 0.001:
 
            
##        vkpl = np.dot(A,vk)
        vkpl = MatvecLammps(vk)
        #x = vkpl.max()   ## matrix max   what for?
        a = np.dot(np.transpose(vk),vkpl)  #transpose # 4x4 matrix
        alist.append(float(a))

        addit = np.add(np.dot(alist[k],vk),np.dot(blist[k-1],vkml))
        vkpl = np.subtract(vkpl,addit)

        #y = vkpl.max()# may want to make a list

        vkml = vk
       # z = vkml.max()
        b = np.linalg.norm(vkpl)
        blist.append(float(b))
        vk = np.divide(vkpl,blist[k]) 
        
        s = len(blist)

        blist1 = np.diag(blist[0:s-1],1)
        blist_1 = np.diag(blist[0:s-1],-1)
        diaga = np.diag(alist)
        J = np.add(diaga,np.add(blist1,blist_1))
        w,v = np.linalg.eig(J)
        Llist.append(w.min())
        DL = abs (Llist[k] - Llist[k-1])
        DLlist.append(DL)
        k = k+ 1
##        print(w.min())

    #############################################
    #Get rid of dump forces files 
    #############################################
##    os.system("DEL log.lammps")
##    os.system("DEL modi.atoms1")
##    os.system("DEL modi.atoms2")
##    os.system("DEL dump.forces")
##    os.system("DEL dump1.forces")
    plt.plot(DLlist[1:])
    plt.ylabel('DL')
    plt.show()

    print(Llist[k-1])
    return (Llist[k-1], DL, k-1)
    
    
