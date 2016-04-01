import os
import numpy as np

def Matvec(vector):
    
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
#Run perturb1 to get dumpforce of data787
#############################################
os.system("lmp_serial -in in.perturb")

#############################################
#Read and sort dumpforce
#############################################

dataRead = open("dump.forces","r")
w = open("sorted_dumpforce", 'w')
## atomes type 1
list1 = []-
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
#Runllammps with modi.atoms
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
w = open("Vo",'w')

listx = []
listy = []
listz = []
for i in range(840):
    listx.append((float(data1.readline())-float(data2.readline()))*0.01)
for i in range(840):
    listy.append((float(data1.readline())-float(data2.readline()))*0.01)
for i in range(840):
    listz.append((float(data1.readline())-float(data2.readline()))*0.01)

for i in range(840):
    w.write(str(1+i) + '\t' + str(listx[i]) + '\t' + str(listy[i]) + '\t' + str(listz[i]) + '\n')

data1.close()
data2.close()
w.close
