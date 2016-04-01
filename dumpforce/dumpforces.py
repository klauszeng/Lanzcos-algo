#dump.forces
import os

#check fille existance
filename = input("Please enter the filename you want to extract data including the extension.")


[name,extension] = [filename.split('.')[0],'.'+filename.split('.')[1]]

timestep = input("Please type the timestep you want.")
#line search     #The first 9 lines are just some basic info, skip to the data body
lineindex = int(timestep)*849 +10
#open the file
f = open(filename,'r')
#create a file that nsamed like input file + the timestep
w = open(name+'_'+str(timestep)+'data'+extension,'w')
#Indicate timestep
##w.write("Timestep:"+str(timestep)+'\n')
##w.write("Total Number of Atoms:840\n")
##w.write('ID  TYPE Fx Fy Fz\n')
#create an empty list
ls = []

for i in range(lineindex):
    line = f.readline()
for i in range(840):
    list1 = line.split()
    ls.append(list1)
    line = f.readline()
ls.sort(key=lambda x: (x[1]),reverse=True)

for thing in ls:
    w.write(' '.join(thing)+'\n')
    
##        serial = list1[1]
##        if i+1 <= 10:
##            w.write('00' + str(i) +' '+str(serial)+str(list1[2:])+'\n')
##        elif i+1>10 and i <100:
##            w.write('0' + str(i) +' '+str(serial)+str(list1[2:])+'\n')
##        else:
##            w.write(str(i)+' '+str(serial)+str(list1[2:])+'\n')
##        line = f.readline()
    
f.close()
w.close()
