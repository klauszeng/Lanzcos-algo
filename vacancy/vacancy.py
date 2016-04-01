import random

vacancy = open("vacancy.ion", "r")
vacancyoutput = open("vacancyoutput","w")

for line in vacancy.readlines():
    i = 0
    if "Al 0." in line:
        i = i + 1
        x = "%.14f" % (float(line.split()[1])+ random.random())
        y = "%.14f" % (float(line.split()[2])+ random.random())
        z = "%.14f" % (float(line.split()[3])+ random.random())
        vacancyoutput.write(" ".join(["Al",x,y,z,"\n"]) )
    else:
        vacancyoutput.write(line)

vacancy.close()
vacancyoutput.close()
