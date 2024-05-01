import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *
import os
import io
import zipfile
import game
import tweener

import time

import copy

camera = [0, 0]

fond = (0, 0, 0)

objects = {}

listlevel = []
indexselection = 0

animselection = tweener.Tween(
    begin=0,
    end=643,
    duration=600,
    easing=tweener.Easing.CUBIC,
    easing_mode=tweener.EasingMode.OUT
)


calques = {}

def init():
    global objects, calques, camera, fond, listlevel
    if not objects:
        objects.update({
            "fond_selection" : Actif(
                {"anim1" : [PurePath("images/fonds/animation/ecran_selecteur_niveau/ecran_selecteur_niveau_" + format(i, '05d') + ".jpg") for i in range(125)], 
                "anim2" : [PurePath("images/fonds/animation/ecran_selecteur_niveau2/ecran_selecteur_niveau2_" + format(i, '05d') + ".jpg") for i in range(125)]},
                {"anim1" : [True, 2],
                "anim2" : [True, 2]},
                "anim2"
            ),
            "perso" : Bouton(
                {"logoperso" :
            [
                [PurePath("images/interface/logoperso.png")],
                [PurePath("images/interface/logoperso.png")],
                [PurePath("images/interface/logoperso.png")],
                [PurePath("images/interface/logoperso.png")],
                [PurePath("images/interface/logoperso.png")]
            ]},
            {"logoperso" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "logoperso"
            ),
            "cadreniv" : Actif
                ({"anim1" : [PurePath("images/interface/cadreniv.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "jaugevideniv" : Actif
                ({"anim1" : [PurePath("images/interface/jauge_selecteur_niveau.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "jaugerempliniv" : Actif
                ({"anim1" : [PurePath("images/interface/bandeauniv.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "param" : Bouton(
                {"param" :
            [
                [PurePath("images/interface/parametre.png")],
                [PurePath("images/interface/parametre.png")],
                [PurePath("images/interface/parametre.png")],
                [PurePath("images/interface/parametre.png")],
                [PurePath("images/interface/parametre.png")]
            ]},
            {"param" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "param"
            ),
            "fleche1" : Actif
                ({"anim1" : [PurePath("images/interface/fleche_gauche.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "fleche2" : Actif
                ({"anim1" : [PurePath("images/interface/fleche_droite.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "cube1" : Actif
                ({"anim1" : [PurePath("images/interface/cubeblanc.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "cube2" : Actif
                ({"anim1" : [PurePath("images/interface/cubeblanc.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            ),
            "difficulte" : Text(
                "1/3",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                30,
                (255, 255, 255)
            ),
            "niveau" : Text(
                "Niv. 2",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                20,
                (255, 255, 255)
            )})
    calques.update({
        0:{
            "fond_selection" : [0, 0]
        },
        "fondlevel" : {},
        1:{},
        2:{
            "perso" : [0, 0],
            "cadreniv" : [335, 0],
            "jaugevideniv" : [345, 10],
            "jaugerempliniv" : [345, 10],
            "param" : [890, 0],
            "fleche1" : [123, 219],
            "fleche2" : [736, 221],  
            "cube1" : [0, 470],
            "cube2" : [890, 470],
            "niveau" : [460, 15]
        }})
    objects["jaugerempliniv"].taillex = 0.45

    listlevel = []

    for file in os.listdir("levelfiles"):
        if file.endswith(".asrg"):
            namelevel = file[2:-5]
            objects["barreniv"+namelevel] = Actif(
                {"anim1" : [PurePath("images/fonds/barre_fond_selecteur_niveau.png")]},
                {"anim1" : [False, 5]},
                "anim1"
            )
            objects["imageniv"+namelevel] = Bouton(
                    {"anim1" :
                [
                    [PurePath("images/fonds/fond_selection_" + namelevel + ".png")],
                    [PurePath("images/fonds/fond_selection_" + namelevel + ".png")],
                    [PurePath("images/fonds/fond_selection_" + namelevel + ".png")],
                    [PurePath("images/fonds/fond_selection_" + namelevel + ".png")],
                    [PurePath("images/fonds/fond_selection_" + namelevel + ".png")]
                ]},
                {"anim1" :[
                    [False, 0, 5],
                    [False, 0, 5],
                    [False, 0, 5],
                    [False, 0, 5],
                    [False, 0, 5]
                ]},
                "anim1"
                )
            
            with zipfile.ZipFile(PurePath("levelfiles/" + file), "r") as filelevel:
                fileconfig = io.TextIOWrapper(filelevel.open(namelevel + ".config"))
                title = ""
                pathfont = ""
                for line in fileconfig:
                    if "TITLE" in line:
                        title = line.split("\t")[1][:-1]
                    if "FICHIERPOLICE" in line:
                        pathfont = "fonts/"+line.split("\t")[1][:-1]
                    if "PHASES" in line:
                        listphases = line[:-1].split("\t")[1:]
                        print(listphases)
                        if "1" in listphases:
                            objects["phase1"+namelevel] = Actif(
                                {"anim1" : [PurePath("images/interface/icone_phase1.png")]},
                                {"anim1" : [False, 5]},
                                "anim1"
                            )
                            calques[1]["phase1"+namelevel] = [500 + len(listlevel)*643 + listphases.index("1")*62, 282]
                        if "2" in listphases:
                            objects["phase2"+namelevel] = Actif(
                                {"anim1" : [PurePath("images/interface/icone_phase2.png")]},
                                {"anim1" : [False, 5]},
                                "anim1"
                            )
                            calques[1]["phase2"+namelevel] = [500 + len(listlevel)*643 + listphases.index("2")*62, 282]
                        if "3" in listphases:
                            objects["phase3"+namelevel] = Actif(
                                {"anim1" : [PurePath("images/interface/icone_phase3.png")]},
                                {"anim1" : [False, 5]},
                                "anim1"
                            )
                            calques[1]["phase3"+namelevel] = [500 + len(listlevel)*643 + listphases.index("3")*62, 282]
                    
                objects["nomniv"+namelevel] = Text(
                    "",
                    PurePath(pathfont),
                    35,
                    (255, 255, 255)
                )
                objects["nomniv"+namelevel].changeTexte(title)

                
            calques["fondlevel"]["imageniv"+namelevel] = [257 + len(listlevel)*643, 135]
            calques["fondlevel"]["barreniv"+namelevel] = [257 + len(listlevel)*643, 278]
            calques[1]["nomniv"+namelevel] = [273 + len(listlevel)*643, 292]
            listlevel.append(namelevel)
    
    with open("save.asrg", "r") as filesave:
        titlelevel = ""
        for line in filesave:
            if "LEVELNAME" in line:
                titlelevel = line.split("\t")[1][:-1]
            if "PROGRESSION" in line and titlelevel.lower() in listlevel:
                progress = line.split("\t")[1][:-1]
                objects["pourcentniv"+titlelevel.lower()] = Text(
                    progress+"%",
                    PurePath("fonts/LTSaeada-SemiBold.otf"),
                    35,
                    (255, 255, 255)
                )
                calques[1]["pourcentniv"+titlelevel.lower()] = [333 + listlevel.index(titlelevel.lower())*643, 357]
            if "DONE" in line and titlelevel.lower() in listlevel:
                donelevel = line.split("\t")[1][:-1]
                objects["difficulte"+titlelevel.lower()] = Text(
                    donelevel+"/3",
                    PurePath("fonts/LTSaeada-SemiBold.otf"),
                    30,
                    (255, 255, 255)
                )
                calques[1]["difficulte"+titlelevel.lower()] = [569 + listlevel.index(titlelevel.lower())*643, 355]

    for element in calques[0]:
        objects[element].suivreScene = True
    for element in calques[2]:
        objects[element].suivreScene = True

    """for file in listlevel:
        with zipfile.ZipFile(PurePath("levelfiles/" + file), "r") as filelevel:
            fileconfig = io.TextIOWrapper(filelevel.open(namelevel + ".config"))
            for line in fileconfig:
                if "TITLE" in str(line):
                    title = str(line).split("\t")[1][:-1]
                    print(title)"""
    


def loopevent(event):
    global indexselection, listlevel, animselection
    if event.type == KEYDOWN and event.key == K_RETURN :
        game.selectsound.play()
        game.niveaucourant = "niveau_Oriane"
        game.scenecourante = "infoNiveau"
    if event.type == objects["param"].CLICKED:
        game.selectsound.play()
        game.scenecourante = "parametres"
    if event.type == objects["perso"].CLICKED:
        game.selectsound.play()
        game.scenecourante = "infoPerso"
    if (event.type == KEYDOWN and event.key == K_RIGHT) or (event.type == MOUSEBUTTONDOWN and objects["fleche2"].visible and game.displaylist["fleche2"].collidepoint(pygame.mouse.get_pos())):
        if 0 <= indexselection < len(listlevel)-1:
            indexselection += 1
            

            animselection = tweener.Tween(
                begin=camera[0],
                end=indexselection*643,
                duration=600,
                easing=tweener.Easing.CUBIC,
                easing_mode=tweener.EasingMode.OUT
            )
        animselection.start()
    if (event.type == KEYDOWN and event.key == K_LEFT) or (event.type == MOUSEBUTTONDOWN and objects["fleche1"].visible and game.displaylist["fleche1"].collidepoint(pygame.mouse.get_pos())):
        if 0 < indexselection <= len(listlevel)-1:
            indexselection -= 1
            if indexselection == 0:
                objects["fleche1"].visible = False
            else:
                objects["fleche1"].visible = True
        
            animselection = tweener.Tween(
                begin=camera[0],
                end=indexselection*643,
                duration=600,
                easing=tweener.Easing.CUBIC,
                easing_mode=tweener.EasingMode.OUT
            )
            animselection.start()
    """    
    if event.type == objects["niv2"].CLICKED:
        game.selectsound.play()
        game.niveaucourant = "niveau_Oriane"
        game.scenecourante = "infoNiveau"
    """

def loopbeforeupdate():
    global indexselection, listlevel, animselection
    if indexselection == 0:
        objects["fleche1"].visible = False
    else:
        objects["fleche1"].visible = True

    if indexselection == len(listlevel)-1:
        objects["fleche2"].visible = False
    else:
        objects["fleche2"].visible = True
    animselection.update()
    camera[0] = animselection.value

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["param"].activate(game.displaylist["param"])
    objects["perso"].activate(game.displaylist["perso"])
    # objects["niv2"].activate(game.displaylist["niv2"])