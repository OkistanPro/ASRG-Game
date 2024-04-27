import sys
import numpy as np

precision = 0

def getelements(path):
    global precision
    csvfile = open(path, "r")

    elements = {}
    typeelement = ""

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
                    elements[typeelement] = {}
                case "theme":
                    elements[typeelement] = [] #[[num dossier, milisecondes], [...]]

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
                            elements[typeelement]["F5"].append(int(time)*mstick)
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
                    compteurcube = 0
                    if paramlist[1] == "59":
                        elements[typeelement].append(("phase0", int(time)*mstick))
                        phase3 = False
                    if paramlist[1] == "60":
                        elements[typeelement].append(("phase1", int(time)*mstick))
                        phase3 = False
                    if paramlist[1] == "61":
                        elements[typeelement].append(("phase2", int(time)*mstick))
                        phase3 = False
                    if paramlist[1] == "62":
                        elements[typeelement].append(("phase3", int(time)*mstick))
                        phase3 = True
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
                case "cube" | "dash" | "pique":
                    if int(paramlist[1]) > 59 and int(paramlist[1]) < 66:
                        pos = int(paramlist[1])-60
                        if str(int(time)*mstick) not in elements[typeelement]:
                            elements[typeelement][str(int(time)*mstick)] = [0, 0, 0, 0, 0, 0]
                        elements[typeelement][str(int(time)*mstick)][pos] = 1
                case "orbe":
                    if int(paramlist[1]) > 59 and int(paramlist[1]) < 66:
                        pos = int(paramlist[1])-60
                        if str(int(time)*mstick) not in elements[typeelement]:
                            elements[typeelement][str(int(time)*mstick)] = [[0, 0, 0, 0, 0, 0], paramlist[2]]
                        elements[typeelement][str(int(time)*mstick)][0][pos] = 1
                case "theme":
                    numdossier = int(paramlist[1])-60
                    elements[typeelement].append([numdossier, int(time)*mstick])


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
    mincube = min([float(list(elements["cube"].keys())[i+1])-float(list(elements["cube"].keys())[i]) for i in range(len(list(elements["cube"].keys()))-1)])
    elements["mincube"] = mincube

    print(elements["orbe"])
    
    if elements["cube"]:
        for time in [str(element) for element in np.arange(float(list(elements["cube"].keys())[0]), float(list(elements["cube"].keys())[-1]), mincube*mstick) if str(element) not in list(elements["cube"].keys())]:
            elements["cube"][time] = [0, 0, 0, 0, 0, 0]
            elements["orbe"][time] = [0, 0, 0, 0, 0, 0]
            elements["dash"][time] = [0, 0, 0, 0, 0, 0]
            elements["pique"][time] = [0, 0, 0, 0, 0, 0]
    if elements["orbe"]:
        for time in [str(element) for element in np.arange(float(list(elements["orbe"].keys())[0]), float(list(elements["orbe"].keys())[-1]), mincube*mstick) if str(element) not in list(elements["orbe"].keys())]:
            elements["cube"][time] = [0, 0, 0, 0, 0, 0]
            elements["orbe"][time] = [0, 0, 0, 0, 0, 0]
            elements["dash"][time] = [0, 0, 0, 0, 0, 0]
            elements["pique"][time] = [0, 0, 0, 0, 0, 0]
    if elements["dash"]:
        for time in [str(element) for element in np.arange(float(list(elements["dash"].keys())[0]), float(list(elements["dash"].keys())[-1]), mincube*mstick) if str(element) not in list(elements["dash"].keys())]:
            elements["cube"][time] = [0, 0, 0, 0, 0, 0]
            elements["orbe"][time] = [0, 0, 0, 0, 0, 0]
            elements["dash"][time] = [0, 0, 0, 0, 0, 0]
            elements["pique"][time] = [0, 0, 0, 0, 0, 0]
    if elements["pique"]:
        for time in [str(element) for element in np.arange(float(list(elements["pique"].keys())[0]), float(list(elements["pique"].keys())[-1]), mincube*mstick) if str(element) not in list(elements["pique"].keys())]:
            elements["cube"][time] = [0, 0, 0, 0, 0, 0]
            elements["orbe"][time] = [0, 0, 0, 0, 0, 0]
            elements["dash"][time] = [0, 0, 0, 0, 0, 0]
            elements["pique"][time] = [0, 0, 0, 0, 0, 0]

    elements["cube"] = dict(sorted(elements["cube"].items()))
    elements["orbe"] = dict(sorted(elements["orbe"].items()))
    elements["dash"] = dict(sorted(elements["dash"].items()))
    elements["pique"] = dict(sorted(elements["pique"].items()))
    return elements