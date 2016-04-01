import os

filename = input("Please enter you filename including the extension.")

[name,extension] = [filename.split('.')[0],'.'+filename.split('.')[1]]
n=1
f = open(filename,'r')
while 'Atoms' not in f.readline()[0:5]:
    do = 'nothing happens'
do = f.readline()#empty line before Atoms
#create a file
w = open(name+'atom'+extension,'w')
line= f.readline()
while len(line)>3:
    w.write(line)
    line = f.readline()
##w.write('\n')
##w.write('velocity\n')
###skip 3 lines
##line = f.readline()
##line = f.readline()
##line = f.readline()
##while len(line)>3:
##    w.write(line)
##    line=f.readline()
    
f.close()
