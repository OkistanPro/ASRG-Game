import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *

import game

import time

import copy

camera = [0, 0]

fond = (0, 0, 0)

pause = 0
button = 0
gameovertimer = 0

phaseindex = 0

initcalques = {0:{
            "quatriemeFond" : [0, 0], 
            "quatriemeFondbis" : [960, 0], 
            "troisiemeFond" : [0, 150], 
            "troisiemeFondbis" : [960, 150], 
            "deuxiemeFond" : [0, 181], 
            "deuxiemeFondbis" : [960, 181], 
            "premierFond" : [0, 201], 
            "premierFondbis" : [960, 201], 
            "sol" : [0, 410], 
            "solbis" : [960, 410] ,
            "gameoverscreen" : [0, 0]
        }, 
        1:{
            "portee_haut" : [0, 120],
            "portee_bas" : [0, 300],
            "ligne" : [150, 0],
            "pers1" : [50, 280]
        },
        2:{},
        3:{},
        4:{
            "fondpause" : [0, 0],
            "bandeau_haut" : [0, 0], 
            "bandeau_bas" : [0, 470], 
            "cadreProgression" : [480 - (game.objects["cadreProgression"].sprites["anim1"][0].get_rect().width / 2), 492],
            "cadrePV" : [480 - (game.objects["cadrePV"].sprites["anim1"][0].get_rect().width / 2), 7], 
            "jaugeProgression" : [480 - (game.objects["jaugeProgression"].sprites["anim1"][0].get_rect().width / 2), 497], 
            "jaugeRougePV" : [480 - (game.objects["jaugeRougePV"].sprites["anim1"][0].get_rect().width / 2), 11], 
            "jaugeVertPV" : [480 - (game.objects["jaugeVertPV"].sprites["anim1"][0].get_rect().width / 2), 11], 
            "PV" : [480 - (game.objects["PV"].renderText().get_rect().width / 2), 10], 
            "score" : [10, 40],
            "numscore" : [10, 10],
            "combo" : [480 - (game.objects["combo"].renderText().get_rect().width / 2), 40],
            "pause" : [890, 0]
        }}

calques = copy.deepcopy(initcalques)

levelelements = levelmaker.getelements(PurePath("levelfiles/testniveau3.csv"))

