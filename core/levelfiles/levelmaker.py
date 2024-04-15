import sys
def getelements(path):
    csvfile = open(path, "r")

    elements = {}
    typeelement = ""

    precision = 0
    mstick = 0

    flagliee = False

    for line in csvfile:
        channel, time, control = line[:-1].split(", ")[:3]
        paramlist = line[:-1].split(", ")[3:]

        if control == "Header":
            precision = int(paramlist[2])
        if control == "Tempo":
            mstick = (int(paramlist[0])/1000)/precision
        if control == "Title_t":
            typeelement = paramlist[0][1:-1]
            match paramlist[0][1:-1]:
                case "phase":
                    elements[typeelement] = []
                case "small" | "large" | "fantome" | "long" :
                    elements[typeelement] = {"up" : [], "down" : []}
                case "items":
                    elements[typeelement] = {
                        "C5" : [],
                        "C#5" : [],
                        "D5" : [],
                        "D#5" : [],
                        "E5" : [],
                        "F5" : [],
                        "C6" : [],
                        "C#6" : [],
                        "D6" : [],
                        "D#6" : [],
                        "E6" : [],
                        "F6" : [],
                    }
                case "boss":
                    elements[typeelement] = {"hit" : [], "long" : []}
                case "normal":
                    elements[typeelement] = []
                case "liee":
                    elements[typeelement] = {
                        "flagliee" : [],
                        "lieehaut" : [],
                        "lieebas" : []
                    }
                case "silence":
                    elements[typeelement] = {"up" : [], "middle" : [], "down" : []}
                case "cube" | "pique" | "orbe" | "dash":
                    elements[typeelement] = [] #[[hauteur,milisecondes], [...]]

        if control == "Note_on_c":
            match typeelement:
                case "items":
                    match paramlist[1]:
                        case "60":
                            elements[typeelement]["C5"].append(int(time)*mstick)
                        case "61":
                            elements[typeelement]["C#5"].append(int(time)*mstick)
                        case "62":
                            elements[typeelement]["D5"].append(int(time)*mstick)
                        case "63":
                            elements[typeelement]["D#5"].append(int(time)*mstick)
                        case "64":
                            elements[typeelement]["E5"].append(int(time)*mstick)
                        case "65":
                            elements[typeelement]["F6"].append(int(time)*mstick)
                        case "72":
                            elements[typeelement]["C6"].append(int(time)*mstick)
                        case "73":
                            elements[typeelement]["C#6"].append(int(time)*mstick)
                        case "74":
                            elements[typeelement]["D6"].append(int(time)*mstick)
                        case "75":
                            elements[typeelement]["D#6"].append(int(time)*mstick)
                        case "76":
                            elements[typeelement]["E6"].append(int(time)*mstick)
                        case "77":
                            elements[typeelement]["F6"].append(int(time)*mstick)
                case "small" | "large" | "fantome":
                    if paramlist[1] == "61":
                        elements[typeelement]["up"].append(int(time)*mstick)
                    if paramlist[1] == "60":
                        elements[typeelement]["down"].append(int(time)*mstick)
                case "long":
                    if paramlist[1] == "61":
                        elements[typeelement]["up"].append([int(time)*mstick])
                    if paramlist[1] == "60":
                        elements[typeelement]["down"].append([int(time)*mstick])
                case "boss":
                    if paramlist[1] == "61":
                        elements[typeelement]["long"].append([int(time)*mstick])
                    if paramlist[1] == "60":
                        elements[typeelement]["hit"].append(int(time)*mstick)
                case "phase":
                    if paramlist[1] == "60":
                        elements[typeelement].append(("phase1", int(time)*mstick))
                    if paramlist[1] == "61":
                        elements[typeelement].append(("phase2", int(time)*mstick))
                    if paramlist[1] == "62":
                        elements[typeelement].append(("phase3", int(time)*mstick))
                case "silence":
                    if paramlist[1] == "60":
                        elements[typeelement]["down"].append(int(time)*mstick)
                    if paramlist[1] == "61":
                        elements[typeelement]["middle"].append(int(time)*mstick)
                    if paramlist[1] == "62":
                        elements[typeelement]["up"].append(int(time)*mstick)
                case "normal":
                    if int(paramlist[1]) < 78 and int(paramlist[1]) > 42:
                        elements[typeelement].append([paramlist[1], int(time)*mstick])
                case "liee":
                    if paramlist[1] == "41":
                        elements[typeelement]["flagliee"].append([int(time)*mstick])
                    if paramlist[1] == "40":
                        elements[typeelement]["lieehaut"].append(int(time)*mstick)
                    if paramlist[1] == "39":
                        elements[typeelement]["lieebas"].append(int(time)*mstick)
                case "cube" | "orbe" | "dash" | "pique":
                    pos = int(paramlist[1])-60
                    elements[typeelement].append([pos, int(time)*mstick])


        if control == "Note_off_c":
            match typeelement:
                case "long":
                    if paramlist[1] == "61":
                        elements[typeelement]["up"][-1].append(int(time)*mstick)
                    if paramlist[1] == "60":
                        elements[typeelement]["down"][-1].append(int(time)*mstick)
                case "boss":
                    if paramlist[1] == "61":
                        elements[typeelement]["long"][-1].append(int(time)*mstick)
                case "normal":
                    if int(paramlist[1]) < 78 and int(paramlist[1]) > 42:
                        elements[typeelement][-1].append(int(time)*mstick)
                case "liee":
                    if paramlist[1] == "41":
                        elements[typeelement]["flagliee"][-1].append(int(time)*mstick)

    csvfile.close()
    return elements