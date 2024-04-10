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

initcalques = {0:{
            "quatriemeFond" : [0, 0], 
            "quatriemeFondbis" : [960, 0], 
            "troisiemeFond" : [0, 150], 
            "troisiemeFondbis" : [960, 150], 
            "deuxiemeFond" : [0, 181], 
            "deuxiemeFondbis" : [960, 181], 
            "premierFond" : [0, 181], 
            "premierFondbis" : [960, 181], 
            "sol" : [0, 410], 
            "solbis" : [960, 410] ,
            "gameoverscreen" : [0, 0]
        }, 
        1:{
            "pers1" : [50, 280]
        }, 
        2:{},
        3:{
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

def init():
    global calques, initcalques, camera, fond, pause, button, gameovertimer
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

    for object in calques[3]:
        game.objects[object].suivreScene = True

    game.objects["fondpause"].visible = False
    game.objects["gameoverscreen"].visible = False
    game.objects["gameoverscreen"].suivreScene = True

    levelelements = levelmaker.getelements(PurePath("levelfiles/testniveau3.csv"))
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
                if levelelements[element]["notes"] != {"up" : [], "down" : []}:
                    for up in levelelements[element]["notes"]['up']:
                        game.objects["note"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/note.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "items", "notes"]
                    )
                        calques[2]["note"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    for down in levelelements[element]["notes"]['down']:
                        game.objects["note"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/note.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown", "items", "notes"]
                    )
                        calques[2]["note"+str(down)] = [(down * 600 / 1000) + 150, 340]

                if levelelements[element]["coeur"] != {"up" : [], "down" : []}:
                    for up in levelelements[element]["coeur"]['up']:
                        game.objects["coeur"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/coeur.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "items", "coeur"]
                    )
                        calques[2]["coeur"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    for down in levelelements[element]["coeur"]['down']:
                        game.objects["coeur"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/coeur.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown", "items", "coeur"]
                    )
                        calques[2]["coeur"+str(down)] = [(down * 600 / 1000) + 150, 340]
            case "small":
                for up in levelelements[element]['up']:
                    game.objects["smallu"+str(up)] = Actif(
                    {"anim1" : [PurePath("images/level/placeholder/small.png")]},
                    {"anim1" : [False, 5]},
                    "anim1",
                    tags=["element", "elementup", "small"]
                )
                    calques[2]["smallu"+str(up)] = [(up * 600 / 1000) + 150, 160]
                    if up in levelelements[element]['down']:
                        game.objects["double"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/barredouble.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "double"]
                    )
                        calques[2]["double"+str(up)] = [(up * 600 / 1000) + 150, 210]
                for down in levelelements[element]['down']:
                    game.objects["smalld"+str(down)] = Actif(
                    {"anim1" : [PurePath("images/level/placeholder/small.png")]},
                    {"anim1" : [False, 5]},
                    "anim1",
                    tags=["element", "elementdown", "small"]
                )
                    calques[2]["smalld"+str(down)] = [(down * 600 / 1000) + 150, 340]
            
            case "large":
                for up in levelelements[element]['up']:
                        game.objects["large"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "large"]
                    )
                        calques[2]["large"+str(up)] = [(up * 600 / 1000) + 150, 135]
                for down in levelelements[element]['down']:
                        game.objects["large"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown", "large"]
                    )
                        calques[2]["large"+str(down)] = [(down * 600 / 1000) + 150, 315]

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
                        calques[2]["longstart"+str(up[0])] = [(up[0] * 600 / 1000) + 150, 150]
                        calques[2]["longend"+str(up[1])] = [(up[1] * 600 / 1000) -131, 150]
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
                        calques[2]["longstart"+str(down[0])] = [(down[0] * 600 / 1000) + 150, 360]
                        calques[2]["longend"+str(down[1])] = [(down[1] * 600 / 1000) -131, 360]

            case "boss":
                for hit in levelelements[element]['hit']:
                        game.objects["boss"+str(hit)] = Actif(
                        {"anim1" : [PurePath("images/level/boss.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "boss", "hit"]
                    )
                        calques[2]["boss"+str(hit)] = [(hit * 600 / 1000) + 420, 100]
                for long in levelelements[element]['long']:
                        game.objects["boss"+str(long[0])] = Actif(
                        {"anim1" : [PurePath("images/level/boss.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "boss", "long", str(long[1])]
                    )
                        calques[2]["boss"+str(long[0])] = [(long[0] * 600 / 1000) + 420, 100]

            case "fantome":
                for up in levelelements[element]['up']:
                        game.objects["fantome"+str(up)] = Actif(
                        {"anim1" : [PurePath("images/level/fantome.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementup", "fantome"]
                    )
                        calques[2]["fantome"+str(up)] = [(up * 600 / 1000) + 150, 135]
                for down in levelelements[element]['down']:
                        game.objects["fantome"+str(down)] = Actif(
                        {"anim1" : [PurePath("images/level/fantome.png")]},
                        {"anim1" : [False, 5]},
                        "anim1",
                        tags=["element", "elementdown", "fantome"]
                    )
                        calques[2]["fantome"+str(down)] = [(down * 600 / 1000) + 150, 315]

            # case "normal":

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
    global pause, button, gameovertimer, camera
    if (time.time() - gameovertimer) > 5 and gameovertimer != 0:
        game.scenecourante = "gameover"
        camera = [0, 0]
        gameovertimer = 0
    if pause == 0 and gameovertimer == 0:
        camera[0] = pygame.mixer.music.get_pos()*600/1000

def loopafterupdate():
    global pause, button, gameovertimer, camera
    game.objects["pause"].activate(game.displaylist["pause"])

    for element in game.displaylist:
        if element in game.objects and isinstance(game.objects[element], Actif) and "boss" in game.objects[element].tags:
            if "hit" in game.objects[element].tags:
                calques[2][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 90
            elif "long" in game.objects[element].tags:
                if pygame.mixer.music.get_pos()-float(element[4:]) < 0:
                    calques[2][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 90
                elif pygame.mixer.music.get_pos()-float(game.objects[element].tags[-1]) < 0:
                    game.objects[element].suivreScene = True
                    calques[2][element][0] = 90
                else:
                    game.objects[element].suivreScene = False
                    calques[2][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(game.objects[element].tags[-1]))) + 90
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
    if game.displaylist["solbis"].right == 0:
        calques[0]["solbis"][0] += 1920
    if game.displaylist["sol"].right == 0:
        calques[0]["sol"][0] += 1920