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

objects = {}

calques = {}

def init():
    global objects, calques, camera, fond
    if not objects:
        objects.update({"fond_infoPersoG" : Actif(
            {"anim1" : [PurePath("images/fonds/animation/ecran_info_perso_gauche/" + format(i, '05d') + ".jpg") for i in range(125)]},
            {"anim1" : [True, 1]},
            "anim1"
            ),
            "fond_infoPersoD" : Actif(
            {"anim1" : [PurePath("images/fonds/animation/ecran_info_perso_droit/" + format(i, '05d') + ".jpg") for i in range(125)]},
            {"anim1" : [True, 1]},
            "anim1"
            ),
            "textnbNiveaux" : Text(
                "Nombre de niveaux débloqués :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "progression" : Text(
                "Progression du jeu :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "textprogFacile" : Text(
                "Facile :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "progFacile" : Text(
                "25%",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "textprogNormal" : Text(
                "Normal :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "progNormal" : Text(
                "25%",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "textprogDiff" : Text(
                "Difficile :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "progDiff" : Text(
                "0%",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "textprogExtrem" : Text(
                "Extrême :",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "progExtrem" : Text(
                "0%",
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                25,
                (255, 255, 255)
            ),
            "cadre" : Actif(
            {"anim1" : [PurePath("images/interface/cadre_info_perso.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "jaugeRouge" : Actif(
            {"anim1" : [PurePath("images/interface/bandeau_info_perso.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "jaugeBleue" : Actif(
            {"anim1" : [PurePath("images/interface/jauge_info_perso.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "niveau" : Text(
                "Niv. " + str(game.niveauglobal),
                PurePath("fonts/LTSaeada-SemiBold.otf"),
                20,
                (255, 255, 255)
            ),
            "perso" : Actif(
            {"anim1" : [PurePath("images/level/personnage_info_perso.png")]},
            {"anim1" : [False, 5]},
            "anim1"
            ),
            "retour" : Bouton(
                {"flecheRetour" :
            [
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")]
            ]},
            {"flecheRetour" :[
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "flecheRetour"
            )
        })
    calques.update({
        0:{
            "fond_infoPersoG" : [0, 0],
            "fond_infoPersoD" : [635, 0]
        },
        1:{
            "textnbNiveaux" : [60, 100],
            "progression" : [60, 175],
            "textprogFacile" : [120, 250],
            "textprogNormal" : [120, 325],
            "textprogDiff" : [120, 400],
            "textprogExtrem" : [120, 475],
            "cadre" : [163, 0]
        },
        2:{
            "jaugeBleue" : [173, 10]
        },
        3:{
            "jaugeRouge" : [173, 10]
        },
        4:{
            "niveau" : [290, 15],
            "retour" : [0, 0],
            "perso" : [710, 33]
        }})
    objects["jaugeRouge"].taillex = game.scoreglobal / (100000*(game.niveauglobal+1))

    
    # Ouverture du fichier de sauvegarde
    with open("save.asrg", "r") as filesave:
        nbniveaudeb = 0
        nbniveaumoy = 0
        nbniveaudif = 0
        nbniveauext = 0
        hardcore = 0

        for line in filesave:
            if "LEVELNAME" in line:
                if line[:-1].split("\t")[1] == "ALPHELIA":
                    hardcore = 0
                else:
                    hardcore = 1
            if "DONEFACILE" in line and int(line[:-1].split("\t")[1]) > 0:
                if hardcore == 0:
                    nbniveaudeb += 1
                else:
                    nbniveaumoy += 1
                
            if "DONEMOYEN" in line and int(line[:-1].split("\t")[1]) > 0:
                if hardcore == 0:
                    nbniveaumoy += 1
                else:
                    nbniveaudif += 1

            if "DONEDIFFICILE" in line and int(line[:-1].split("\t")[1]) > 0:
                if hardcore == 0:
                    nbniveaudif += 1
                else:
                    nbniveauext += 1

        
        objects["NbNiveaux"] = Text(
            str(nbniveaudeb + nbniveaumoy + nbniveaudif + nbniveauext) + "/12",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255, 255, 255)
        )
        objects["progFacile"] = Text(
            str(int(nbniveaudeb*100)) + "%",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255, 255, 255)
        )
        objects["progMoyen"] = Text(
            str(int(nbniveaumoy*100/4)) + "%",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255, 255, 255)
        )
        objects["progDiff"] = Text(
            str(int(nbniveaudif*100/4)) + "%",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255, 255, 255)
        )
        objects["progDemon"] = Text(
            str(int(nbniveauext*100/3)) + "%",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255, 255, 255)
        )
        calques[1]["NbNiveaux"] = [470, 100]
        calques[1]["progFacile"] = [250, 250]
        calques[1]["progMoyen"] = [250, 325]
        calques[1]["progDiff"] = [250, 400]
        calques[1]["progDemon"] = [250, 475]

    pygame.mixer.music.load(PurePath("music/intheembraceofdarkness.mp3"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(game.volume)


def loopevent(event):
    global pause, button, gameovertimer, camera
    if event.type == objects["retour"].CLICKED:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        game.scenecourante = "selectionniveau"
        
    

def loopbeforeupdate():
    pass

def loopafterupdate():
     global pause, button, gameovertimer, camera
     objects["retour"].activate(game.displaylist["retour"])