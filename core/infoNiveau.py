import pygame
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
import classes
import zipfile
import os
import io
import game
import shutil

import time

import copy

camera = [0, 0]

fond = (0, 0, 0)

objects = {}

calques = {}

hardcore = "0"
listphases = []

def init():
    global objects, calques, camera, fond, hardcore, listphases
    # Définition des objets
    objects.update({"fondInfoNiv" : classes.Actif(
            {"anim1" : [PurePath("images/fonds/fond_dessus_info_niveau.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "imageNiv" : classes.Actif(
        {"anim1" : [PurePath("images/fonds/fond_info_"+ game.niveaucourant + ".png")]},
        {"anim1" : [False, 5]},
        "anim1"
        ),
        "iconeFacile" : classes.Bouton(
            {"iconeF" :
        [
            [PurePath("images/interface/difficult_easy.png")],
            [PurePath("images/interface/difficult_easy.png")],
            [PurePath("images/interface/difficult_easy.png")],
            [PurePath("images/interface/difficult_easy.png")],
            [PurePath("images/interface/difficult_easy.png")]
        ]},
        {"iconeF" :[
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5]
        ]},
        "iconeF"
        ),
        "iconeMoyen" : classes.Bouton(
            {"iconeM" :
        [
            [PurePath("images/interface/difficult_normal.png")],
            [PurePath("images/interface/difficult_normal.png")],
            [PurePath("images/interface/difficult_normal.png")],
            [PurePath("images/interface/difficult_normal.png")],
            [PurePath("images/interface/difficult_normal.png")]
        ]},
        {"iconeM" :[
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5]
        ]},
        "iconeM"
        ),
        "iconeDur" : classes.Bouton(
            {"iconeDu" :
        [
            [PurePath("images/interface/difficult_hard.png")],
            [PurePath("images/interface/difficult_hard.png")],
            [PurePath("images/interface/difficult_hard.png")],
            [PurePath("images/interface/difficult_hard.png")],
            [PurePath("images/interface/difficult_hard.png")]
        ]},
        {"iconeDu" :[
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5]
        ]},
        "iconeDu"
        ),
        "iconeDemon" : classes.Bouton(
            {"iconeD" :
        [
            [PurePath("images/interface/difficult_hell.png")],
            [PurePath("images/interface/difficult_hell.png")],
            [PurePath("images/interface/difficult_hell.png")],
            [PurePath("images/interface/difficult_hell.png")],
            [PurePath("images/interface/difficult_hell.png")]
        ]},
        {"iconeD" :[
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5]
        ]},
        "iconeD"
        ),
        "jouer" : classes.Bouton(
            {"BoutonJouer" :
        [
            [PurePath("images/interface/BoutonJouer.png")],
            [PurePath("images/interface/BoutonJouer.png")],
            [PurePath("images/interface/BoutonJouer.png")],
            [PurePath("images/interface/BoutonJouer.png")],
            [PurePath("images/interface/BoutonJouer.png")]
        ]},
        {"BoutonJouer" :[
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5],
            [False, 0, 5]
        ]},
        "BoutonJouer"
        ),
        "retour" : classes.Bouton(
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
        ),
        "cube" : classes.Actif
            ({"anim1" : [PurePath("images/interface/cubeblanc.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "NomNiveau" : classes.Text(
            "Niveau Test",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            40,
            (255,255,255)
        ),
        "Scoremax1" : classes.Text(
            "Score max",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255,255,255)
        ),
        "NbScoremax1F" : classes.Text(
            "125000",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbScoremax1Dur" : classes.Text(
            "10000",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbScoremax1Demon" : classes.Text(
            "0",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "Combomax1" : classes.Text(
            "Combo max",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255,255,255)
        ),
        "NbCombomax1F" : classes.Text(
            "120",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbCombomax1Dur" : classes.Text(
            "100",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbCombomax1Demon" : classes.Text(
            "0",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "Scoremax2" : classes.Text(
            "Score max",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255,255,255)
        ),
        "NbScoremax2F" : classes.Text(
            "125000",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbScoremax2Dur" : classes.Text(
            "10000",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbScoremax2Demon" : classes.Text(
            "0",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "Combomax2" : classes.Text(
            "Combo max",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255,255,255)
        ),
        "NbCombomax2F" : classes.Text(
            "120",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbCombomax2Dur" : classes.Text(
            "100",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbCombomax2Demon" : classes.Text(
            "0",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "Scoremax3" : classes.Text(
            "Score max",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255,255,255)
        ),
        "NbScoremax3F" : classes.Text(
            "125000",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbScoremax3Dur" : classes.Text(
            "10000",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbScoremax3Demon" : classes.Text(
            "0",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "Combomax3" : classes.Text(
            "Combo max",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (255,255,255)
        ),
        "NbCombomax3F" : classes.Text(
            "120",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbCombomax3Dur" : classes.Text(
            "100",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        "NbCombomax3Demon" : classes.Text(
            "0",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            25,
            (236,52,22)
        ),
        #ronds de sélection
        "selectionFacile" : classes.Actif(
            {"anim1" : [PurePath("images/interface/rond_selection.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "selectionDur" : classes.Actif(
            {"anim1" : [PurePath("images/interface/rond_selection.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "selectionDemon" : classes.Actif(
            {"anim1" : [PurePath("images/interface/rond_selection.png")]},
            {"anim1" : [False, 5]},
            "anim1"
    )})
    # Placement des objets
    calques.update({
        
        0:{
            "imageNiv" : [0, 0]
        },
        1:{
            "fondInfoNiv" : [0, 270],
            "selectionFacile" : [18, 288],
            "selectionDur" : [148, 288],
            "selectionDemon" : [288, 288]

        },
        2:{
            #bloc phase 1
            "Scoremax1" : [600, 275], #+10
            "NbScoremax1F" : [780, 275],
            "NbScoremax1Dur" : [780, 275],
            "NbScoremax1Demon" : [780, 275],
            "Combomax1" : [600, 315], #+5
            "NbCombomax1F" : [780, 315],
            "NbCombomax1Dur" : [780, 315],
            "NbCombomax1Demon" : [780, 315],
            #bloc phase 2
            "Scoremax2" : [600, 376], #+10
            "NbScoremax2F" : [780, 376],
            "NbScoremax2Dur" : [780, 376],
            "NbScoremax2Demon" : [780, 376],
            "Combomax2" : [600, 416],
            "NbCombomax2F" : [780, 416],
            "NbCombomax2Dur" : [780, 416],
            "NbCombomax2Demon" : [780, 416],
            #bloc phase 3
            "Scoremax3" : [600, 477],
            "NbScoremax3F" : [780, 477],
            "NbScoremax3Dur" : [780, 477],
            "NbScoremax3Demon" : [780, 477],
            "Combomax3" : [600, 517],
            "NbCombomax3F" : [780, 517],
            "NbCombomax3Dur" : [780, 517],
            "NbCombomax3Demon" : [780, 517],
            #nom niveau
            "NomNiveau" : [110, 220]
        },
        3:{
            "jouer" : [85, 420],
            "retour" : [0, 0],
            "cube" : [890, 0]
        }
    })

    # Propriétés des objets
    objects["selectionDur"].visible = False
    objects["selectionDemon"].visible = False

    objects["Scoremax1"].visible = False
    objects["Scoremax2"].visible = False
    objects["Scoremax3"].visible = False
    objects["Combomax1"].visible = False
    objects["Combomax2"].visible = False
    objects["Combomax3"].visible = False

    objects["NbScoremax1F"].visible = False
    objects["NbScoremax1Dur"].visible = False
    objects["NbScoremax1Demon"].visible = False
    objects["NbCombomax1F"].visible = False
    objects["NbCombomax1Dur"].visible = False
    objects["NbCombomax1Demon"].visible = False

    objects["NbScoremax2F"].visible = False
    objects["NbScoremax2Dur"].visible = False
    objects["NbScoremax2Demon"].visible = False
    objects["NbCombomax2F"].visible = False
    objects["NbCombomax2Dur"].visible = False
    objects["NbCombomax2Demon"].visible = False

    objects["NbScoremax3F"].visible = False
    objects["NbScoremax3Dur"].visible = False
    objects["NbScoremax3Demon"].visible = False
    objects["NbCombomax3F"].visible = False
    objects["NbCombomax3Dur"].visible = False
    objects["NbCombomax3Demon"].visible = False

    print(game.niveaucourant)

    # Pour chaque fichier dans levelfiles
    for file in os.listdir("levelfiles"):
        # Détecter les fichiers asrg
        if game.niveaucourant in file and file.endswith(".asrg"):
            # Ouverture du fichier (zip)
            with zipfile.ZipFile(PurePath("levelfiles/" + file), "r") as filelevel:
                # Ouverture du fichier de configuration du niveau
                fileconfig = io.TextIOWrapper(filelevel.open(game.niveaucourant + ".config"))
                title = ""
                pathfont = ""
                # Pour chaque ligne du fichier de configuration
                for line in fileconfig:
                    # Titre du niveau
                    if "TITLE" in line:
                        title = line[:-1].split("\t")[1]
                    # Nom du fichier police à afficher dans infoNiveau
                    if "FICHIERPOLICE" in line:
                        pathfont = "fonts/"+line[:-1].split("\t")[1]
                    # Difficulté du niveau
                    if "HARDCORE" in line:
                        hardcore = line[:-1].split("\t")[1]
                        # Si hardcore est 0, les niveaux sont facile/normal/difficile
                        # Si hardcore est 1, les niveaux sont normal/difficile/extreme
                        if hardcore == "0":
                            calques[1]["iconeFacile"] = [30, 300]
                            calques[1]["iconeMoyen"] = [160, 300]
                            calques[1]["iconeDur"] = [300, 300]
                        if hardcore == "1":
                            calques[1]["iconeMoyen"] = [30, 300]
                            calques[1]["iconeDur"] = [160, 300]
                            calques[1]["iconeDemon"] = [300, 300]

                    # Phases du niveau
                    if "PHASES" in line:
                        listphases = line[:-1].split("\t")[1:]
                        # Si une phase est dans la liste, afficher l'icone et les score/combo
                        if "1" in listphases:
                            objects["phase1"] = classes.Actif(
                                {"anim1" : [PurePath("images/interface/icone_phase1.png")]},
                                {"anim1" : [False, 5]},
                                "anim1"
                                )
                            calques[1]["phase1"] = [530, 280]
                            objects["Scoremax1"].visible = True
                            objects["Combomax1"].visible = True
                            
                        if "2" in listphases:
                            objects["phase2"] = classes.Actif(
                                {"anim1" : [PurePath("images/interface/icone_phase2.png")]},
                                {"anim1" : [False, 5]},
                                "anim1"
                            )
                            calques[1]["phase2"] = [530, 381]
                            objects["Scoremax2"].visible = True
                            objects["Combomax2"].visible = True
                        if "3" in listphases:
                            objects["phase3"] = classes.Actif(
                                {"anim1" : [PurePath("images/interface/icone_phase3.png")]},
                                {"anim1" : [False, 5]},
                                "anim1"
                            )
                            calques[1]["phase3"] = [530, 482]
                            objects["Scoremax3"].visible = True
                            objects["Combomax3"].visible = True
                
                objects["NomNiveau"] = classes.Text(
                    title,
                    PurePath(pathfont),
                    40,
                    (255,255,255)
                )
                calques[2]["NomNiveau"] = [110, 220]

    # Mettre la liste des phases dans les variables globales
    game.listphases = listphases
    for phase in listphases:
            match phase:
                case "1":
                    objects["NbScoremax1F"].visible = True
                    objects["NbCombomax1F"].visible = True
                case "2":
                    objects["NbScoremax2F"].visible = True
                    objects["NbCombomax2F"].visible = True
                case "3":
                    objects["NbScoremax3F"].visible = True
                    objects["NbCombomax3F"].visible = True

    # Ouvrir le fichier de sauvegarde
    with open("save.asrg", "r") as filesave:
        titlelevel = ""
        # Pour chaque ligne, enregistrer les valeurs du niveau et les afficher au bon endroit
        for line in filesave:
            if "LEVELNAME" in line:
                titlelevel = line[:-1].split("\t")[1]
            if "SCORE_FACILE_PHASE1" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax1F"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_FACILE_PHASE1" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax1F"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_FACILE_PHASE2" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax2F"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_FACILE_PHASE2" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax2F"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_FACILE_PHASE3" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax3F"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_FACILE_PHASE3" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax3F"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_MOYEN_PHASE1" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax1Dur"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_MOYEN_PHASE1" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax1Dur"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_MOYEN_PHASE2" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax2Dur"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_MOYEN_PHASE2" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax2Dur"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_MOYEN_PHASE3" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax3Dur"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_MOYEN_PHASE3" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax3Dur"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_DIFFICILE_PHASE1" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax1Demon"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_DIFFICILE_PHASE1" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax1Demon"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_DIFFICILE_PHASE2" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax2Demon"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_DIFFICILE_PHASE2" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax2Demon"].changeTexte(line[:-1].split("\t")[1])
            if "SCORE_DIFFICILE_PHASE3" in line and titlelevel == game.niveaucourant.upper():
                objects["NbScoremax3Demon"].changeTexte(line[:-1].split("\t")[1])
            if "COMBO_DIFFICILE_PHASE3" in line and titlelevel == game.niveaucourant.upper():
                objects["NbCombomax3Demon"].changeTexte(line[:-1].split("\t")[1])

def loopevent(event):
    global pause, button, gameovertimer, camera, listphases

    # Pour chaque icone, lors du clic, afficher les stats correspondants du niveau et de la difficulté
    if event.type == objects["iconeFacile"].CLICKED:
        game.selectsound.play()
        game.niveaudifficulte = 0
        objects["selectionFacile"].visible = True
        objects["selectionDur"].visible = False
        objects["selectionDemon"].visible = False

        objects["NbScoremax1Dur"].visible = False
        objects["NbScoremax1Demon"].visible = False
        objects["NbCombomax1Dur"].visible = False
        objects["NbCombomax1Demon"].visible = False

        objects["NbScoremax2Dur"].visible = False
        objects["NbScoremax2Demon"].visible = False
        objects["NbCombomax2Dur"].visible = False
        objects["NbCombomax2Demon"].visible = False

        objects["NbScoremax3Dur"].visible = False
        objects["NbScoremax3Demon"].visible = False
        objects["NbCombomax3Dur"].visible = False
        objects["NbCombomax3Demon"].visible = False

        for phase in listphases:
            match phase:
                case "1":
                    objects["NbScoremax1F"].visible = True
                    objects["NbCombomax1F"].visible = True
                case "2":
                    objects["NbScoremax2F"].visible = True
                    objects["NbCombomax2F"].visible = True
                case "3":
                    objects["NbScoremax3F"].visible = True
                    objects["NbCombomax3F"].visible = True
        


    if event.type == objects["iconeMoyen"].CLICKED:
        game.selectsound.play()
        
        if hardcore == "1":
            game.niveaudifficulte = 0
            objects["selectionFacile"].visible = True
            objects["selectionDur"].visible = False
            objects["selectionDemon"].visible = False

            objects["NbScoremax1Dur"].visible = False
            objects["NbScoremax1Demon"].visible = False
            objects["NbCombomax1Dur"].visible = False
            objects["NbCombomax1Demon"].visible = False

            objects["NbScoremax2Dur"].visible = False
            objects["NbScoremax2Demon"].visible = False
            objects["NbCombomax2Dur"].visible = False
            objects["NbCombomax2Demon"].visible = False

            objects["NbScoremax3Dur"].visible = False
            objects["NbScoremax3Demon"].visible = False
            objects["NbCombomax3Dur"].visible = False
            objects["NbCombomax3Demon"].visible = False

            for phase in listphases:
                match phase:
                    case "1":
                        objects["NbScoremax1F"].visible = True
                        objects["NbCombomax1F"].visible = True
                    case "2":
                        objects["NbScoremax2F"].visible = True
                        objects["NbCombomax2F"].visible = True
                    case "3":
                        objects["NbScoremax3F"].visible = True
                        objects["NbCombomax3F"].visible = True

        if hardcore == "0":
            game.niveaudifficulte = 1
            objects["selectionDur"].visible = True
            objects["selectionFacile"].visible = False
            objects["selectionDemon"].visible = False

            objects["NbScoremax1Demon"].visible = False
            objects["NbScoremax1F"].visible = False
            objects["NbCombomax1Demon"].visible = False
            objects["NbCombomax1F"].visible = False

            objects["NbScoremax2Demon"].visible = False
            objects["NbScoremax2F"].visible = False
            objects["NbCombomax2Demon"].visible = False
            objects["NbCombomax2F"].visible = False

            objects["NbScoremax3Demon"].visible = False
            objects["NbScoremax3F"].visible = False
            objects["NbCombomax3Demon"].visible = False
            objects["NbCombomax3F"].visible = False

            for phase in listphases:
                match phase:
                    case "1":
                        objects["NbScoremax1Dur"].visible = True
                        objects["NbCombomax1Dur"].visible = True
                    case "2":
                        objects["NbScoremax2Dur"].visible = True
                        objects["NbCombomax2Dur"].visible = True
                    case "3":
                        objects["NbScoremax3Dur"].visible = True
                        objects["NbCombomax3Dur"].visible = True

    if event.type == objects["iconeDur"].CLICKED:
        game.selectsound.play()
        if hardcore == "1":
            game.niveaudifficulte = 1
            objects["selectionDur"].visible = True
            objects["selectionFacile"].visible = False
            objects["selectionDemon"].visible = False

            objects["NbScoremax1Demon"].visible = False
            objects["NbScoremax1F"].visible = False
            objects["NbCombomax1Demon"].visible = False
            objects["NbCombomax1F"].visible = False

            objects["NbScoremax2Demon"].visible = False
            objects["NbScoremax2F"].visible = False
            objects["NbCombomax2Demon"].visible = False
            objects["NbCombomax2F"].visible = False

            objects["NbScoremax3Demon"].visible = False
            objects["NbScoremax3F"].visible = False
            objects["NbCombomax3Demon"].visible = False
            objects["NbCombomax3F"].visible = False

            for phase in listphases:
                match phase:
                    case "1":
                        objects["NbScoremax1Dur"].visible = True
                        objects["NbCombomax1Dur"].visible = True
                    case "2":
                        objects["NbScoremax2Dur"].visible = True
                        objects["NbCombomax2Dur"].visible = True
                    case "3":
                        objects["NbScoremax3Dur"].visible = True
                        objects["NbCombomax3Dur"].visible = True

        if hardcore == "0":
            game.niveaudifficulte = 2
            objects["selectionDemon"].visible = True
            objects["selectionFacile"].visible = False
            objects["selectionDur"].visible = False

            objects["NbScoremax1Dur"].visible = False
            objects["NbScoremax1F"].visible = False
            objects["NbCombomax1Dur"].visible = False
            objects["NbCombomax1F"].visible = False

            objects["NbScoremax2Dur"].visible = False
            objects["NbScoremax2F"].visible = False
            objects["NbCombomax2Dur"].visible = False
            objects["NbCombomax2F"].visible = False

            objects["NbScoremax3Dur"].visible = False
            objects["NbScoremax3F"].visible = False
            objects["NbCombomax3Dur"].visible = False
            objects["NbCombomax3F"].visible = False

            for phase in listphases:
                match phase:
                    case "1":
                        objects["NbScoremax1Demon"].visible = True
                        objects["NbCombomax1Demon"].visible = True
                    case "2":
                        objects["NbScoremax2Demon"].visible = True
                        objects["NbCombomax2Demon"].visible = True
                    case "3":
                        objects["NbScoremax3Demon"].visible = True
                        objects["NbCombomax3Demon"].visible = True

    if event.type == objects["iconeDemon"].CLICKED:
        game.selectsound.play()
        game.niveaudifficulte = 2
        objects["selectionDemon"].visible = True
        objects["selectionFacile"].visible = False
        objects["selectionDur"].visible = False

        objects["NbScoremax1Dur"].visible = False
        objects["NbScoremax1F"].visible = False
        objects["NbCombomax1Dur"].visible = False
        objects["NbCombomax1F"].visible = False

        objects["NbScoremax2Dur"].visible = False
        objects["NbScoremax2F"].visible = False
        objects["NbCombomax2Dur"].visible = False
        objects["NbCombomax2F"].visible = False

        objects["NbScoremax3Dur"].visible = False
        objects["NbScoremax3F"].visible = False
        objects["NbCombomax3Dur"].visible = False
        objects["NbCombomax3F"].visible = False

        for phase in listphases:
            match phase:
                case "1":
                    objects["NbScoremax1Demon"].visible = True
                    objects["NbCombomax1Demon"].visible = True
                case "2":
                    objects["NbScoremax2Demon"].visible = True
                    objects["NbCombomax2Demon"].visible = True
                case "3":
                    objects["NbScoremax3Demon"].visible = True
                    objects["NbCombomax3Demon"].visible = True

    # Clic sur le bouton jouer
    if event.type == objects["jouer"].CLICKED:
        # Si le dossier level existe
        if os.path.exists("level"):
            # Le supprimer
            shutil.rmtree("level")
        pygame.mixer.music.unload()
        game.selectsound.play()
        # Mettre le niveau courant dans les valeurs globales
        classes.imageniveau = game.niveaucourant
        game.scenecourante = "scene1"
        camera = [0, 0]

    if event.type == objects["retour"].CLICKED:
        pygame.mixer.music.unload()
        game.selectsound.play()
        game.scenecourante = "selectionniveau"
        
    

def loopbeforeupdate():
    pass

def loopafterupdate():
     global pause, button, gameovertimer, camera
     # Activation des boutons
     objects["jouer"].activate(game.displaylist["jouer"])
     objects["retour"].activate(game.displaylist["retour"])
     if "iconeFacile" in calques[1]:
        objects["iconeFacile"].activate(game.displaylist["iconeFacile"])
     if "iconeMoyen" in calques[1]:
        objects["iconeMoyen"].activate(game.displaylist["iconeMoyen"])
     if "iconeDur" in calques[1]:
        objects["iconeDur"].activate(game.displaylist["iconeDur"])
     if "iconeDemon" in calques[1]:
        objects["iconeDemon"].activate(game.displaylist["iconeDemon"])