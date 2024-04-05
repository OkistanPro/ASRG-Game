import sys

csvfile = open(sys.argv[1], "r")

elements = {}
typeelement = ""

precision = 0
mstick = 0

for line in csvfile:
    channel, time, control = line[:-1].split(", ")[:3]
    paramlist = line[:-1].split(", ")[3:]

    if control == "Header":
        precision = int(paramlist[2])
    if control == "Tempo":
        mstick = (int(paramlist[0])/1000)/precision
    if control == "Title_t":
        if "small" in paramlist[0]:
            typeelement = "small"
            elements[typeelement] = {"up" : [], "down" : []}
    
    if control == "Note_on_c" and typeelement != "long":
        if paramlist[1] == "61":
            elements[typeelement]["up"].append(int(time)*mstick)
        if paramlist[1] == "60":
            elements[typeelement]["down"].append(int(time)*mstick)

print(elements)

csvfile.close()