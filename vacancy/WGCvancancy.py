

WGCvancancy = open("WGCvacancy_unrelaxed", "r")
WGCvancancyout = open("WGCvancacy_output","w")

for line in WGCvancancy.readlines():
    i = 0
    if ": Al" in line:
        i =  i + 1
        x = line.split()[3]
        y = line.split()[4]
        z = line.split()[5]
        print(x,y,z)
        WGCvancancyout.write(str(i)+ '\t' + str(x) + '\t' + str(y)+ '\t' + str(z)+ '\n')

WGCvancancy.close()
WGCvancancyout.close()