def init():
    global calques, initcalques, camera, fond, pause, button, gameovertimer, levelelements
    pygame.mixer.music.load(PurePath("levelfiles/testniveau_music.wav"))
    pygame.mixer.music.play()
    # Setup les objets (changement des propriétés de chaque objet)
    calques = copy.deepcopy(initcalques)
    # print(init)
    #Tailles objets
    game.objects["pers1"].taillex = 0.5
    game.objects["pers1"].tailley = 0.5

    #Ombres objets
    game.objects["PV"].shadow = True
    game.objects["score"].shadow = True
    game.objects["numscore"].shadow = True
    game.objects["combo"].shadow = True

    #Parallax
    game.objects["premierFond"].parallax = game.objects["premierFondbis"].parallax = [0.8, 1.0]
    game.objects["deuxiemeFond"].parallax = game.objects["deuxiemeFondbis"].parallax = [0.6, 1.0]
    game.objects["troisiemeFond"].parallax = game.objects["troisiemeFondbis"].parallax = [0.4, 1.0]
    game.objects["quatriemeFond"].parallax = game.objects["quatriemeFondbis"].parallax = [0.2, 1.0]

    for object in calques[1]:
        game.objects[object].suivreScene = True

    for object in calques[4]:
        game.objects[object].suivreScene = True

    game.objects["fondpause"].visible = False
    game.objects["gameoverscreen"].visible = False
    game.objects["portee_haut"].visible = False
    game.objects["portee_bas"].visible = False
    game.objects["ligne"].visible = False
    game.objects["gameoverscreen"].suivreScene = True

    print(levelelements)
    """
    for element in levelelements:
        match element:
            case "phase":

            case "items":

            case "small":

            case "large":

            case "long":

            case "boss":

            case "fantome":

            case "normal":

            case "liee":

            case "silence":

            case "cube":

            case "pique":

            case "orbe":
            
            case "dash":
    """

    for element in levelelements:
        match element:
            case "phase":
                for phase in levelelements[element]:
                    if phase=="phase1" and levelelements[element][phase] != []:
                        game.objects["iconphase1"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase1.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface", "phase"]
                        )
                    if phase=="phase2" and levelelements[element][phase] != []:
                        game.objects["iconphase2"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase2.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface", "phase"]
                        )
                    if phase=="phase3" and levelelements[element][phase] != []:
                        game.objects["iconphase3"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase3.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface", "phase"]
                        )

            case "items":
                for note in levelelements[element]:
                    match note:
                        case "C5":
                            for time in levelelements[element][note]:
                                game.objects["coeurC5"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["coeurC5"+str(time)] = [(time * 600 / 1000) + 150, 382]
                        case "C#5":
                            for time in levelelements[element][note]:
                                game.objects["coeurC#5"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["coeurC#5"+str(time)] = [(time * 600 / 1000) + 150, 332]
                        case "D5":
                            for time in levelelements[element][note]:
                                game.objects["coeurD5"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["coeurD5"+str(time)] = [(time * 600 / 1000) + 150, 282]
                        case "D#5":
                            for time in levelelements[element][note]:
                                game.objects["coeurD#5"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["coeurD#5"+str(time)] = [(time * 600 / 1000) + 150, 232]
                        case "E5":
                            for time in levelelements[element][note]:
                                game.objects["coeurE5"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/coeurRouge.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["coeurE5"+str(time)] = [(time * 600 / 1000) + 150, 182]
                        case "C6":
                            for time in levelelements[element][note]:
                                game.objects["noteC6"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/note.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["noteC6"+str(time)] = [(time * 600 / 1000) + 150, 382]
                        case "C#6":
                            for time in levelelements[element][note]:
                                game.objects["noteC#6"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/note.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["noteC#6"+str(time)] = [(time * 600 / 1000) + 150, 332]
                        case "D6":
                            for time in levelelements[element][note]:
                                game.objects["noteD6"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/note.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["noteD6"+str(time)] = [(time * 600 / 1000) + 150, 282]
                        case "D#6":
                            for time in levelelements[element][note]:
                                game.objects["noteD#6"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/note.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["noteD#6"+str(time)] = [(time * 600 / 1000) + 150, 232]
                        case "E6":
                            for time in levelelements[element][note]:
                                game.objects["noteE6"+str(time)] = Actif(
                                    {"anim1" : [PurePath("images/level/note.png")]},
                                    {"anim1" : [False, 5]},
                                    "anim1",
                                    tags=["element", "elementup", "coeur"]
                                )
                                calques[3]["noteE6"+str(time)] = [(time * 600 / 1000) + 150, 182]
            case "small":
                for up in levelelements[element]['up']:
                    game.objects["smallu"+str(up)] = Actif(
                    {"anim1" : [PurePath("images/level/placeholder/small.png")]},
                    {"anim1" : [False, 5]},
                    "anim1",
                    tags=["element", "elementup", "small"]
                )
                    calques[3]["smallu"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    if up in levelelements[element]['down']:
                        game.objects["double"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/barredouble.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "double"]
                    )
                        calques[3]["double"+str(up)] = [(up * 600 / 1000) + 150, 210]
                for down in levelelements[element]['down']:
                    game.objects["smalld"+str(down)] = Actif(
                    {"anim1" : [PurePath("images/level/placeholder/small.png")]},
                    {"anim1" : [False, 5]},
                    "anim1",
                    tags=["element", "elementdown", "small"]
                )
                    calques[3]["smalld"+str(down)] = [(down * 600 / 1000) + 150, 340]
            
            case "large":
                for up in levelelements[element]['up']:
                        game.objects["large"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "large"]
                    )
                        calques[3]["large"+str(up)] = [(up * 600 / 1000) + 150, 135]
                for down in levelelements[element]['down']:
                        game.objects["large"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown", "large"]
                    )
                        calques[3]["large"+str(down)] = [(down * 600 / 1000) + 150, 315]

            case "long":
                for up in levelelements[element]['up']:
                        game.objects["longstart"+str(up[0])] = Actif(
                        {"anim1" : [PurePath("images/level/debutlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "start", "up"]
                    )
                        game.objects["longend"+str(up[1])] = Actif(
                        {"anim1" : [PurePath("images/level/finlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "end", "down"]
                    )
                        calques[3]["longstart"+str(up[0])] = [(up[0] * 600 / 1000) + 150, 150]
                        calques[3]["longend"+str(up[1])] = [(up[1] * 600 / 1000) -131, 150]
                for down in levelelements[element]['down']:
                        game.objects["longstart"+str(down[0])] = Actif(
                        {"anim1" : [PurePath("images/level/debutlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "start", "down"]
                    )
                        game.objects["longend"+str(down[1])] = Actif(
                        {"anim1" : [PurePath("images/level/finlongredi.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "long", "end", "down"]
                    )
                        calques[3]["longstart"+str(down[0])] = [(down[0] * 600 / 1000) + 150, 360]
                        calques[3]["longend"+str(down[1])] = [(down[1] * 600 / 1000) -131, 360]

            case "boss":
                for hit in levelelements[element]['hit']:
                        game.objects["boss"+str(hit)] = Actif(
                        {"anim1" : [PurePath("images/level/boss.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "boss", "hit"]
                    )
                        calques[3]["boss"+str(hit)] = [(hit * 600 / 1000) + 420, 100]
                for long in levelelements[element]['long']:
                        game.objects["boss"+str(long[0])] = Actif(
                        {"anim1" : [PurePath("images/level/boss.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "boss", "long", str(long[1])]
                    )
                        calques[3]["boss"+str(long[0])] = [(long[0] * 600 / 1000) + 420, 100]

            case "fantome":
                for up in levelelements[element]['up']:
                        game.objects["fantome"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/fantome.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "fantome"]
                    )
                        calques[3]["fantome"+str(up)] = [(up * 600 / 1000) + 150, 135]
                for down in levelelements[element]['down']:
                        game.objects["fantome"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/fantome.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown", "fantome"]
                    )
                        calques[3]["fantome"+str(down)] = [(down * 600 / 1000) + 150, 315]

            case "normal":
                for note in levelelements[element]:
                    match note:
                        case "G3" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 388]
                        case "A3" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 376]
                        case "B3" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 365]
                        case "C4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 353]
                        case "D4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 341]
                        case "E4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 330]
                        case "F4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 319]
                        case "G4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 307]
                        case "A4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 296]
                        case "B4" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        game.objects["dblcroche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["dblcroche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        game.objects["croche"+str(time[0])].sprites["anim1"][0] = pygame.transform.flip(game.objects["croche"+str(time[0])].sprites["anim1"][0], 0, 1)
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 281]

                        case "C5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 252]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 252-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 252-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 252-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 252-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 252]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 252]
                        case "D5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 221]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 221-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 221-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 221-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 221-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 221]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 221]
                        case "E5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 208]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 208-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 208-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 208-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 208-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 208]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 208]
                        case "F5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 196]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 196-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 196-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 196-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 196-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 196]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 196]
                        case "G5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 185]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 185-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 185-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 185-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 185-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 185]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 185]
                        case "A5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 173]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 173-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 173-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 173-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 173-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 173]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 173]
                        case "B5" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 161]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 161-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 161-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 161-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 161-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 161]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 161]
                        case "C6" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 150]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 150-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 150-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 150-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 150-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 150]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 150]
                        case "D6" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 139]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 139-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 139-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 139-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 139-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 139]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 139]
                        case "E6" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 127]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 127-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 127-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 127-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 127-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 127]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 127]
                        case "F6" :
                            for time in levelelements[element][note]:
                                if time[1]-time[0] <= 384:
                                    game.objects["noire"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/noire.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "noire"]
                                        )
                                    calques[3]["noire"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 116]
                                    if time[1]-time[0] <= 96:
                                        game.objects["dblcroche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/doublecroche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "dblcroche"]
                                        )
                                        
                                        calques[2]["dblcroche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 116-70]
                                    elif time[1]-time[0] <= 192:
                                        game.objects["croche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/croche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "croche"]
                                        )
                                        
                                        calques[2]["croche"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 116-70]
                                    else:
                                        game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                        calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 116-70]
                                elif time[1]-time[0] <= 768:
                                    game.objects["blanche"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/blanche.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "blanche"]
                                        )
                                    game.objects["lignenote"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/lignenote.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "lignenote"]
                                        )
                                    calques[2]["lignenote"+str(time[0])] = [(time[0] * 600 / 1000) + 176, 116-70]
                                    calques[3]["blanche"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 116]

                                elif time[1]-time[0] <= 1536:
                                    game.objects["ronde"+str(time[0])] = Actif(
                                            {"anim1" : [PurePath("images/level/ronde.png")]},
                                            {"anim1" : [False, 5]},
                                            "anim1",
                                            tags=["element", "ronde"]
                                        )
                                    calques[3]["ronde"+str(time[0])] = [(time[0] * 600 / 1000) + 150, 116]

            # case "liee":

            # case "silence":

            # case "cube":

            # case "pique":

            # case "orbe":
            
            # case "dash":

def loopevent(event):
    global calques, initcalques, camera, fond, pause, button, gameovertimer
    if event.type == KEYDOWN and event.key == K_f and gameovertimer == 0:
        calques[1]["pers1"][1] = 100

    if event.type == KEYDOWN and event.key == K_j and gameovertimer == 0:
        calques[1]["pers1"][1] = 280
        
    if event.type == game.objects["pause"].CLICKED and gameovertimer == 0:
        if pause == 0:
            game.objects["pause"].animCourante = "play"
            game.objects["pause"].imageCourante = 0
            game.objects["pause"].cptframe = 0
            game.objects["fondpause"].visible = True
            pygame.mixer.music.pause()
            pause = 1
        elif pause == 1:
            game.objects["pause"].animCourante = "pause"
            game.objects["pause"].imageCourante = 0
            game.objects["pause"].cptframe = 0
            game.objects["fondpause"].visible = False
            pygame.mixer.music.unpause()
            pause = 0
    
    if event.type == KEYDOWN and event.key == K_a:
            pygame.mixer.music.stop()
            game.objects["gameoverscreen"].visible = True
            gameovertimer = time.time()

    if event.type == KEYDOWN and event.key == K_v:
            game.scenecourante = "victoire"
            camera = [0, 0]
            pygame.mixer.music.stop()

def loopbeforeupdate():
    global pause, button, gameovertimer, camera, levelelements
    if (time.time() - gameovertimer) > 5 and gameovertimer != 0:
        game.scenecourante = "gameover"
        camera = [0, 0]
        gameovertimer = 0
    if pause == 0 and gameovertimer == 0:
        camera[0] = pygame.mixer.music.get_pos()*600/1000
    for phaseindex in range(len(levelelements["phase"])):
        if pygame.mixer.music.get_pos() < levelelements["phase"][phaseindex][1]:
            if levelelements["phase"][phaseindex-1][0] == "phase1" or levelelements["phase"][phaseindex-1][0] == "phase3":
                game.objects["portee_haut"].visible = False
                game.objects["portee_bas"].visible = False
                game.objects["ligne"].visible = False
                game.objects["sol"].visible = True
                game.objects["solbis"].visible = True
            elif levelelements["phase"][phaseindex-1][0] == "phase2":
                game.objects["portee_haut"].visible = True
                game.objects["portee_bas"].visible = True
                game.objects["ligne"].visible = True
                game.objects["sol"].visible = False
                game.objects["solbis"].visible = False
            break
        elif phaseindex == len(levelelements["phase"])-1:
            if levelelements["phase"][phaseindex][0] == "phase1" or levelelements["phase"][phaseindex][0] == "phase3":
                game.objects["portee_haut"].visible = False
                game.objects["portee_bas"].visible = False
                game.objects["ligne"].visible = False
                game.objects["sol"].visible = True
                game.objects["solbis"].visible = True
            elif levelelements["phase"][phaseindex][0] == "phase2":
                game.objects["portee_haut"].visible = True
                game.objects["portee_bas"].visible = True
                game.objects["ligne"].visible = True
                game.objects["sol"].visible = False
                game.objects["solbis"].visible = False


def loopafterupdate():
    global pause, button, gameovertimer, camera
    game.objects["pause"].activate(game.displaylist["pause"])

    for element in game.displaylist:
        if element in game.objects and isinstance(game.objects[element], Actif) and "boss" in game.objects[element].tags:
            if "hit" in game.objects[element].tags:
                calques[3][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 90
            elif "long" in game.objects[element].tags:
                if pygame.mixer.music.get_pos()-float(element[4:]) < 0:
                    calques[3][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 90
                elif pygame.mixer.music.get_pos()-float(game.objects[element].tags[-1]) < 0:
                    game.objects[element].suivreScene = True
                    calques[3][element][0] = 90
                else:
                    game.objects[element].suivreScene = False
                    calques[3][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(game.objects[element].tags[-1]))) + 90
    if game.displaylist["premierFond"].right == 0:
        calques[0]["premierFond"][0] += 1920
    if game.displaylist["premierFondbis"].right == 0:
        calques[0]["premierFondbis"][0] += 1920
    if game.displaylist["deuxiemeFond"].right == 0:
        calques[0]["deuxiemeFond"][0] += 1920
    if game.displaylist["deuxiemeFondbis"].right == 0:
        calques[0]["deuxiemeFondbis"][0] += 1920
    if game.displaylist["troisiemeFond"].right == 0:
        calques[0]["troisiemeFond"][0] += 1920
    if game.displaylist["troisiemeFondbis"].right == 0:
        calques[0]["troisiemeFondbis"][0] += 1920
    if game.displaylist["quatriemeFond"].right == 0:
        calques[0]["quatriemeFond"][0] += 1920
    if game.displaylist["quatriemeFondbis"].right == 0:
        calques[0]["quatriemeFondbis"][0] += 1920
    if "sol" in game.displaylist:
        if game.displaylist["solbis"].right == 0:
            calques[0]["solbis"][0] += 1920
        if game.displaylist["sol"].right == 0:
            calques[0]["sol"][0] += 1920