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

victoiresound = pygame.mixer.Sound(PurePath("music/victoire.wav"))

# valeurs de scenes

calques = {}

def init():
    global objects, calques, camera, fond, victoiresound
    # Décharger une musique s'il y a
    pygame.mixer.music.unload()
    # Définition des objets
    objects.update({"fondvicperso" : Actif(
        {"anim1" : [PurePath("images/fonds/animation/ecran_victoire_droit/" + format(i, '05d') + ".jpg") for i in range(125)]},
        {"anim1" : [True, 1]},
        "anim1"
    ),
    "cadrescore" : Actif(
        {"anim1" : [PurePath("images/interface/cadre_score_V.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "scoregen" : Text(
        "Score Général : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "nbscoregen" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        19,
        (0, 0, 0)
    ),
    "combogen" : Text(
        "Combo Général : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "nbcombogen" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "nbpourcentgen" : Text(
        "0%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (0, 0, 0)
    ),
    "fondvic" : Actif(
        {"anim1" : [PurePath("images/fonds/animation/ecran_victoire_gauche/" + format(i, '05d') + ".png") for i in range(30)]},
        {"anim1" : [False, 1]},
        "anim1"
    ),
    "quitter" : Bouton( {"quitter" :
    [
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")],
        [PurePath("images/interface/flecheretour.png")]
    ]},
    {"quitter" :[
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ]},
    "quitter"),
    "rejouer" : Bouton( {"rejouer" :
    [
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")],
        [PurePath("images/interface/Fleche_Recommencer.png")]
    ]},
    {"rejouer" :[
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ]},
    "rejouer"),
    "phase1" : Actif(
        {"anim1" : [PurePath("images/interface/phase1.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "nbpourcent1" : Text(
        "0%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "Scorevic1" : Text(
        "Score : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "numscore1" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        25,
        (254, 95, 83)
    ),
    "miss1" : Text(
        "Miss : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numiss1" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "great1" : Text(
        "Great : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numgreat1" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "perfect1" : Text(
        "Perfect : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numperfect1" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "combo1" : Text(
        "Combo Max : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numcombo1" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (254, 95, 83)
    ),
    "phase2" : Actif(
        {"anim1" : [PurePath("images/interface/phase2.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "nbpourcent2" : Text(
        "0%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "Scorevic2" : Text(
        "Score : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "numscore2" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        25,
        (84, 185, 255)
    ),
    "miss2" : Text(
        "Miss : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numiss2" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "great2" : Text(
        "Great : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numgreat2" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "perfect2" : Text(
        "Perfect : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numperfect2" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "pass2" : Text(
        "Pass : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numpass2" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "combo2" : Text(
        "Combo Max : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numcombo2" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (84, 185, 255)
    ),
    "phase3" : Actif(
        {"anim1" : [PurePath("images/interface/phase3.png")]},
        {"anim1" : [False, 5]},
        "anim1"
    ),
    "nbpourcent3" : Text(
        "0%",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "Scorevic3" : Text(
        "Score : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        30,
        (255, 255, 255)
    ),
    "numscore3" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        25,
        (246, 240, 119)
    ),
    "miss3" : Text(
        "Miss : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numiss3" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (246, 240, 119)
    ),
    "pass3" : Text(
        "Pass : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numpass3" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (246, 240, 119)
    ),
    "combo3" : Text(
        "Combo Max : ",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (255, 255, 255)
    ),
    "numcombo3" : Text(
        "0",
        PurePath("fonts/LTSaeada-SemiBold.otf"),
        20,
        (246, 240, 119)
    ),
    "pers" : Actif(
        {"debout" : [PurePath("images/level/personnage.png")]},
        {"debout" : [True, 5]}, #Au hazard
        "debout"
    )})
    # Placement des objets
    calques.update({
        0:{
            "fondvicperso" : [635, 0],
            "fondvic" : [0, 0]
        },
        1:{
            "quitter" : [0, 0],
            "rejouer" : [565, 0],
            "cadrescore" : [677, 0],
            "phase1" : [10, 90],
            "phase2" : [10, 254],
            "phase3" : [10, 418],
            "pers" : [752, 213]
        },
        2:{
            "scoregen" : [687, 15],
            "nbscoregen" : [834, 16],
            "combogen" : [687, 55],
            "nbcombogen" : [846, 56],
            "nbpourcentgen" : [778, 95]
        },
        3:{
            "Scorevic1" : [124, 96],
            "numscore1" : [224, 101],
            "nbpourcent1" : [533, 96],
            "miss1" : [144, 129],
            "numiss1" : [197, 130],
            "great1" : [313, 129],
            "numgreat1" : [382, 130],
            "perfect1" : [484, 129],
            "numperfect1" : [567, 130],
            "combo1" : [268, 154],
            "numcombo1" : [391, 155],

            "Scorevic2" : [124, 259],
            "numscore2" : [224, 264],
            "nbpourcent2" : [533, 259],
            "miss2" : [144, 293],
            "numiss2" : [197, 294],
            "great2" : [313, 293],
            "numgreat2" : [382, 294],
            "perfect2" : [484, 293],
            "numperfect2" : [567, 294],
            "pass2" : [232, 319],
            "numpass2" : [289, 319],
            "combo2" : [407, 319],
            "numcombo2" : [530, 320],

            "Scorevic3" : [124, 423],
            "numscore3" : [224, 428],
            "nbpourcent3" : [533, 423],#[595-(objects["nbpourcent3"].renderText().get_rect().width), 30+490-(objects["phase3"].sprites["anim1"][0].get_rect().height)],
            "miss3" : [144, 456],
            "numiss3" : [197, 457],
            "pass3" : [144, 481],
            "numpass3" : [201, 482],
            "combo3" : [268, 481],
            "numcombo3" : [391, 482]
        }})

    # Propriétés des objets
    objects["scoregen"].color_shadow = (180, 180, 180)
    objects["nbscoregen"].color_shadow = (180, 180, 180)
    objects["combogen"].color_shadow = (180, 180, 180)
    objects["nbcombogen"].color_shadow = (180, 180, 180)
    objects["nbpourcentgen"].color_shadow = (180, 180, 180)

    # Pour chaque objet, si c'est un objet appartenant à une phase, on commence par tous les mettre en non-visible
    for objet in objects:
        if objet[-1] == "1" or objet[-1] == "2" or objet[-1] == "3":
            objects[objet].visible = False

    pourcentglobal = 0

    # On met le score et le combo venant des valeurs globales
    objects["nbscoregen"].text = str(game.stats_perso["score"])
    objects["nbcombogen"].text = str(game.stats_perso["comboglobal"])

    print(game.listphases)

    # Si y'a une phase (1, 2 ou 3) dans la liste des phases
    if "1" in game.listphases:
        # Afficher les objets correspondants
        for objet in objects:
            if objet[-1] == "1":
                objects[objet].visible = True
        
        # Définir les textes
        objects["numscore1"].text = str(game.stats_perso["scorephase1"])
        objects["nbpourcent1"].text = str(int((game.stats_perso["perfectphase1"]/game.stats_perso["nbitems1"] + game.stats_perso["greatphase1"]*0.7/game.stats_perso["nbitems1"])*100)) + "%"
        pourcentglobal += int((game.stats_perso["perfectphase1"]/game.stats_perso["nbitems1"] + game.stats_perso["greatphase1"]*0.7/game.stats_perso["nbitems1"])*100)
        objects["numiss1"].text = str(game.stats_perso["missphase1"])
        objects["numgreat1"].text = str(game.stats_perso["greatphase1"])
        objects["numperfect1"].text = str(game.stats_perso["perfectphase1"])
        objects["numcombo1"].text = str(game.stats_perso["combophase1"])
    
    if "2" in game.listphases:
        for objet in objects:
            if objet[-1] == "2":
                objects[objet].visible = True
        objects["numscore2"].text = str(game.stats_perso["scorephase2"])
        objects["nbpourcent2"].text = str(int((game.stats_perso["perfectphase2"]/game.stats_perso["nbitems2"] + game.stats_perso["greatphase2"]*0.7/game.stats_perso["nbitems2"])*100)) + "%"
        pourcentglobal += int((game.stats_perso["perfectphase2"]/game.stats_perso["nbitems2"] + game.stats_perso["greatphase2"]*0.7/game.stats_perso["nbitems2"])*100)
        objects["numiss2"].text = str(game.stats_perso["missphase2"])
        objects["numgreat2"].text = str(game.stats_perso["greatphase2"])
        objects["numperfect2"].text = str(game.stats_perso["perfectphase2"])
        objects["numpass2"].text = str(game.stats_perso["passphase2"])
        objects["numcombo2"].text = str(game.stats_perso["combophase2"])
    
    if "3" in game.listphases:
        for objet in objects:
            if objet[-1] == "3":
                objects[objet].visible = True
        objects["numscore3"].text = str(game.stats_perso["scorephase3"])
        if game.stats_perso["notesphase3"] == 0 and game.stats_perso["missphase3"] == 0:
            objects["nbpourcent3"].text = "0%"
        else:
            objects["nbpourcent3"].text = str(int((game.stats_perso["notesphase3"]/(game.stats_perso["notesphase3"]+game.stats_perso["missphase3"]))*100))+"%"
            print(game.stats_perso["notesphase3"], game.stats_perso["missphase3"], int((game.stats_perso["notesphase3"]/(game.stats_perso["notesphase3"]+game.stats_perso["missphase3"]))*100))
            pourcentglobal += int((game.stats_perso["notesphase3"]/(game.stats_perso["notesphase3"]+game.stats_perso["missphase3"]))*100)
        objects["numiss3"].text = str(game.stats_perso["missphase3"])
        objects["numpass3"].text = str(game.stats_perso["notesphase3"])
    objects["nbpourcentgen"].text = str(int(pourcentglobal / len(game.listphases))) + "%"


    # Enregistrement des points dans le fichier de sauvegarde
    filelines = []
    with open("save.asrg", "r") as filesave:
        filelines = filesave.readlines()

    titlelevel = ""
    done = 0
    for index, line in enumerate(filelines):
        if "SCOREGLOBAL" in line and int(line[:-1].split("\t")[1]) > game.stats_perso["score"]:
            filelines[index] = "SCOREGLOBAL\t"+str(game.stats_perso["score"])+"\n"
        if "LEVELNAME" in line:
            titlelevel = line[:-1].split("\t")[1]
            print(titlelevel, game.niveaucourant, game.niveaudifficulte)
        if "DONE" in line and titlelevel.lower() == game.niveaucourant:
            if "FACILE" in line and game.niveaudifficulte == 0 and line[:-1].split("\t")[1] != "1":
                filelines[index] = "DONEFACILE\t1\n"
            if "MOYEN" in line and game.niveaudifficulte == 1 and line[:-1].split("\t")[1] != "1":
                filelines[index] = "DONEMOYEN\t1\n"
            if "DIFFICILE" in line and game.niveaudifficulte == 2 and line[:-1].split("\t")[1] != "1":
                filelines[index] = "DONEDIFFICILE\t1\n"
        for line in filelines:
            titlelevel2 = ""
            if "LEVELNAME" in line:
                titlelevel2 = line[:-1].split("\t")[1]
            if "DONE" in line and titlelevel2.lower() == game.niveaucourant and line[:-1].split("\t")[1] == "1":
                done+=1
                print(done)
        if "PROGRESSION" in line and titlelevel.lower() == game.niveaucourant:
            progress = int(done/3*100)
            filelines[index] = "PROGRESSION\t" + str(progress) + "\n"
        if "SCORE" in line and titlelevel.lower() == game.niveaucourant:
            if "FACILE" in line and game.niveaudifficulte == 0:
                if "PHASE1" in line and "1" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase1"]:
                    filelines[index] = "SCORE_FACILE_PHASE1\t" + str(game.stats_perso["scorephase1"]) + "\n"
                if "PHASE2" in line and "2" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase2"]:
                    filelines[index] = "SCORE_FACILE_PHASE2\t" + str(game.stats_perso["scorephase2"]) + "\n"
                if "PHASE3" in line and "3" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase3"]:
                    filelines[index] = "SCORE_FACILE_PHASE3\t" + str(game.stats_perso["scorephase3"]) + "\n"
            if "MOYEN" in line and game.niveaudifficulte == 1:
                if "PHASE1" in line and "1" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase1"]:
                    filelines[index] = "SCORE_MOYEN_PHASE1\t" + str(game.stats_perso["scorephase1"]) + "\n"
                if "PHASE2" in line and "2" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase2"]:
                    filelines[index] = "SCORE_MOYEN_PHASE2\t" + str(game.stats_perso["scorephase2"]) + "\n"
                if "PHASE3" in line and "3" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase3"]:
                    filelines[index] = "SCORE_MOYEN_PHASE3\t" + str(game.stats_perso["scorephase3"]) + "\n"
            if "DIFFICILE" in line and game.niveaudifficulte == 2:
                if "PHASE1" in line and "1" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase1"]:
                    filelines[index] = "SCORE_DIFFICILE_PHASE1\t" + str(game.stats_perso["scorephase1"]) + "\n"
                if "PHASE2" in line and "2" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase2"]:
                    filelines[index] = "SCORE_DIFFICILE_PHASE1\t" + str(game.stats_perso["scorephase2"]) + "\n"
                if "PHASE3" in line and "3" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["scorephase3"]:
                    filelines[index] = "SCORE_DIFFICILE_PHASE1\t" + str(game.stats_perso["scorephase3"]) + "\n"
        if "COMBO" in line and titlelevel.lower() == game.niveaucourant:
            if "FACILE" in line and game.niveaudifficulte == 0:
                if "PHASE1" in line and "1" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["combophase1"]:
                    filelines[index] = "COMBO_FACILE_PHASE1\t" + str(game.stats_perso["combophase1"]) + "\n"
                if "PHASE2" in line and "2" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["combophase2"]:
                    filelines[index] = "COMBO_FACILE_PHASE2\t" + str(game.stats_perso["combophase2"]) + "\n"
                if "PHASE3" in line and "3" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["notesphase3"]:
                    filelines[index] = "COMBO_FACILE_PHASE3\t" + str(game.stats_perso["notesphase3"]) + "\n"
            if "MOYEN" in line and game.niveaudifficulte == 1:
                if "PHASE1" in line and "1" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["combophase1"]:
                    filelines[index] = "COMBO_MOYEN_PHASE1\t" + str(game.stats_perso["combophase1"]) + "\n"
                if "PHASE2" in line and "2" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["combophase2"]:
                    filelines[index] = "COMBO_MOYEN_PHASE2\t" + str(game.stats_perso["combophase2"]) + "\n"
                if "PHASE3" in line and "3" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["notesphase3"]:
                    filelines[index] = "COMBO_MOYEN_PHASE3\t" + str(game.stats_perso["notesphase3"]) + "\n"
            if "DIFFICILE" in line and game.niveaudifficulte == 2:
                if "PHASE1" in line and "1" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["combophase1"]:
                    filelines[index] = "COMBO_DIFFICILE_PHASE1\t" + str(game.stats_perso["combophase1"]) + "\n"
                if "PHASE2" in line and "2" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["combophase2"]:
                    filelines[index] = "COMBO_DIFFICILE_PHASE1\t" + str(game.stats_perso["combophase2"]) + "\n"
                if "PHASE3" in line and "3" in game.listphases and int(line[:-1].split("\t")[1]) < game.stats_perso["notesphase3"]:
                    filelines[index] = "COMBO_DIFFICILE_PHASE1\t" + str(game.stats_perso["notesphase3"]) + "\n"

    # Ecrire sur le fichier
    with open("save.asrg", "w") as filesave:
        filesave.writelines(filelines)

    victoiresound.play(loops=-1)
    

            


def loopevent(event):
    global pause, button, gameovertimer, camera, victoiresound
    if event.type == objects["rejouer"].CLICKED:
        victoiresound.stop()
        game.selectsound.play()
        game.scenecourante = "scene1"
        camera = [0, 0]
    if event.type == objects["quitter"].CLICKED:
        victoiresound.stop()
        game.selectsound.play()
        game.scenecourante = "selectionniveau"
    

def loopbeforeupdate():
    pass

def loopafterupdate():
    global pause, button, gameovertimer, camera
    objects["rejouer"].activate(game.displaylist["rejouer"])
    objects["quitter"].activate(game.displaylist["quitter"])