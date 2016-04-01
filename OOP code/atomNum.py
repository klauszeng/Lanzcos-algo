def atomNum(filename):
    dataRead = open(filename, 'r')
    for i in range (3):
        copy = dataRead.readline()
    atomNum = int(copy.split()[0])
    dataRead.close()
    return atomNum
