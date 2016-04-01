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
