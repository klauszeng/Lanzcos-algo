import matplotlib.pyplot as plt


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
