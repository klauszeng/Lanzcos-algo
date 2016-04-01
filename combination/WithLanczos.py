import numpy as np
import matplotlib.pyplot as plt
import os

def Matvec(inputVector):
    ############################################
    #Read data.787 and get vectors also update postion
    ############################################
    filename = "data.787" 
    dataRead = open(filename,'r')
    w = open("modi.atoms","w")
    vk = np.random.rand(840,3) * 0.01
    for i in range(22):
        w.write(dataRead.readline())
    xa=[]
    num = []
    for i in range(840):
        contents = dataRead.readline().split()
        xa.append([float(contents[2]),float(contents[3]),float(contents[4])])
        num.append([contents[0], contents[1]])
    matrix = np.add(vk,xa)
    for i in range(len(matrix)):
        execute = num[i][0]+ ' ' + num[i][1] + ' ' + str(matrix[i][0]) + ' ' + str(matrix[i][1]) + ' ' + str(matrix[i][2]) + '\n'
        w.write(execute)
    dataRead.close()
    w.close()
    #############################################
    #Run perturb1 to get dumpforce of data3207
    #############################################
    os.system("lmp_serial -in in.perturb")
    #############################################
    #Read and sort dumpforce
    #############################################
    dataRead = open("dump.forces","r")
    w = open("sorted_dumpforce", 'w')
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
            list1.append([float(contents[0]),contents[2],contents[3],contents[4]])
        elif contents[1] == '2':
            list2.append([float(contents[0]),contents[2],contents[3],contents[4]])
        else:
            break
    ##sort list 
    list1.sort(key=lambda x:x[0])
    list2.sort(key=lambda x:x[0])
    ##creat list associate with x,y,z
    list1x=[]
    list1y=[]
    list1z=[]
    list2x=[]
    list2y=[]
    list2z=[]
    for element in list1:
        list1x.append( element[1])
        list1y.append( element[2])
        list1z.append( element[3])
    for element in list2:
        list2x.append( element[1])
        list2y.append( element[2])
        list2z.append( element[3])
    outputlist = list2x +list1x +list2y + list1y + list2z+ list1z
    ##write data in the target file
    for thing in outputlist:
        w.write(thing + '\n')
    dataRead.close()
    w.close()
    #############################################
    #Runlammps with modi.atoms
    #############################################
    os.system("lmp_serial -in in.perturb1")
    #############################################
    #Read and sort dumpforce
    #############################################
    dataRead = open("dump.forces","r")
    w = open("sorted_dumpforce1", 'w')
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
            list1.append([float(contents[0]),contents[2],contents[3],contents[4]])
        elif contents[1] == '2':
            list2.append([float(contents[0]),contents[2],contents[3],contents[4]])
        else:
            break
    ##sort list 
    list1.sort(key=lambda x:x[0])
    list2.sort(key=lambda x:x[0])
    ##creat list associate with x,y,z
    list1x=[]
    list1y=[]
    list1z=[]
    list2x=[]
    list2y=[]
    list2z=[]
    for element in list1:
        list1x.append( element[1])
        list1y.append( element[2])
        list1z.append( element[3])
    for element in list2:
        list2x.append( element[1])
        list2y.append( element[2])
        list2z.append( element[3])
    outputlist = list2x +list1x +list2y + list1y + list2z+ list1z
    ##write data in the target file
    for thing in outputlist:
        w.write(thing + '\n')
    dataRead.close()
    w.close()
    ###############################################
    ###subtract
    ###############################################
    data1 = open("sorted_dumpforce1",'r')
    data2 = open("sorted_dumpforce",'r')
    
    listx = []
    listy = []
    listz = []
    for i in range(840):
        listx.append((float(data1.readline())-float(data2.readline()))*0.01)
    for i in range(840):
        listy.append((float(data1.readline())-float(data2.readline()))*0.01)
    for i in range(840):
        listz.append((float(data1.readline())-float(data2.readline()))*0.01)
        
    vec = []
    for i in range(840):
        vec .append([float(listx[i]),float(listy[i]),float(listz[i])])


    data1.close()
    data2.close()
    return vec
    
def lanczos_algo(N):
    vkml = np.random.rand(N,1)
    vkml = np.divide(vkml,np.linalg.norm(vkml)) ##  Matrix normalization and division 
    vk = Matvec(vkml)

    a = np.dot(np.transpose(vkml),vk)
    alist =[]
    alist.append(float(a))

    vk = np.subtract(vk,alist[0] * vkml)  # matrix subtraction
    b = np.linalg.norm(vk)
    blist = []
    blist.append(float(b))
    vk = np.divide(vk,blist[0])

    k = 1
    DL =1
    DLlist = []
    Llist = []
    Llist.append(0)

    while DL > 0.00001:
##        vkpl = np.dot(A,vk)
        vkpl = Matvec(vk)
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


    plt.plot(DLlist[1:])
    plt.ylabel('DL')
    plt.show()
    return (Llist[k-1], DL, k-1)
    
    


