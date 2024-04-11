import sys
def getelements(path):
    csvfile = open(path, "r")

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
                case "normal" | "liee":
                    elements[typeelement] = {
                        "G3" : [],
                        "A3" : [],
                        "B3" : [],
                        "C4" : [],
                        "D4" : [],
                        "E4" : [],
                        "F4" : [],
                        "G4" : [],
                        "A4" : [],
                        "B4" : [],
                        "C5" : [],
                        "D5" : [],
                        "E5" : [],
                        "F5" : [],
                        "G5" : [],
                        "A5" : [],
                        "B5" : [],
                        "C6" : [],
                        "D6" : [],
                        "E6" : [],
                        "F6" : [],
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
                    match paramlist[1]:
                        case "43":
                            elements[typeelement]["G3"].append([int(time)*mstick])
                        case "45":
                            elements[typeelement]["A3"].append([int(time)*mstick])
                        case "47":
                            elements[typeelement]["B3"].append([int(time)*mstick])
                        case "48":
                            elements[typeelement]["C4"].append([int(time)*mstick])
                        case "50":
                            elements[typeelement]["D4"].append([int(time)*mstick])
                        case "52":
                            elements[typeelement]["E4"].append([int(time)*mstick])
                        case "53":
                            elements[typeelement]["F4"].append([int(time)*mstick])
                        case "55":
                            elements[typeelement]["G4"].append([int(time)*mstick])
                        case "57":
                            elements[typeelement]["A4"].append([int(time)*mstick])
                        case "59":
                            elements[typeelement]["B4"].append([int(time)*mstick])
                        case "60":
                            elements[typeelement]["C5"].append([int(time)*mstick])
                        case "62":
                            elements[typeelement]["D5"].append([int(time)*mstick])
                        case "64":
                            elements[typeelement]["E5"].append([int(time)*mstick])
                        case "65":
                            elements[typeelement]["F5"].append([int(time)*mstick])
                        case "67":
                            elements[typeelement]["G5"].append([int(time)*mstick])
                        case "69":
                            elements[typeelement]["A5"].append([int(time)*mstick])
                        case "71":
                            elements[typeelement]["B5"].append([int(time)*mstick])
                        case "72":
                            elements[typeelement]["C6"].append([int(time)*mstick])
                        case "74":
                            elements[typeelement]["D6"].append([int(time)*mstick])
                        case "76":
                            elements[typeelement]["E6"].append([int(time)*mstick])
                        case "77":
                            elements[typeelement]["F6"].append([int(time)*mstick])
                case "liee":
                    match paramlist[1]:
                        case "43":
                            elements[typeelement]["G3"].append([int(time)*mstick])
                        case "45":
                            elements[typeelement]["A3"].append([int(time)*mstick])
                        case "47":
                            elements[typeelement]["B3"].append([int(time)*mstick])
                        case "48":
                            elements[typeelement]["C4"].append([int(time)*mstick])
                        case "50":
                            elements[typeelement]["D4"].append([int(time)*mstick])
                        case "52":
                            elements[typeelement]["E4"].append([int(time)*mstick])
                        case "53":
                            elements[typeelement]["F4"].append([int(time)*mstick])
                        case "55":
                            elements[typeelement]["G4"].append([int(time)*mstick])
                        case "57":
                            elements[typeelement]["A4"].append([int(time)*mstick])
                        case "59":
                            elements[typeelement]["B4"].append([int(time)*mstick])
                        case "60":
                            elements[typeelement]["C5"].append([int(time)*mstick])
                        case "62":
                            elements[typeelement]["D5"].append([int(time)*mstick])
                        case "64":
                            elements[typeelement]["E5"].append([int(time)*mstick])
                        case "65":
                            elements[typeelement]["F5"].append([int(time)*mstick])
                        case "67":
                            elements[typeelement]["G5"].append([int(time)*mstick])
                        case "69":
                            elements[typeelement]["A5"].append([int(time)*mstick])
                        case "71":
                            elements[typeelement]["B5"].append([int(time)*mstick])
                        case "72":
                            elements[typeelement]["C6"].append([int(time)*mstick])
                        case "74":
                            elements[typeelement]["D6"].append([int(time)*mstick])
                        case "76":
                            elements[typeelement]["E6"].append([int(time)*mstick])
                        case "77":
                            elements[typeelement]["F6"].append([int(time)*mstick])
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
                case "normal" | "liee" :
                    match paramlist[1]:
                        case "43":
                            elements[typeelement]["G3"][-1].append(int(time)*mstick)
                        case "45":
                            elements[typeelement]["A3"][-1].append(int(time)*mstick)
                        case "47":
                            elements[typeelement]["B3"][-1].append(int(time)*mstick)
                        case "48":
                            elements[typeelement]["C4"][-1].append(int(time)*mstick)
                        case "50":
                            elements[typeelement]["D4"][-1].append(int(time)*mstick)
                        case "52":
                            elements[typeelement]["E4"][-1].append(int(time)*mstick)
                        case "53":
                            elements[typeelement]["F4"][-1].append(int(time)*mstick)
                        case "55":
                            elements[typeelement]["G4"][-1].append(int(time)*mstick)
                        case "57":
                            elements[typeelement]["A4"][-1].append(int(time)*mstick)
                        case "59":
                            elements[typeelement]["B4"][-1].append(int(time)*mstick)
                        case "60":
                            elements[typeelement]["C5"][-1].append(int(time)*mstick)
                        case "62":
                            elements[typeelement]["D5"][-1].append(int(time)*mstick)
                        case "64":
                            elements[typeelement]["E5"][-1].append(int(time)*mstick)
                        case "65":
                            elements[typeelement]["F5"][-1].append(int(time)*mstick)
                        case "67":
                            elements[typeelement]["G5"][-1].append(int(time)*mstick)
                        case "69":
                            elements[typeelement]["A5"][-1].append(int(time)*mstick)
                        case "71":
                            elements[typeelement]["B5"][-1].append(int(time)*mstick)
                        case "72":
                            elements[typeelement]["C6"][-1].append(int(time)*mstick)
                        case "74":
                            elements[typeelement]["D6"][-1].append(int(time)*mstick)
                        case "76":
                            elements[typeelement]["E6"][-1].append(int(time)*mstick)
                        case "77":
                            elements[typeelement]["F6"][-1].append(int(time)*mstick)

    csvfile.close()
    return elements