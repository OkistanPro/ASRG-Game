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
        if "large" in paramlist[0]:
            typeelement = "large"
            elements[typeelement] = {"up" : [], "down" : []}
        if "notes" in paramlist[0]:
            typeelement = "notes"
            elements[typeelement] = {"up" : [], "down" : []}
        if "coeur" in paramlist[0]:
            typeelement = "coeur"
            elements[typeelement] = {"up" : [], "down" : []}
        if "fantome" in paramlist[0]:
            typeelement = "fantome"
            elements[typeelement] = {"up" : [], "down" : []}
        if "long" in paramlist[0]:
            typeelement = "long"
            elements[typeelement] = {"up" : [], "down" : []}
            # "up" : [[depart, arrivé], [...]]
        if "boss" in paramlist[0]:
            typeelement = "boss"
            elements[typeelement] = {"hit" : [], "long" : []}
            # "hit" : [temps1, temps2, ...], "long" [[depart, arrivé], [...]]

    if control == "Note_on_c" and typeelement != "long" and typeelement != "boss":
        if paramlist[1] == "61":
            elements[typeelement]["up"].append(int(time)*mstick)
        if paramlist[1] == "60":
            elements[typeelement]["down"].append(int(time)*mstick)
    
    if control == "Note_on_c" and typeelement == "long":
        if paramlist[1] == "61":
            elements[typeelement]["up"].append([int(time)*mstick])
        if paramlist[1] == "60":
            elements[typeelement]["down"].append([int(time)*mstick])
    
    if control == "Note_off_c" and typeelement == "long":
        if paramlist[1] == "61":
            elements[typeelement]["up"][-1].append(int(time)*mstick)
        if paramlist[1] == "60":
            elements[typeelement]["down"][-1].append(int(time)*mstick)

    if control == "Note_on_c" and typeelement == "boss":
        if paramlist[1] == "61":
            elements[typeelement]["long"].append([int(time)*mstick])
        if paramlist[1] == "60":
            elements[typeelement]["hit"].append(int(time)*mstick)

    if control == "Note_off_c" and typeelement == "boss":
        if paramlist[1] == "61":
            elements[typeelement]["long"][-1].append(int(time)*mstick)


print(elements)

csvfile.close()