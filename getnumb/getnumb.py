import os
def getNumb():
    filename = input("Please enter the file name(string ex readme.txt).")
    n = 0
    check = 'False'
    if os.path.isfile(filename):
        check = 'True'
        while check == 'True':
            fp = open(filename,'r+')
            for line in fp.readlines():
                if '@   xaxis label ' in line:
                    beginning = line.find('= ')+2
                    ending = line.find('eV')-1
                    numb = line[beginning:ending]
                else:
                    pass
            value = str(n)+'. ' + str(numb)
            n=n+1
            numbfile.write(value)
            check = 'False'
            filename = filename + str(n)
            fp.close()
    else:
        print("The filename you enter doesn't exist, please try again.")
    
    fp.close()
