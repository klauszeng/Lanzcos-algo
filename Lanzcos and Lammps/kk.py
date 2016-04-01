
import os
import numpy as np
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
xlist = []
ylist = []
zlist = []
for i in range(len(vk)):
    if i < 840:
        xlist.append(float(vk[i])*0.01)
    elif i < 1680 and i >= 840:
        ylist.append(float(vk[i])*0.01)
    else:
        zlist.append(float(vk[i])*0.01)
        
##addition
for i in range(840):
    dataList[i][2] = np.add(dataList[i][2], xlist[i])
    dataList[i][3] = np.add(dataList[i][3], ylist[i])
    dataList[i][4] = np.add(dataList[i][4], zlist[i])

#Execute write 
for i in range(840):
    modiAtoms2.write(str(dataList[i][0]) + '\t' + str(dataList[i][1]) + '\t' + str(dataList[i][2]) + '\t' + str(dataList[i][3])
                    + '\t' + str(dataList[i][4]) + '\t' + str(dataList[i][5]) + '\t' + str(dataList[i][6]) + '\t' + str(dataList[i][7])+ '\n')

dataRead.close()
modiAtoms1.close()
modiAtoms2.close()
