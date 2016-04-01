import numpy as np
import matplotlib.pyplot as plt

def Matvec(inputVector, A):
##    size = len(inputVector)
    vec = np.dot(A,inputVector)
##    I = np.zeros(shape=(size,size))
##    for i in range(0,size):
##        I[i][i] = 1
##    print(I)
    return vec

def lanczos_algoA(A):
    print("this is original version")
    N = len(A)
    vkml = A[0]
    vkml = np.ones((N,1))
    vkml = np.divide(vkml,np.linalg.norm(vkml)) ##  Matrix normalization and division 
    vk = np.dot(A,vkml)  # dot product
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
        vkpl = np.dot(A,vk)
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


def lanczos_algo(A):
    N = len(A)
    vkml = A[0]
    vkml = np.ones((N,1))
    vkml = np.divide(vkml,np.linalg.norm(vkml)) ##  Matrix normalization and division 
##    vk = np.dot(A,vkml)  # dot product
    vk = Matvec(vkml,A)
    print("I am using Matvec")
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
        vkpl = Matvec(vk,A)
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
    


