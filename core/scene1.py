import pygame
#from pygame_geometry.curves import BezierCurve
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *
import createcube
import os
import io
import game
import zipfile

import time

import copy

# Variables de scènes

# Statistiques des persos
stats_perso = {
    "score" : 0,
    "pv" : 200,
    "compteurcomboglobal" : 0,
    "comboglobal" : 0,

    "scorephase1": 0,
    "scorephase2": 0,
    "scorephase3": 0,

    "precisionphase1" : 0,
    "precisionphase2" : 0,
    "precisionphase3" : 0,

    "compteurcombophase1" : 0,
    "compteurcombophase2" : 0,
    "combophase1" : 0,
    "combophase2" : 0,

    "compteurtempsphase3" : 0,
    "tempsphase3" : 0,

    "notesphase1" : 0,
    "notesphase3" : 0,

    "missphase1" : 0,
    "missphase2" : 0,
    "missphase3" : 0,

    "greatphase1" : 0,
    "greatphase2" : 0,
    
    "perfectphase1" : 0,
    "perfectphase2" : 0,

    "passphase2" : 0,

    "inLongUp" : False,
    "inLongDown" : False,
    "tempsUp" : "",
    "tempsDown" : "",

    "nbitems1" : 0,
    "nbitems2" : 0
}

# Position de la caméra de scène
camera = [0, 0]
# Nombre de pixels par secondes auxquels la caméra se déplace sur X
vitessecam = 600

# Couleur de fond de la scène
fond = (0, 0, 0)

# Position du perso de la phase 1 : 0 pour haut, 1 pour bas
pos_pers = 1

#True si un boss long est en cours
longboss = False

#True si un long d'une phase 2 est en cours
longphase2 = False

# Booléen qui pause le jeu si True
pause = False
# Quand True, active le gameover et lance le timer avant l'affichage de la scène gameover
gameoverbool = False
# Enregistre le temps de l'ordinateur à laquelle le gameoverbool s'est activée et sert à tester si 2 secondes sont passés
gameovertimer = 0

# Pendant la création des objets, sert à activer le code pour créer les images liées
flagliee = False
# True si parmi les objets liées, ce n'est pas la première note liée (crée donc une ligne de liée)
autreliee = False
# Enregistre la position d'une note liée pour le premier sommet de la ligne liée
positionliee = [0, 0]
# Pendant la création des objets, l'intervalle courant où l'on applique les notes liées
intervallecourant = [0, 0]

# Index de la phase courante
phaseindex = 0
# Index du thème courant
themeindex = 0

# Propriétés du personnage de la phase 3
perso_phase3 = {
    "jumpCount" : 0,
    "isJump" : False,
    "reverse" : False,
    "dash" : False,
    "objectdash" : "",
    "posydash" : 0
}

# Initialisation des listes des collisions pendant la phase 3
collidephase3 = []
collidemortphase3 = []
collideorbephase3 = []
collidepiquephase3 = []
collidegroundphase3 = []

# Liste des parallax
parallax1 = []
parallax2 = []
parallax3 = []
parallax4 = []

# Initialisation des dictionnaires objets, calques et levelelements

objects = {}

calques = {}

levelelements = {}

# Nom du niveau à charger
nomniveau = ""

# Fonctions de scènes pour créer et placer les objets des éléments
# temps en milisecondes
# Positionner l'objet sur le x --> temps/1000 * vitessecam + position x sur l'écran où l'élement sera au temps de la musique donnée
def creerCoeur(temps, posy):
    objects["coeur"+str(temps)] = Actif(
        {"anim1" : [PurePath("level/elements/coeur/" + image) for image in os.listdir(PurePath("level/elements/coeur/"))]},
        {"anim1" : [True, 1]},
        "anim1",
        tags=["element", "itemcoeur"]
    )
    calques["items"]["coeur"+str(temps)] = [(temps * vitessecam / 1000) + 150, posy]
    
def creerNote(temps, posy) :
    objects["note"+str(temps)] = Actif(
        {"anim1" : [PurePath("level/elements/note/" + image) for image in os.listdir(PurePath("level/elements/note/"))]},
        {"anim1" : [True, 1]},
        "anim1",
        tags=["element", "itemnote"]
    )
    calques["items"]["note"+str(temps)] = [(temps * vitessecam / 1000) + 150, posy]

def creerSmall(temps, placement) :
    global stats_perso
    # placement - up : en haut, down : en bas
    if placement == "up":
        objects["smallu"+str(temps)] = Actif(
        {
            key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/small"))], [[PurePath("level/elements/small/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/small/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/small"))]])
        },
        {
            key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/small"))]
        },
        "idle",
        tags=["enemy", "elementup", "small", str(temps)]
        )
        calques[3]["smallu"+str(temps)] = [(temps * vitessecam / 1000) + 150, 187 - objects["smallu"+str(temps)].sprites["idle"][0].get_height() / 2]
        stats_perso["nbitems1"] += 1
        # si sur le même temps, il y a un small en bas, créer un double
        if temps in levelelements["small"]['down']:
            objects["double"+str(temps)] = Actif(
            {"anim1" : [PurePath("level/elements/double/" + image) for image in os.listdir(PurePath("level/elements/double/"))]},
            {"anim1" : [True, 1]},
            "anim1",
            tags=["element", "double", str(temps)]
            )
            calques[3]["double"+str(temps)] = [(temps * vitessecam / 1000) + 150, 210]
    elif placement == "down":
        objects["smalld"+str(temps)] = Actif(
        {
            key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/small"))], [[PurePath("level/elements/small/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/small/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/small"))]])
        },
        {
            key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/small"))]
        },
        "idle",
        tags=["enemy", "elementdown", "small", str(temps)]
        )
        calques[3]["smalld"+str(temps)] = [(temps * vitessecam / 1000) + 150, 367 - objects["smalld"+str(temps)].sprites["idle"][0].get_height() / 2]
        stats_perso["nbitems1"] += 1

def creerLarge(temps, placement) :
    global stats_perso
    # placement - up : en haut, down : en bas
    if placement == "up":
        objects["largeu"+str(temps)] = Actif(
        {
            key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/large"))], [[PurePath("level/elements/large/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/large/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/large"))]])
        },
        {
            key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/large"))]
        },
        "idle",
        tags=["enemy", "elementup", "large", str(temps)]
        )
        calques[3]["largeu"+str(temps)] = [(temps * vitessecam / 1000) + 150, 187 - objects["largeu"+str(temps)].sprites["idle"][0].get_height() / 2]
        stats_perso["nbitems1"] += 1
        # si sur le même temps, il y a un large en bas, créer un double
        if temps in levelelements["large"]['down']:
            objects["double"+str(temps)] = Actif(
            {"anim1" : [PurePath("level/elements/double/" + image) for image in os.listdir(PurePath("level/elements/double/"))]},
            {"anim1" : [True, 1]},
            "anim1",
            tags=["element", "double", str(temps)]
            )
            calques[3]["double"+str(temps)] = [(temps * vitessecam / 1000) + 150, 210]
    if placement == "down":
        objects["larged"+str(temps)] = Actif(
        {
            key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/large"))], [[PurePath("level/elements/large/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/large/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/large"))]])
        },
        {
            key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/large"))]
        },
        "idle",
        tags=["enemy", "elementdown", "large", str(temps)]
        )
        calques[3]["larged"+str(temps)] = [(temps * vitessecam / 1000) + 150, 367 - objects["larged"+str(temps)].sprites["idle"][0].get_height() / 2]
        stats_perso["nbitems1"] += 1

def creerLong(temps, placement) :
    global stats_perso
    # temps = [ms, ms] : début et fin
    # placement - up : en haut, down : en bas
    if placement == "up":
        # Pour chaque element, créer trois elements
        # Le long au début
        objects["longstartup"+str(temps[0])] = Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))], [[PurePath("level/elements/long_ends/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_ends/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]
            },
            "idle",
            tags=["element", "long", "start", "elementup", str(temps[1])]
        )
        # Le long à la fin
        objects["longendup"+str(temps[1])] = Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))], [[PurePath("level/elements/long_ends/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_ends/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]
            },
            "idle",
            tags=["element", "long", "end", "up", str(temps[0])]
        )
        # Le long entre les deux
        objects["longmiddleup"+str(temps[0])] = Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_line"))], [[PurePath("level/elements/long_line/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_line/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_line"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_line"))]
            },
            "idle",
            tags=["element", "long", "middle"]
        )

        for anim in objects["longmiddleup"+str(temps[0])].sprites:
            for index, image in enumerate(objects["longmiddleup"+str(temps[0])].sprites[anim]):
                surfaceinit = pygame.Surface(((((temps[1] * vitessecam / 1000) + 150 - objects["longendup"+str(temps[1])].sprites["idle"][0].get_width()/2) - ((temps[0] * vitessecam / 1000) + 150 + objects["longstartup"+str(temps[0])].sprites["idle"][0].get_width() / 2)), image.get_height()), flags=SRCALPHA)
                drawx = 0
                while drawx <= surfaceinit.get_width():
                    surfaceinit.blit(image, (drawx, 0))
                    drawx += image.get_width()-1
                objects["longmiddleup"+str(temps[0])].sprites[anim][index] = surfaceinit

        # La taille du long au milieu = (position de la fin - taille d'un extrémité) - (position du début + taille d'un extrémité) / taille originale du milieu 
        # objects["longmiddleup"+str(temps[0])].taillex = (((temps[1] * vitessecam / 1000) + 150) - ((temps[0] * vitessecam / 1000) + 150)) / objects["longmiddleup"+str(temps[0])].sprites["idle"][0].get_width()
        calques[3]["longmiddleup"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150 + objects["longstartup"+str(temps[0])].sprites["idle"][0].get_width() / 2, 187 - objects["longmiddleup"+str(temps[0])].sprites["idle"][0].get_height() / 2]
        calques[3]["longstartup"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, 187 - objects["longstartup"+str(temps[0])].sprites["idle"][0].get_height() / 2]
        stats_perso["nbitems1"] += 1
        # 200 --> 150 + taille de l'extrémité du début (50)
        # 100 --> 150 - taille de l'extrémité de la fin (50) --> le côté droit de l'extrémité de la fin sera à la fin du long
        calques[3]["longendup"+str(temps[1])] = [(temps[1] * vitessecam / 1000) + 150 - objects["longendup"+str(temps[1])].sprites["idle"][0].get_width(), 187 - objects["longendup"+str(temps[1])].sprites["idle"][0].get_height() / 2]

    elif placement == "down":
        objects["longstartdown"+str(temps[0])] = Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))], [[PurePath("level/elements/long_ends/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_ends/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]
            },
            "idle",
            tags=["element", "long", "start", "elementdown", str(temps[1])]
            )
        objects["longenddown"+str(temps[1])] = Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))], [[PurePath("level/elements/long_ends/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_ends/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]
            },
            "idle",
            tags=["element", "long", "end", "down", str(temps[0])]
            )
        objects["longmiddledown"+str(temps[0])] = Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_line"))], [[PurePath("level/elements/long_line/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_line/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_line"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_line"))]
            },
            "idle",
            tags=["element", "long", "middle"]
            )

        for anim in objects["longmiddledown"+str(temps[0])].sprites:
            for index, image in enumerate(objects["longmiddledown"+str(temps[0])].sprites[anim]):
                surfaceinit = pygame.Surface(((((temps[1] * vitessecam / 1000) + 150 - objects["longenddown"+str(temps[1])].sprites["idle"][0].get_width()/2) - ((temps[0] * vitessecam / 1000) + 150 + objects["longstartdown"+str(temps[0])].sprites["idle"][0].get_width() / 2)), image.get_height()), flags=SRCALPHA)
                drawx = 0
                while drawx <= surfaceinit.get_width():
                    surfaceinit.blit(image, (drawx, 0))
                    drawx += image.get_width()-1
                objects["longmiddledown"+str(temps[0])].sprites[anim][index] = surfaceinit
            
        # objects["longmiddledown"+str(temps[0])].taillex = (((temps[1] * vitessecam / 1000) + 150) - ((temps[0] * vitessecam / 1000) + 150)) / objects["longmiddledown"+str(temps[0])].sprites["idle"][0].get_width()
        calques[3]["longmiddledown"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150 + objects["longstartdown"+str(temps[0])].sprites["idle"][0].get_width() / 2, 367 - objects["longmiddledown"+str(temps[0])].sprites["idle"][0].get_height() / 2]        
        calques[3]["longstartdown"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, 367 - objects["longstartdown"+str(temps[0])].sprites["idle"][0].get_height() / 2]
        stats_perso["nbitems1"] += 1
        calques[3]["longenddown"+str(temps[1])] = [(temps[1] * vitessecam / 1000) + 150 - objects["longenddown"+str(temps[1])].sprites["idle"][0].get_width(), 367 - objects["longenddown"+str(temps[1])].sprites["idle"][0].get_height() / 2]

def creerBoss(temps, typeelement) :
    global stats_perso
    # si le boss est de type hit, le temps sera juste en milisecondes
    # sinon, le temps sera [ms, ms] --> début, fin
    if typeelement == "hit":
        objects["boss"+str(temps)] = Actif(
        {
            key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/boss"))], [[PurePath("level/elements/boss/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/boss/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/boss"))]])
        },
        {
            key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/boss"))]
        },
        "idle",
        tags=["enemy", "boss", "hit"]
        )
        stats_perso["nbitems1"] += 1
        calques[3]["boss"+str(temps)] = [(temps * vitessecam / 1000) + 150, 273 - objects["boss"+str(temps)].sprites["idle"][0].get_height() / 2]
    elif typeelement == "long":
        objects["boss"+str(temps[0])] = Actif(
        {
            key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/boss"))], [[PurePath("level/elements/boss/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/boss/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/boss"))]])
        },
        {
            key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/boss"))]
        },
        "idle",
        tags=["enemy", "boss", "bosslong", str(temps[1])]
        )
        calques[3]["boss"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, 273 - objects["boss"+str(temps[0])].sprites["idle"][0].get_height() / 2]

def creerFantome(temps, typeelement) :
    if typeelement == "up":
        objects["fantome"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/fantome.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "fantome"]
        )
        calques[3]["fantome"+str(temps)] = [(temps * vitessecam / 1000) + 150, 160]
    elif typeelement == "down":
        objects["fantome"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/fantome.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementdown", "fantome"]
        )
        calques[3]["fantome"+str(temps)] = [(temps * vitessecam / 1000) + 150, 340]

def creerNotePhase2(temps, note, offsetx, offsety) :
    global flagliee, autreliee, positionliee, intervallecourant, stats_perso
    # temps en milisecondes
    # note : hauteur midi
    # offset : décalage x et y des positions des queues de notes
    # precision : longueur d'une double croche
    precision = levelmaker.precision
    nomnote = ""
    # Si la note est inférieure à une blanche
    if temps[1]-temps[0] <= 8*precision:
        # Créer le cercle noire
        nomnote = "noire"
        objects["noire"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/noire.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "note", "noire", str(temps[1])]
            )
        calques[3]["noire"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, note]
        stats_perso["nbitems2"] += 1
        # Si le temps est inférieur à une croche
        if temps[1]-temps[0] <= 2*precision:
            # Créer la queue d'une double croche
            objects["dblcroche"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/doublecroche.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "dblcroche"]
            )
            # Si offsety == 0, elle est donc à gauche du cercle noire, donc surement une note dans la deuxième mesure, donc on retourne la croche horizontalement
            if offsety==0:
                objects["dblcroche"+str(temps[0])].sprites["anim1"][0] = pygame.transform.flip(objects["dblcroche"+str(temps[0])].sprites["anim1"][0], 0, 1)
            calques[2]["dblcroche"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150 + offsetx, note - offsety]
        # Si le temps est inférieur à une noire
        elif temps[1]-temps[0] <= 4*precision:
            # Créer la queue d'une croche
            objects["croche"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/croche.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "croche"]
            )
            # Si offsety == 0, elle est donc à gauche du cercle noire, donc surement une note dans la deuxième mesure, donc on retourne la croche horizontalement
            if offsety==0:
                objects["croche"+str(temps[0])].sprites["anim1"][0] = pygame.transform.flip(objects["croche"+str(temps[0])].sprites["anim1"][0], 0, 1)
            calques[2]["croche"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150 + offsetx, note - offsety]
        # Si le temps est inférieur à une blanche
        else:
            # Créer une queue simple
            objects["lignenote"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/lignenote.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "lignenote"]
            )
            calques[2]["lignenote"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150 + offsetx, note - offsety]
    
    # Si la note est inférieure à une ronde
    elif temps[1]-temps[0] <= 16*precision:
        # Créer une blanche
        nomnote = "blanche"
        objects["blanche"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/blanche.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "note", "blanche", str(temps[1])]
            )
        # Créer une queue simple
        objects["lignenote"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/lignenote.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "lignenote"]
            )
        # Créer la ligne de durée d'une blanche
        objects["line"+str(temps[0])] = Line(
                    0, 
                    0, 
                    (temps[1]-temps[0])*vitessecam/1000,
                    0,
                    (255, 255, 255), 
                    5, 
                    lueurBool=True, 
                    couleurlueur=(0, 255, 0)
                )
        calques[2]["lignenote"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150 + offsetx, note - offsety]
        calques[3]["line"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, note + 15]
        calques[3]["blanche"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, note]
        stats_perso["nbitems2"] += 1
    # Si la note est inférieure à une double ronde (au delà, la note n'est pas comptée)
    elif temps[1]-temps[0] <= 32*precision:
        # Créer une ronde
        nomnote = "ronde"
        objects["ronde"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/ronde.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "note", "ronde", str(temps[1])]
            )
        calques[3]["ronde"+str(temps[0])] = [(temps[0] * vitessecam / 1000) + 150, note]
        stats_perso["nbitems2"] += 1
    # Pour chaque intervalle de notes liées
    for intervalle in levelelements["liee"]["flagliee"]:
        # Si la note crée se trouve dans l'intervalle liée
        if temps[0] >= intervalle[0] and temps[0] <= intervalle[1]:
            # Activer le flag liée
            flagliee = True
        else:
            # Le désactiver
            flagliee = False
            # Si l'intervalle était pas celui courant (si on avait déjà une ligne liée en cours)
            if intervalle != intervallecourant:
                # S'arrêter, passer au prochain intervalle
                continue
        # Si le flag est activée
        if flagliee:
            # Si c'est la première note liée dans l'intervalle
            if not autreliee:
                # Ne rien faire, définir la position de cette note
                positionliee = [(temps[0] * vitessecam / 1000) + 150 + 15, note + 15]
                objects[nomnote+str(temps[0])].tags.insert(1, "lien")
                # Activez le flag autreliee
                autreliee = True
                # Définir l'intervalle en cours
                intervallecourant = intervalle
            # Si c'est une autre note liée dans l'intervalle
            else:
                # Créer la ligne de liée
                objects["liee"+str(temps[0])] = Line(
                    0, 
                    0, 
                    (temps[0] * vitessecam / 1000) + 150 + 15 - positionliee[0],
                    note + 15 - positionliee[1],
                    (255, 255, 255), 
                    5, 
                    lueurBool=True, 
                    couleurlueur=(0, 255, 0)
                )
                # Le positionner à la position de la note précédente
                calques[3]["liee"+str(temps[0])] = positionliee
                # Redéfinir la position de cette note pour la prochaine
                positionliee = [(temps[0] * vitessecam / 1000) + 150 + 15, note + 15]
                objects[nomnote+str(temps[0])].tags.insert(1, "lien")
        # Si le flag n'est plus activée dans l'intervalle courant
        else:
            # Plus d'autre liée, remettre à False
            autreliee = False

def creerSilence(temps, placement) :
    if placement == "up":
        objects["silence"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/silence.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "silence"]
        )
        calques[3]["silence"+str(temps)] = [(temps * vitessecam / 1000) + 150, 125]
    elif placement == "middle":
        objects["silence"+str(temps)] = Actif(
            {"anim1" : [PurePath("images/level/silence.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "elementup", "silence"]
        )
        calques[3]["silence"+str(temps)] = [(temps * vitessecam / 1000) + 150, 215]
    elif placement == "down":
        objects["silence"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/silence.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementdown", "silence"]
        )
        calques[3]["silence"+str(temps)] = [(temps * vitessecam / 1000) + 150, 305]

# Programme à lancer au début de scène
def init():
    global objects, calques, camera, fond, pause, gameovertimer, levelelements, pos_pers, gameoverbool, perso_phase3, stats_perso, nomniveau, vitessecam, parallax1, parallax2, parallax3, parallax4
    
    # Redéfinir les valeurs par défaut
    gameovertimer = 0

    # Propriétés du perso de la phase 3
    perso_phase3.update({
        "jumpCount" : 0,
        "isJump" : False,
        "reverse" : False,
        "dash" : False,
        "objectdash" : "",
        "posydash" : 0
    })
    
    gameoverbool = False
    # Le perso de la phase 3 est à l'endroit
    perso_phase3["reverse"] = False
    # Plus de collision dans la phase 3
    collidephase3 = []

    fileconfig = None

    # Chargement de la musique du niveau en mémoire
    for file in os.listdir("levelfiles"):
        if game.niveaucourant in file and file.endswith(".asrg"):
            with zipfile.ZipFile(PurePath("levelfiles/" + file), "r") as filelevel:
                fileconfig = io.TextIOWrapper(filelevel.open(game.niveaucourant + ".config"))
                with open("music_stream", "wb") as musstr:
                    musstr.write(filelevel.open(game.niveaucourant + ".wav").read())

                for line in fileconfig:
                    if "VITESSECAMERA" in line:
                        vitessecam = int(line[:-1].split("\t")[1])
                    if "PARALLAX1" in line:
                        parallax1 = list(map(float, line[:-1].split("\t")[1:]))
                    if "PARALLAX2" in line:
                        parallax2 = list(map(float, line[:-1].split("\t")[1:]))
                    if "PARALLAX3" in line:
                        parallax3 = list(map(float, line[:-1].split("\t")[1:]))
                    if "PARALLAX4" in line:
                        parallax4 = list(map(float, line[:-1].split("\t")[1:]))

                filelevel.extractall(PurePath("level"))

                # Analyse du fichier csv niveau
                match game.niveaudifficulte:
                    case 0:
                        filelevel.extract(game.niveaucourant + "_facile.csv")
                        levelelements = levelmaker.getelements(PurePath(game.niveaucourant + "_facile.csv"))
                    case 1:
                        filelevel.extract(game.niveaucourant + "_moyen.csv")
                        levelelements = levelmaker.getelements(PurePath(game.niveaucourant + "_moyen.csv"))
                    case 2:
                        filelevel.extract(game.niveaucourant + "_difficile.csv")
                        levelelements = levelmaker.getelements(PurePath(game.niveaucourant + "_difficile.csv"))
                

    pygame.mixer.music.load(PurePath("music_stream"))

    # Création (ou recréation) des objets de base
    objects.clear()
    objects.update({"bandeau_haut" : Actif(
        {"bandeau_haut" : [PurePath("images/interface/bandeau.png")]},
        {"bandeau_haut" : [True, 1]},
        "bandeau_haut"
        ),
        "bandeau_bas" : Actif(
            {"bandeau_bas" : [PurePath("images/interface/bandeau.png")]},
            {"bandeau_bas" : [True, 1]},
            "bandeau_bas"
        ),
        "pers1" : Actif(
            {"debout" : [PurePath("images/level/personnage.png")]},
            {"debout" : [True, 5]},
            "debout"
        ),
        "PV" : Text(
            "PV",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            20,
            (255,255,255)
        ),
        "score" : Text(
            "Score",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            30,
            (255,255,255)
        ),
        "numscore" : Text(
            "01458",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            32,
            (255,255,0)
        ),
        "combo" : Text(
            "combo",
            PurePath("fonts/LTSaeada-SemiBold.otf"),
            20,
            (255,255,0)
        ),
        "pause" : Bouton(
            { "pause" : [
                [PurePath("images/interface/boutonpause.png")],
                [PurePath("images/interface/boutonpause.png")],
                [PurePath("images/interface/boutonpause.png")],
                [PurePath("images/interface/boutonpause.png")],
                [PurePath("images/interface/boutonpause.png")]
            ]},
            {"pause" : [
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "pause"
        ),
        "cadreProgression" : Actif(
            {"anim1" : [PurePath("images/interface/cadreProgression.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "cadrePV" : Actif(
            {"anim1" : [PurePath("images/interface/cadrePV.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "jaugeProgression" : Actif(
            {"anim1" : [PurePath("images/interface/jaugeProgression.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "jaugeVertPV" : Actif(
            {"anim1" : [PurePath("images/interface/jaugeVertPV.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "jaugeRougePV" : Actif(
            {"anim1" : [PurePath("images/interface/jaugeRougePV.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "premierFond" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/premierPlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/premierPlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/premierPlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/premierPlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/premierPlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "premierFondbis" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/premierPlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/premierPlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/premierPlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/premierPlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/premierPlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "deuxiemeFond" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/deuxiemePlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/deuxiemePlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/deuxiemePlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/deuxiemePlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/deuxiemePlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "deuxiemeFondbis" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/deuxiemePlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/deuxiemePlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/deuxiemePlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/deuxiemePlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/deuxiemePlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "troisiemeFond" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/troisiemePlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/troisiemePlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/troisiemePlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/troisiemePlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/troisiemePlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "troisiemeFondbis" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/troisiemePlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/troisiemePlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/troisiemePlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/troisiemePlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/troisiemePlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "quatriemeFond" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/quatriemePlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/quatriemePlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/quatriemePlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/quatriemePlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/quatriemePlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "quatriemeFondbis" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/quatriemePlan")) if namefond.startswith("fond")], [[PurePath("level/fonds/quatriemePlan/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/quatriemePlan/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/quatriemePlan")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/quatriemePlan")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "sol" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")], [[PurePath("level/fonds/sol/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/sol/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "solbis" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")], [[PurePath("level/fonds/sol/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/sol/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "solhaut" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")], [[PurePath("level/fonds/sol/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/sol/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "solbishaut" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")], [[PurePath("level/fonds/sol/" + anim + "/" + image) for image in os.listdir(PurePath("level/fonds/sol/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/fonds/sol")) if namefond.startswith("fond")]
            },
            "fond0"
        ),
        "fondpause" : Actif(
            {"anim1" : [PurePath("images/fonds/fondpause.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "portee_haut" : Actif(
            {"anim1" : [PurePath("images/level/portee.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "portee_bas" : Actif(
            {"anim1" : [PurePath("images/level/portee.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "ligne" : Actif(
            {"anim1" : [PurePath("images/level/ligne_phase2.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "cible_haut" : Actif(
            {"anim1" : [PurePath("images/level/cible.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "cible_bas" : Actif(
            {"anim1" : [PurePath("images/level/cible.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "gameoverscreen" : Actif(
            {"anim1" : [PurePath("images/fonds/gameoverscreen.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "curseur" : Actif(
            {"anim1" : [PurePath("images/level/curseur.png")]},
            {"anim1" : [False, 5]},
            "anim1"
        ),
        "persophase3" : Actif(
            {
                "marche" : [PurePath("images/level/animation/persophase3marche/" + format(i, '05d') + ".png") for i in range(18)],
                "saut" : [PurePath("images/level/animation/persophase3saut/" + format(i, '05d') + ".png") for i in range(18)]
            },
            {
                "marche" : [True, 2],
                "saut" : [False, 2]
            },
            "marche"
        ),
        "texthit" : Actif(
            {
                "start" : [PurePath("images/interface/animation/start/" + format(i, '05d') + ".png") for i in range(17)],
                "miss" : [PurePath("images/interface/animation/miss/" + format(i, '05d') + ".png") for i in range(15)],
                "great" : [PurePath("images/interface/animation/great/" + format(i, '05d') + ".png") for i in range(15)],
                "perfect" : [PurePath("images/interface/animation/perfect/" + format(i, '05d') + ".png") for i in range(15)]
            },

            {
                "start" : [False, 1],
                "miss" : [False, 1],
                "great" : [False, 1],
                "perfect" : [False, 1]
            },

            "start"
        ),
        "impacthaut" : Actif(
            {"anim1" : [PurePath("images/interface/animation/impact/" + format(i, '05d') + ".png") for i in range(1, 7)]},
            {"anim1" : [False, 1]},
            "anim1"
        ),
        "impactbas" : Actif(
            {"anim1" : [PurePath("images/interface/animation/impact/" + format(i, '05d') + ".png") for i in range(1, 7)]},
            {"anim1" : [False, 1]},
            "anim1"
        ),
        "dedoublepersohaut" : Actif(
            {"anim1" : [PurePath("images/level/personnage2.png")]},
            {"anim1" : [False, 1]},
            "anim1"
        ),
        "dedoublepersobas" : Actif(
            {"anim1" : [PurePath("images/level/personnage2.png")]},
            {"anim1" : [False, 1]},
            "anim1"
        ),
        "longendcurseurhaut" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))], [[PurePath("level/elements/long_ends/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_ends/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]
            },
            "idle"
        ),
        "longendcurseurbas" : Actif(
            {
                key : value for key, value in zip([namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))], [[PurePath("level/elements/long_ends/" + anim + "/" + image) for image in os.listdir(PurePath("level/elements/long_ends/" + anim))] for anim in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]])
            },
            {
                key : [True, 1] for key in [namefond for namefond in os.listdir(PurePath("level/elements/long_ends"))]
            },
            "idle"
        ),
        "play" : Bouton(
            { "play" : [
                [PurePath("images/interface/boutonplay.png")],
                [PurePath("images/interface/boutonplay.png")],
                [PurePath("images/interface/boutonplay.png")],
                [PurePath("images/interface/boutonplay.png")],
                [PurePath("images/interface/boutonplay.png")]
            ]},
            {"play" : [
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "play"
        ),
        "decompteplay" : Actif(
            {"anim1" : [PurePath("images/interface/animation/decompteplay/" + format(i, '05d') + ".png") for i in range(45)]},
            {"anim1" : [False, 1]},
            "anim1"
        ),
        "retour" : Bouton(
            { "anim1" : [
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")],
                [PurePath("images/interface/flecheretour.png")]
            ]},
            {"anim1" : [
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "anim1"
        ),
        "recommencer" : Bouton(
            { "anim1" : [
                [PurePath("images/interface/Fleche_Recommencer.png")],
                [PurePath("images/interface/Fleche_Recommencer.png")],
                [PurePath("images/interface/Fleche_Recommencer.png")],
                [PurePath("images/interface/Fleche_Recommencer.png")],
                [PurePath("images/interface/Fleche_Recommencer.png")]
            ]},
            {"anim1" : [
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5],
                [False, 0, 5]
            ]},
            "anim1"
        ),
        "changetheme" : Actif(
            {"anim1" : [PurePath("images/level/animation/changetheme/" + str(i) + ".png") for i in range(6)]},
            {"anim1" : [False, 1]},
            "anim1"
        )
        })

    # A enlever
    """
    objects["premierFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["premierFondbis"].sprites["anim1"][0], 1, 0)
    objects["deuxiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["deuxiemeFondbis"].sprites["anim1"][0], 1, 0)
    objects["troisiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["troisiemeFondbis"].sprites["anim1"][0], 1, 0)
    objects["quatriemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["quatriemeFondbis"].sprites["anim1"][0], 1, 0)
    """
    for anim in objects["solhaut"].sprites:
        for index, image in enumerate(objects["solhaut"].sprites[anim]):
            objects["solhaut"].sprites[anim][index] = pygame.transform.flip(image, 0, 1)

    for anim in objects["solbishaut"].sprites:
        for index, image in enumerate(objects["solbishaut"].sprites[anim]):
            objects["solbishaut"].sprites[anim][index] = pygame.transform.flip(image, 0, 1)

    #Tailles objets
    """
    objects["pers1"].taillex = 0.5
    objects["pers1"].tailley = 0.5
    """
    
    # (Re)Définition des calques et des positions de chaque objet de la scène
    calques.clear()
    calques.update({0:{
            "quatriemeFond" : [0, 0], 
            "quatriemeFondbis" : [960, 0], 
            "troisiemeFond" : [0, 0], 
            "troisiemeFondbis" : [960, 0], 
            "deuxiemeFond" : [0, 0], 
            "deuxiemeFondbis" : [960, 0], 
            "premierFond" : [0, 0], 
            "premierFondbis" : [960, 0], 
            "sol" : [0, 410], 
            "solbis" : [960, 410],
            "solhaut" : [0, 65], 
            "solbishaut" : [960, 65],
            "gameoverscreen" : [0, 0]
        }, 
        1:{
            "cible_haut" : [141, 150],
            "cible_bas" : [141, 330],
            "portee_haut" : [0, 120],
            "portee_bas" : [0, 300],
            "ligne" : [158, 0],
            "curseur" : [142, 235],
            "persophase3" : [50, 350],
            "pers1" : [50, 280],
            "dedoublepersohaut" : [50, 100],
            "dedoublepersobas" : [50, 280]
        },
        2:{},
        "border":{},
        3:{},
        "items" : {},
        4:{
            "fondpause" : [0, 0],
            "changetheme" : [0, 0],
            "bandeau_haut" : [0, 0], 
            "bandeau_bas" : [0, 470], 
            "cadreProgression" : [125, 492],
            "cadrePV" : [288, 7], 
            "jaugeProgression" : [130, 497], 
            "jaugeRougePV" : [293, 11], 
            "jaugeVertPV" : [293, 11], 
            "PV" : [461, 10], 
            "score" : [10, 40],
            "numscore" : [10, 10],
            "combo" : [474, 40],
            "decompteplay" : [420, 199],
            "pause" : [890, 0],
            "texthit" : [120, 220],
            "impacthaut" : [75, 65],
            "impactbas" : [75, 260],
            "longendcurseurhaut" : [176 - objects["longendcurseurhaut"].sprites["idle"][0].get_width() / 2, 187 - objects["longendcurseurhaut"].sprites["idle"][0].get_height() / 2],
            "longendcurseurbas" : [176 - objects["longendcurseurbas"].sprites["idle"][0].get_width() / 2, 367 - objects["longendcurseurbas"].sprites["idle"][0].get_height() / 2],
            "play" : [445, 235],
            "retour" : [358, 235],
            "recommencer" : [532, 235]
        }})

    
    # Le perso de la phase 1 commence en bas
    pos_pers = 1

    #Ombres objets
    objects["PV"].shadow = True
    objects["score"].shadow = True
    objects["numscore"].shadow = True
    objects["combo"].shadow = True

    #Parallax
    objects["premierFond"].parallax = objects["premierFondbis"].parallax = [0.8, 1.0]
    objects["deuxiemeFond"].parallax = objects["deuxiemeFondbis"].parallax = [0.6, 1.0]
    objects["troisiemeFond"].parallax = objects["troisiemeFondbis"].parallax = [0.4, 1.0]
    objects["quatriemeFond"].parallax = objects["quatriemeFondbis"].parallax = [0.2, 1.0]

    # Tous les objets du calque 1 restent sur l'écran
    for object in calques[1]:
        objects[object].suivreScene = True

    # Tous les objets du calque 4 restent sur l'écran
    for object in calques[4]:
        objects[object].suivreScene = True

    objects["gameoverscreen"].suivreScene = True

    objects["fondpause"].visible = False
    objects["portee_haut"].visible = False
    objects["portee_bas"].visible = False
    objects["ligne"].visible = False
    objects["dedoublepersohaut"].visible = False
    objects["dedoublepersobas"].visible = False
    objects["ligne"].visible = False
    objects["curseur"].visible = False
    objects["gameoverscreen"].visible = False
    objects["play"].visible = False
    objects["decompteplay"].visible = False
    objects["retour"].visible = False
    objects["recommencer"].visible = False

    # Reset des stats du perso
    stats_perso.update({
        "score" : 0,
        "pv" : 200,
        "compteurcomboglobal" : 0,
        "comboglobal" : 0,

        "scorephase1": 0,
        "scorephase2": 0,
        "scorephase3": 0,

        "precisionphase1" : 0,
        "precisionphase2" : 0,
        "precisionphase3" : 0,

        "compteurcombophase1" : 0,
        "compteurcombophase2" : 0,
        "combophase1" : 0,
        "combophase2" : 0,

        "compteurtempsphase3" : 0,
        "tempsphase3" : 0,

        "notesphase1" : 0,
        "notesphase3" : 0,

        "missphase1" : 0,
        "missphase2" : 0,
        "missphase3" : 0,

        "greatphase1" : 0,
        "greatphase2" : 0,
        
        "perfectphase1" : 0,
        "perfectphase2" : 0,

        "passphase2" : 0,

        "inLongUp" : False,
        "inLongDown" : False,
        "tempsUp" : "",
        "tempsDown" : "",

        "nbitems1" : 0,
        "nbitems2" : 0
    })
    
    # Mettre le calcul de vitesse de la souris à 0 (en appelant la fonction get_rel de la souris pygame)
    

    # Le jeu n'est pas en pause
    pause = False

        

    # Pour chaque type d'élement du niveau
    for element in levelelements:
        match element:
            # Changement de phase
            case "phase":
                for phase in levelelements[element]:
                    if phase=="phase1" and levelelements[element][phase] != []:
                        objects["iconphase1"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase1.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface", "phase"]
                        )
                    if phase=="phase2" and levelelements[element][phase] != []:
                        objects["iconphase2"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase2.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface", "phase"]
                        )
                    if phase=="phase3" and levelelements[element][phase] != []:
                        objects["iconphase3"] = Actif(
                            {"anim1" : [PurePath("images/level/placeholder/phase3.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["interface", "phase"]
                        )
            # Items (note de score et coeur)
            case "items":
                # Pour chaque hauteur
                for note in levelelements[element]:
                    match note:
                        # Créer un coeur/note au bon endroit
                        case "C5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 382)
                        case "C#5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 332)
                        case "D5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 282)
                        case "D#5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 232)
                        case "E5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 182)
                        case "F5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 122)
                        case "C6":
                            for time in levelelements[element][note]:
                                creerNote(time, 382)
                        case "C#6":
                            for time in levelelements[element][note]:
                                creerNote(time, 332)
                        case "D6":
                            for time in levelelements[element][note]:
                                creerNote(time, 282)
                        case "D#6":
                            for time in levelelements[element][note]:
                                creerNote(time, 232)
                        case "E6":
                            for time in levelelements[element][note]:
                                creerNote(time, 182)
                        case "F6":
                            for time in levelelements[element][note]:
                                creerNote(time, 122)
            case "small":
                for temps in levelelements[element]['up']:
                    creerSmall(temps, "up")
                for temps in levelelements[element]['down']:
                    creerSmall(temps, "down")
            
            case "large":
                for temps in levelelements[element]['up']:
                    creerLarge(temps, "up")
                for temps in levelelements[element]['down']:
                    creerLarge(temps, "down")

            case "long":
                for temps in levelelements[element]['up']:
                    creerLong(temps, "up")
                for temps in levelelements[element]['down']:
                    creerLong(temps, "down")

            case "boss":
                for temps in levelelements[element]['hit']:
                    creerBoss(temps, "hit")
                for temps in levelelements[element]['long']:
                    creerBoss(temps, "long")

            case "fantome":
                for temps in levelelements[element]['up']:
                    creerFantome(temps, "up")
                for temps in levelelements[element]['down']:
                    creerFantome(temps, "down")

            case "normal" | "liee":
                for note in levelelements[element]:
                    match note[0]:
                        case "43" :
                            creerNotePhase2([note[1], note[2]], 388, 0, 0)
                        case "45" :
                            creerNotePhase2([note[1], note[2]], 376, 0, 0)
                        case "47" :
                            creerNotePhase2([note[1], note[2]], 365, 0, 0)
                        case "48" :
                            creerNotePhase2([note[1], note[2]], 353, 0, 0)
                        case "50" :
                            creerNotePhase2([note[1], note[2]], 341, 0, 0)
                        case "52" :
                            creerNotePhase2([note[1], note[2]], 330, 0, 0)
                        case "53" :
                            creerNotePhase2([note[1], note[2]], 319, 0, 0)
                        case "55" :
                            creerNotePhase2([note[1], note[2]], 307, 0, 0)
                        case "57" :
                            creerNotePhase2([note[1], note[2]], 296, 0, 0)
                        case "59" :
                            creerNotePhase2([note[1], note[2]], 281, 0, 0)
                        case "60" :
                            creerNotePhase2([note[1], note[2]], 252, 26, 70)
                        case "62" :
                            creerNotePhase2([note[1], note[2]], 221, 26, 70)
                        case "64" :
                            creerNotePhase2([note[1], note[2]], 208, 26, 70)
                        case "65" :
                            creerNotePhase2([note[1], note[2]], 196, 26, 70)
                        case "67" :
                            creerNotePhase2([note[1], note[2]], 185, 26, 70)
                        case "69" :
                            creerNotePhase2([note[1], note[2]], 173, 26, 70)
                        case "71" :
                            creerNotePhase2([note[1], note[2]], 161, 26, 70)
                        case "72" :
                            creerNotePhase2([note[1], note[2]], 161, 26, 70)
                        case "74" :
                            creerNotePhase2([note[1], note[2]], 139, 26, 70)
                        case "76" :
                            creerNotePhase2([note[1], note[2]], 127, 26, 70)
                        case "77" :
                            creerNotePhase2([note[1], note[2]], 116, 26, 70)
            case "silence":
                for time in levelelements[element]['up']:
                        creerSilence(time, "up")
                for time in levelelements[element]['middle']:
                        creerSilence(time, "middle")
                for time in levelelements[element]['down']:
                        creerSilence(time, "down")

            case "cube":
                # Pour chaque temps et liste de position de cube
                """
                Exemple : [1, 1, 0, 0, 0, 0]
                ▢
                ▢
                ▢
                ▢
                ■
                ■
                """
                for time, poslist in levelelements[element].items():
                    # Pour chaque position de cube (on parcourt la liste)
                    for cube in range(len(poslist)):
                        # Si c'est 1
                        if poslist[cube] == 1:
                            # On crée le cube et le bord du cube derriére
                            objects["cube"+str(cube)+str(float(time))] = Actif(
                            {"anim1" : [PurePath("images/level/cube_50.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["element", "cube"]
                            )
                            objects["cubebord"+str(cube)+str(float(time))] = Actif(
                            {"anim1" : [PurePath("images/level/cube_bord2.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["element", "cubebord"]
                            )
                            # Taille du cube dépend de la durée d'une note dans la phase 3
                            objects["cube"+str(cube)+str(float(time))].taillex = ((levelelements["mincube"]*vitessecam/1000))/50
                            objects["cubebord"+str(cube)+str(float(time))].taillex = ((levelelements["mincube"]*vitessecam/1000))/50
                            
                            calques[3]["cube"+str(cube)+str(float(time))] = [(float(time) * vitessecam / 1000) + 150, 371-(50*(cube))]
                            calques["border"]["cubebord"+str(cube)+str(float(time))] = [(float(time) * vitessecam / 1000) + 145, 366-(50*(cube))]

            case "pique":
                # Même principe
                for time, poslist in levelelements[element].items():
                    for pique in range(len(poslist)):
                        if poslist[pique] == 1:
                            # Si le pique est pas sur un sol ni sur un cube
                            if 0 < pique < 5 and time in levelelements["cube"] and levelelements["cube"][time][pique+1] == 0 and levelelements["cube"][time][pique-1] == 0:
                                # Créer un pique roue (picrew ＼（〇_ｏ）／)
                                objects["pique"+str(pique)+str(float(time))] = Actif(
                                {"anim1" : [PurePath("images/level/roue.png")]},
                                {"anim1" : [False, 5]},
                                "anim1",
                                tags=["element", "pique"]
                                )
                                objects["pique"+str(pique)+str(float(time))].taillex = ((levelelements["mincube"]*vitessecam/1000))/50
                            else:
                                # Créer un pique normal
                                objects["pique"+str(pique)+str(float(time))] = Actif(
                                {"anim1" : [PurePath("images/level/pique.png")]},
                                {"anim1" : [False, 5]},
                                "anim1",
                                tags=["element", "pique"]
                                )
                                objects["pique"+str(pique)+str(float(time))].taillex = ((levelelements["mincube"]*vitessecam/1000))/50
                                # Si le pique est sur le sol du haut ou un cube se trouve en haut du pique, retourner le pique
                                if pique == 5 or (time in levelelements["cube"] and levelelements["cube"][time][pique+1]):
                                    objects["pique"+str(pique)+str(float(time))].sprites["anim1"][0] = pygame.transform.flip(objects["pique"+str(pique)+str(float(time))].sprites["anim1"][0], 0, 1)
                            calques[3]["pique"+str(pique)+str(float(time))] = [(float(time) * vitessecam / 1000) + 150, 371-(50*(pique))]


            case "orbe":
                # Même principe
                for time, poslist in levelelements[element].items():
                    for orbe in range(len(poslist)):
                        if poslist[orbe] == 1:
                            objects["orbe"+str(orbe)+str(float(time))] = Actif(
                            {"anim1" : [PurePath("images/level/orbe_reverse.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["element", "orbe"]
                            )
                            objects["orbe"+str(orbe)+str(float(time))].taillex = ((levelelements["mincube"]*vitessecam/1000))/50
                            calques[3]["orbe"+str(orbe)+str(float(time))] = [(float(time) * vitessecam / 1000) + 150, 371-(50*(orbe))]

            
            case "dash":
                # Même principe
                for time, poslist in levelelements[element].items():
                    for dash in range(len(poslist)):
                        if poslist[dash] == 1:
                            objects["dash"+str(dash)+str(float(time))] = Actif(
                            {"anim1" : [PurePath("images/level/dash.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["element", "dash"]
                            )
                            objects["dash"+str(dash)+str(float(time))].taillex = ((levelelements["mincube"]*vitessecam/1000))/50
                            calques[3]["dash"+str(dash)+str(float(time))] = [(float(time) * vitessecam / 1000) + 150, 371-(50*(dash))]

    #Quand tous les objets sont crées, jouer la musique
    pygame.mixer.music.play()


def loopevent(event):
    global calques, initcalques, camera, fond, pause, gameovertimer, pos_pers, gameoverbool, longboss, longphase2
    if event.type == objects["decompteplay"].END_ANIMATION and objects["decompteplay"].visible:
        objects["decompteplay"].visible = False
        pygame.mixer.music.unpause()
        pause = False
    if event.type == KEYDOWN and event.key in game.boutons["haut"] and gameovertimer == 0 and objects["curseur"].visible == False and not pause : # and levelelements["phase"][phaseindex-1][0] == "phase1":
        pos_pers = 0
        objects["impacthaut"].changeAnimation("anim1")
        detectelements = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "elementup" in objects[element].tags and objects[element].visible and "touche" not in objects[element].tags and (80 <= game.displaylist[element].left <= 240)], key=lambda x : calques[3][x][0])
        if detectelements:
            elementhit = detectelements[0]
            if "start" in objects[elementhit].tags:
                stats_perso["inLongUp"] = True
                stats_perso["tempsUp"] = objects[elementhit].tags[-1]
            if 130 <= game.displaylist[elementhit].left < 185:
                objects["texthit"].changeAnimation("perfect")
                if "start" not in objects[elementhit].tags:
                    objects[elementhit].visible = False
                else:
                    objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 1000
                stats_perso["scorephase1"] += 1000
                stats_perso["perfectphase1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                
            elif game.displaylist[elementhit].left < 240:
                objects["texthit"].changeAnimation("great")
                if "start" not in objects[elementhit].tags:
                    objects[elementhit].visible = False 
                else:
                    objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 500
                stats_perso["scorephase1"] += 500
                stats_perso["greatphase1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
        detectboss = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "boss" in objects[element].tags and objects[element].visible and "touche" not in objects[element].tags and (80 <= game.displaylist[element].left <= 240)], key=lambda x : calques[3][x][0])
        if detectboss:
            elementhit = detectboss[0]
            if 130 <= game.displaylist[elementhit].left < 185:
                objects["texthit"].changeAnimation("perfect")
                objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 2000
                stats_perso["scorephase1"] += 2000
                stats_perso["perfectphase1"] += 1
                stats_perso["nbitems1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                
            elif game.displaylist[elementhit].left < 240:
                objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 1000
                stats_perso["scorephase1"] += 1000
                stats_perso["greatphase1"] += 1
                stats_perso["nbitems1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])

            if "bosslong" in objects[elementhit].tags:
                longboss = True
        
        if longboss:
            stats_perso["score"] += 500
            stats_perso["scorephase1"] += 500
            stats_perso["perfectphase1"] += 1
            stats_perso["nbitems1"] += 1
            stats_perso["compteurcombophase1"] += 1
            stats_perso["compteurcomboglobal"] += 1
            stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
            stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])


    if event.type == KEYUP and event.key in game.boutons["haut"] and gameovertimer == 0 and objects["curseur"].visible == False and not pause and levelelements["phase"][phaseindex-1][0] == "phase1":
        if stats_perso["inLongUp"]:
            detectelements = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "end" in objects[element].tags and "up" in objects[element].tags and objects[element].visible and (80 <= game.displaylist[element].left <= 240)], key=lambda x : calques[3][x][0])
            if not detectelements:
                objects["texthit"].changeAnimation("miss")
                stats_perso["compteurcombophase1"] = 0
                stats_perso["compteurcomboglobal"] = 0
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                stats_perso["missphase1"] += 1
        stats_perso["inLongUp"] = False
               
    if event.type == KEYDOWN and event.key in game.boutons["bas"] and gameovertimer == 0 and objects["curseur"].visible == False and not pause and levelelements["phase"][phaseindex-1][0] == "phase1":
        pos_pers = 1
        objects["impactbas"].changeAnimation("anim1")
        detectelements = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "elementdown" in objects[element].tags and "touche" not in objects[element].tags and objects[element].visible and (80 <= game.displaylist[element].left <= 240)], key=lambda x : calques[3][x][0])
        if detectelements:
            elementhit = detectelements[0]
            if "start" in objects[elementhit].tags:
                stats_perso["inLongDown"] = True
                stats_perso["tempsDown"] = objects[elementhit].tags[-1]
            if 130 <= game.displaylist[elementhit].left < 185:
                objects["texthit"].changeAnimation("perfect")
                if "start" not in objects[elementhit].tags:
                    objects[elementhit].visible = False 
                else:
                    objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 1000
                stats_perso["scorephase1"] += 1000
                stats_perso["perfectphase1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                
            elif game.displaylist[elementhit].left < 240:
                objects["texthit"].changeAnimation("great")
                if "start" not in objects[elementhit].tags:
                    objects[elementhit].visible = False 
                else:
                    objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 500
                stats_perso["scorephase1"] += 500
                stats_perso["greatphase1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
        detectboss = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "boss" in objects[element].tags and objects[element].visible and (80 <= game.displaylist[element].left <= 240)], key=lambda x : calques[3][x][0])
        if detectboss:
            elementhit = detectboss[0]
            if 130 <= game.displaylist[elementhit].left < 185:
                objects["texthit"].changeAnimation("perfect")
                objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 2000
                stats_perso["scorephase1"] += 2000
                stats_perso["perfectphase1"] += 1
                stats_perso["nbitems1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                
            elif game.displaylist[elementhit].left < 240:
                objects["texthit"].changeAnimation("great")
                objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 1000
                stats_perso["scorephase1"] += 1000
                stats_perso["greatphase1"] += 1
                stats_perso["nbitems1"] += 1
                stats_perso["compteurcombophase1"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])

            if "bosslong" in objects[elementhit].tags and "finlong" not in objects[elementhit].tags:
                longboss = True  

        if longboss:
            stats_perso["score"] += 500
            stats_perso["scorephase1"] += 500
            stats_perso["nbitems1"] += 1
            stats_perso["perfectphase1"] += 1
            stats_perso["compteurcombophase1"] += 1
            stats_perso["compteurcomboglobal"] += 1
            stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
            stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])

    if event.type == MOUSEBUTTONDOWN and gameovertimer == 0 and levelelements["phase"][phaseindex-1][0] == "phase2" and not pause:
        detectnotes = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "note" in objects[element].tags and "touche" not in objects[element].tags and objects[element].visible and (80 <= game.displaylist[element].left <= 240) and (-40 <= game.displaylist[element].centery-pygame.mouse.get_pos()[1]-35 <= 40)], key=lambda x : calques[3][x][0])
        if detectnotes:
            elementhit = detectnotes[0]
            if 130 <= game.displaylist[elementhit].left < 185 and (-18 <= game.displaylist[elementhit].centery-pygame.mouse.get_pos()[1]-35 <= 18):
                objects["texthit"].changeAnimation("perfect")
                objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 1000
                stats_perso["scorephase2"] += 1000
                stats_perso["perfectphase2"] += 1
                stats_perso["compteurcombophase2"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase2"] = max(stats_perso["compteurcombophase2"], stats_perso["combophase2"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
            else:
                objects["texthit"].changeAnimation("great")
                objects[elementhit].tags.insert(0, "touche")
                stats_perso["score"] += 500
                stats_perso["scorephase2"] += 500
                stats_perso["greatphase2"] += 1
                stats_perso["compteurcombophase2"] += 1
                stats_perso["compteurcomboglobal"] += 1
                stats_perso["combophase2"] = max(stats_perso["compteurcombophase2"], stats_perso["combophase2"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
            if "blanche" in objects[elementhit].tags or "ronde" in objects[elementhit].tags or "lien" in objects[elementhit].tags:
                longphase2 = True

    if event.type == MOUSEBUTTONUP and levelelements["phase"][phaseindex-1][0] == "phase2":
        longphase2 = False

    if event.type == KEYUP and event.key in game.boutons["bas"] and gameovertimer == 0 and objects["curseur"].visible == False and not pause and levelelements["phase"][phaseindex-1][0] == "phase1":
        if stats_perso["inLongDown"]:
            detectmiddle = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "middle" in objects[element].tags and "down" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["cible_bas"])], key=lambda x : calques[3][x][0])
            detectend = sorted([element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "end" in objects[element].tags and "down" in objects[element].tags and "touche" not in objects[element].tags and (80 <= game.displaylist[element].left <= 240)], key=lambda x : calques[3][x][0])
            if not detectend and detectmiddle:
                objects["texthit"].changeAnimation("miss")
                stats_perso["compteurcombophase1"] = 0
                stats_perso["compteurcomboglobal"] = 0
                stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                stats_perso["missphase1"] += 1
            elif detectend:
                objects[detectend[-1]].tags.insert(0, "touche")
        
        stats_perso["inLongDown"] = False
        
        
    if (event.type == objects["pause"].CLICKED or (event.type == KEYDOWN and event.key == K_ESCAPE))\
        and gameovertimer == 0 and not pause:
            game.selectsound.play()
            objects["fondpause"].visible = True
            objects["play"].visible = True
            objects["retour"].visible = True
            objects["recommencer"].visible = True
            pygame.mixer.music.pause()
            pause = True
            pygame.mouse.set_visible(True)
    elif (event.type == objects["play"].CLICKED or (event.type == KEYDOWN and event.key == K_ESCAPE))\
        and gameovertimer == 0 and pause:
            game.selectsound.play()
            objects["fondpause"].visible = False
            objects["play"].visible = False
            objects["retour"].visible = False
            objects["recommencer"].visible = False
            objects["decompteplay"].visible = True
            objects["decompteplay"].changeAnimation("anim1")

    if event.type == objects["retour"].CLICKED and gameovertimer == 0 and objects["retour"].visible:
        game.selectsound.play()
        pygame.mixer.music.unload()
        game.scenecourante = "selectionniveau"
    if event.type == objects["recommencer"].CLICKED and gameovertimer == 0 and objects["recommencer"].visible:
        game.selectsound.play()
        pygame.mixer.music.unload()
        init()
            
    
    if (event.type == KEYDOWN and event.key == K_a):
            pygame.mixer.music.stop()
            objects["gameoverscreen"].visible = True
            gameovertimer = time.time()

    if event.type == KEYDOWN and event.key == K_v:
            game.stats_perso.update(stats_perso)
            game.scenecourante = "victoire"
            camera = [0, 0]
            pygame.mixer.music.stop()

    if event.type == KEYDOWN and event.key == game.boutons["saut"] and levelelements["phase"][phaseindex-1][0] == "phase3":
        perso_phase3["jumpCount"] = 8
        perso_phase3["isJump"] = True
        objects["persophase3"].changeAnimation("saut")
        collideorbephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "orbe" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"])]
        collidedashphase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "dash" in objects[element].tags and objects[element].visible and game.displaylist[element].colliderect(game.displaylist["persophase3"])]

        if collideorbephase3:
            perso_phase3["reverse"] = not perso_phase3["reverse"]
            objects["persophase3"].sprites["anim1"][0] = pygame.transform.flip(objects["persophase3"].sprites["anim1"][0], 0, 1)

        if collidedashphase3:
            perso_phase3["dash"] = True
            perso_phase3["objectdash"] = collidedashphase3[-1]
            perso_phase3["posydash"] = calques[1]["persophase3"][1]

    if event.type == KEYUP and event.key == game.boutons["saut"] and levelelements["phase"][phaseindex-1][0] == "phase3":
        if perso_phase3["dash"]:
            perso_phase3["dash"] = False
            perso_phase3["jumpCount"] = 0
            objects[perso_phase3["objectdash"]].visible = False


def loopbeforeupdate():
    global pause, gameovertimer, camera, levelelements, pos_perso, vitessecam, phaseindex, gameoverbool, longboss, stats_perso, longphase2, vitessecam, themeindex

    collidephase3 = []
    collidepiquephase3 = []

    objects["combo"].changeTexte(str(stats_perso["compteurcomboglobal"]))
    calques[4]["combo"][0] = 480 - (objects["combo"].renderText().get_rect().width / 2)
    objects["jaugeVertPV"].taillex = stats_perso["pv"]/200
    objects["PV"].changeTexte(str(stats_perso["pv"]))
    calques[4]["PV"][0] = 480 - (objects["PV"].renderText().get_rect().width / 2)
    objects["numscore"].changeTexte(str(stats_perso["score"]))

    if themeindex < len(levelelements["theme"])-1 and pygame.mixer.music.get_pos() > levelelements["theme"][themeindex+1][1]:
        themeindex += 1
        objects["changetheme"].changeAnimation("anim1")
        objects["premierFond"].changeAnimation("fond"+str(themeindex))
        objects["premierFondbis"].changeAnimation("fond"+str(themeindex))
        objects["deuxiemeFond"].changeAnimation("fond"+str(themeindex))
        objects["deuxiemeFondbis"].changeAnimation("fond"+str(themeindex))
        objects["troisiemeFond"].changeAnimation("fond"+str(themeindex))
        objects["troisiemeFondbis"].changeAnimation("fond"+str(themeindex))
        objects["quatriemeFond"].changeAnimation("fond"+str(themeindex))
        objects["quatriemeFondbis"].changeAnimation("fond"+str(themeindex))
        objects["sol"].changeAnimation("fond"+str(themeindex))
        objects["solbis"].changeAnimation("fond"+str(themeindex))

    if stats_perso["inLongUp"]:
        stats_perso["score"] += 5
        objects["longendcurseurhaut"].visible = True
    else:
        objects["longendcurseurhaut"].visible = False
    if stats_perso["inLongDown"]:
        stats_perso["score"] += 5
        objects["longendcurseurbas"].visible = True
    else:
        objects["longendcurseurbas"].visible = False

    for element in game.displaylist:
        if not pause:
            if element in objects and isinstance(objects[element], Actif) and "small" in objects[element].tags and "elementup" in objects[element].tags and not objects[element].visible and 0 < game.displaylist[element].left < 960:
                if "double"+objects[element].tags[-1] in objects and "smalld"+objects[element].tags[-1] in objects and not objects["smalld"+objects[element].tags[-1]].visible:
                    objects["double"+objects[element].tags[-1]].visible = False

            if element in objects and isinstance(objects[element], Actif) and "large" in objects[element].tags and "elementup" in objects[element].tags and not objects[element].visible and 0 < game.displaylist[element].left < 960:
                if "larged"+objects[element].tags[-1] in objects and not objects["larged"+objects[element].tags[-1]].visible:
                    objects["double"+objects[element].tags[-1]].visible = False

            if element in objects and isinstance(objects[element], Actif) and ("enemy" in objects[element].tags or "start" in objects[element].tags or "note" in objects[element].tags) and "missed" not in objects[element].tags and "touche" not in objects[element].tags and game.displaylist[element].left < 120:
                objects[element].tags.insert(0, "missed")
                objects["texthit"].changeAnimation("miss")
                
                if levelelements["phase"][phaseindex-1][0] == "phase1":
                    stats_perso["compteurcombophase1"] = 0
                    stats_perso["compteurcomboglobal"] = 0
                    stats_perso["missphase1"] += 1
                    stats_perso["combophase1"] = max(stats_perso["compteurcombophase1"], stats_perso["combophase1"])
                    stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
                else:
                    stats_perso["compteurcombophase2"] = 0
                    stats_perso["compteurcomboglobal"] = 0
                    stats_perso["missphase2"] += 1
                    stats_perso["combophase2"] = max(stats_perso["compteurcombophase2"], stats_perso["combophase2"])
                    stats_perso["comboglobal"] = max(stats_perso["compteurcomboglobal"], stats_perso["comboglobal"])
            
            if element in objects and isinstance(objects[element], Actif) and "itemnote" in objects[element].tags and "missed" not in objects[element].tags and objects[element].visible and game.displaylist[element].left < 80 and levelelements["phase"][phaseindex-1][0] == "phase3":
                objects[element].tags.insert(0, "missed")
                objects["texthit"].changeAnimation("miss")
                stats_perso["missphase3"] += 1

            if element in objects and isinstance(objects[element], Actif) and "end" in objects[element].tags and "touche" not in objects[element].tags and 0 < game.displaylist[element].left < 120:
                if "up" in objects[element].tags and stats_perso["inLongUp"]:
                    stats_perso["inLongUp"] = False
                    objects[element].tags.insert(0, "touche")
                if "down" in objects[element].tags and stats_perso["inLongDown"]:
                    stats_perso["inLongDown"] = False
                    objects[element].tags.insert(0, "touche")
            if element in objects and isinstance(objects[element], Actif) and ("enemy" in objects[element].tags or "silence" in objects[element].tags) and "touche" not in objects[element].tags and "long" not in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["pers1"]):
                if "small" in objects[element].tags:
                    stats_perso["pv"] -= 20
                if "large" in objects[element].tags:
                    stats_perso["pv"] -= 30
                if "boss" in objects[element].tags:
                    stats_perso["pv"] -= 40
                    stats_perso["nbitems1"] += 1
                if "silence" in objects[element].tags:
                    stats_perso["pv"] -= 30
                
                if stats_perso["pv"] <= 0:
                    stats_perso["pv"] = 0
                    gameoverbool = True

                objects[element].tags.insert(0, "touche")
            if element in objects and isinstance(objects[element], Actif) and "itemnote" in objects[element].tags and objects[element].visible and \
                (objects["pers1"].visible and game.displaylist[element].colliderect(game.displaylist["pers1"]) or ("persophase3" in game.displaylist and game.displaylist[element].colliderect(game.displaylist["persophase3"])) or (objects["curseur"].visible and game.displaylist[element].colliderect(game.displaylist["curseur"])) or \
                    (objects["dedoublepersohaut"].visible and game.displaylist[element].colliderect(game.displaylist["dedoublepersohaut"])) or (objects["dedoublepersobas"].visible and game.displaylist[element].colliderect(game.displaylist["dedoublepersobas"]))):
                stats_perso["score"] += 1500
                # Compter note phase 1
                if levelelements["phase"][phaseindex-1][0] == "phase3":
                    stats_perso["notesphase3"] += 1
                else:
                    stats_perso["notesphase1"] += 1
                objects[element].visible = False
            if element in objects and isinstance(objects[element], Actif) and "itemcoeur" in objects[element].tags and objects[element].visible and \
                ((objects["pers1"].visible and game.displaylist[element].colliderect(game.displaylist["pers1"])) or ("persophase3" in game.displaylist and game.displaylist[element].colliderect(game.displaylist["persophase3"])) or (objects["curseur"].visible and game.displaylist[element].colliderect(game.displaylist["curseur"])) or\
                    (objects["dedoublepersohaut"].visible and game.displaylist[element].colliderect(game.displaylist["dedoublepersohaut"])) or (objects["dedoublepersobas"].visible and game.displaylist[element].colliderect(game.displaylist["dedoublepersobas"]))):
                stats_perso["pv"] += 75
                if stats_perso["pv"] > 200:
                    stats_perso["pv"] = 200
                objects[element].visible = False
                
            if element in objects and isinstance(objects[element], Actif) and "pique" in objects[element].tags and gameovertimer == 0 and ((objects["pers1"].visible and game.displaylist[element].colliderect(game.displaylist["pers1"])) or ("persophase3" in game.displaylist and game.displaylist[element].colliderect(game.displaylist["persophase3"]))):
                stats_perso["pv"] -= 2
                if stats_perso["pv"] <= 0:
                    stats_perso["pv"] = 0
                    gameoverbool = True

    if not gameoverbool and "persophase3" in game.displaylist:
        collidephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "cubebord" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"])]
        collidepiquephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "pique" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"])]


    perso_phase3["move"] = True
    perso_phase3["newposy"] = 0

    if (time.time() - gameovertimer) > 2 and gameovertimer != 0:
        if perso_phase3["reverse"]:
            objects["persophase3"].sprites["anim1"][0] = pygame.transform.flip(objects["persophase3"].sprites["anim1"][0], 0, 1)
        game.scenecourante = "gameover"
        camera = [0, 0]
    if not pause and gameovertimer == 0:
        camera[0] = pygame.mixer.music.get_pos()*vitessecam/1000
    if objects["curseur"].visible and not pause:
        if calques[1]["curseur"][1] <= 460 and calques[1]["curseur"][1] >= 65:
            calques[1]["curseur"][1] = pygame.mouse.get_pos()[1]
            pygame.mouse.set_pos([142, calques[1]["curseur"][1]])
        elif calques[1]["curseur"][1] > 460:
            calques[1]["curseur"][1] = 460
            pygame.mouse.set_pos([142, 460])
        else :
            calques[1]["curseur"][1] = 65
            pygame.mouse.set_pos([142, 65])

    if longboss:
        calques[1]["pers1"][1] = 190

    if longphase2:
        collidephase2 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Line) and game.displaylist[element].colliderect(game.displaylist["curseur"])]
        if collidephase2:
            stats_perso["score"] += 5
        else:
            longphase2 = False


    for phaseindex in range(len(levelelements["phase"])):
        if gameovertimer == 0:
            if pygame.mixer.music.get_pos() < levelelements["phase"][phaseindex][1]:
                if levelelements["phase"][phaseindex-1][0] == "phase0":
                    game.stats_perso.update(stats_perso)
                    game.scenecourante = "victoire"
                    camera = [0, 0]
                    gameovertimer = 0
                if levelelements["phase"][phaseindex-1][0] == "phase1":
                    objects["portee_haut"].visible = False
                    objects["portee_bas"].visible = False
                    objects["ligne"].visible = False
                    objects["sol"].visible = True
                    objects["solbis"].visible = True
                    objects["solhaut"].visible = False
                    objects["solbishaut"].visible = False
                    objects["cible_haut"].visible = True
                    objects["cible_bas"].visible = True
                    objects["curseur"].visible = False
                    objects["persophase3"].visible = False
                    objects["pers1"].visible = True
                    if not longboss:
                        if pos_pers == 0:
                            if stats_perso["inLongDown"]:
                                calques[1]["pers1"][1] = 280
                                objects["dedoublepersohaut"].visible = True
                            else:
                                calques[1]["pers1"][1] = 100
                                objects["dedoublepersohaut"].visible = False
                        else:
                            if stats_perso["inLongUp"]:
                                calques[1]["pers1"][1] = 100
                                objects["dedoublepersobas"].visible = True
                            else:
                                calques[1]["pers1"][1] = 280
                                objects["dedoublepersobas"].visible = False
                    calques[1]["pers1"][0] = 50
                    pygame.mouse.set_visible(True)
                elif levelelements["phase"][phaseindex-1][0] == "phase2" and not pause:
                    objects["portee_haut"].visible = True
                    objects["portee_bas"].visible = True
                    objects["ligne"].visible = True
                    objects["sol"].visible = False
                    objects["persophase3"].visible = False
                    objects["pers1"].visible = False
                    objects["solbis"].visible = False
                    objects["solhaut"].visible = False
                    objects["solbishaut"].visible = False
                    objects["cible_haut"].visible = False
                    objects["cible_bas"].visible = False
                    objects["curseur"].visible = True
                    pygame.mouse.set_visible(False)
                    
                elif levelelements["phase"][phaseindex-1][0] == "phase3" and not pause:
                    objects["portee_haut"].visible = False
                    objects["portee_bas"].visible = False
                    objects["ligne"].visible = False
                    objects["persophase3"].visible = True
                    objects["pers1"].visible = False
                    objects["sol"].visible = True
                    objects["solbis"].visible = True
                    objects["solhaut"].visible = True
                    objects["solbishaut"].visible = True
                    objects["cible_haut"].visible = False
                    objects["cible_bas"].visible = False
                    objects["curseur"].visible = False
                    pygame.mouse.set_visible(True)
                break
            elif phaseindex == len(levelelements["phase"])-1:
                if levelelements["phase"][phaseindex][0] == "phase0":
                    game.stats_perso.update(stats_perso)
                    game.scenecourante = "victoire"
                    camera = [0, 0]
                    gameovertimer = 0
                if levelelements["phase"][phaseindex][0] == "phase1":
                    objects["portee_haut"].visible = False
                    objects["portee_bas"].visible = False
                    objects["ligne"].visible = False
                    objects["sol"].visible = True
                    objects["solbis"].visible = True
                    objects["solhaut"].visible = False
                    objects["solbishaut"].visible = False
                    objects["cible_haut"].visible = True
                    objects["persophase3"].visible = False
                    objects["pers1"].visible = True
                    objects["cible_bas"].visible = True
                    objects["curseur"].visible = False
                    if not longboss:
                        if pos_pers == 0:
                            if stats_perso["inLongUp"]:
                                calques[1]["pers1"][1] = 280
                                objects["dedoublepersobas"].visible = True
                            else:
                                calques[1]["pers1"][1] = 100
                                objects["dedoublepersobas"].visible = False
                        else:
                            if stats_perso["inLongDown"]:
                                calques[1]["pers1"][1] = 100
                                objects["dedoublepersohaut"].visible = True
                            else:
                                calques[1]["pers1"][1] = 280
                                objects["dedoublepersohaut"].visible = False
                    calques[1]["pers1"][0] = 50
                    pygame.mouse.set_visible(True)
                elif levelelements["phase"][phaseindex][0] == "phase2"  and not pause:
                    objects["portee_haut"].visible = True
                    objects["portee_bas"].visible = True
                    objects["ligne"].visible = True
                    objects["sol"].visible = False
                    objects["solbis"].visible = False
                    objects["solhaut"].visible = False
                    objects["solbishaut"].visible = False
                    objects["cible_haut"].visible = False
                    objects["cible_bas"].visible = False
                    objects["persophase3"].visible = False
                    objects["pers1"].visible = True
                    objects["curseur"].visible = True
                    pygame.mouse.set_visible(False)
                    
                elif levelelements["phase"][phaseindex][0] == "phase3" and not pause:
                    objects["portee_haut"].visible = False
                    objects["portee_bas"].visible = False
                    objects["ligne"].visible = False
                    objects["persophase3"].visible = True
                    objects["pers1"].visible = False
                    objects["sol"].visible = True
                    objects["solbis"].visible = True
                    objects["solhaut"].visible = True
                    objects["solbishaut"].visible = True
                    objects["cible_haut"].visible = False
                    objects["cible_bas"].visible = False
                    objects["curseur"].visible = False
                    pygame.mouse.set_visible(True)
                break

    if gameoverbool == True:
        pygame.mixer.music.stop()
        objects["gameoverscreen"].visible = True
        gameovertimer = time.time()
        gameoverbool = False

    if not objects["gameoverscreen"].visible and "persophase3" in game.displaylist and not perso_phase3["dash"] and not pause:
        if perso_phase3["jumpCount"] > -11:
            perso_phase3["jumpCount"] -= 0.5
        if not perso_phase3["reverse"]:
            collidephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "cubebord" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"].move(0, -(perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3))]
            if calques[1]["persophase3"][1] - (perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3 > 350:
                calques[1]["persophase3"][1] = 350
                perso_phase3["jumpCount"] = 0
                perso_phase3["isJump"] = False
                if objects["persophase3"].animCourante != "marche":
                    objects["persophase3"].changeAnimation("marche")
            if collidephase3:
                if game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).top > game.displaylist["persophase3"].centery :
                    calques[1]["persophase3"][1] = game.displaylist[collidephase3[-1]].top - 74
                    perso_phase3["jumpCount"] = 0
                    perso_phase3["isJump"] = False
                    if objects["persophase3"].animCourante != "marche":
                        objects["persophase3"].changeAnimation("marche")
                elif game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).left > game.displaylist["persophase3"].centerx and game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).height > 30:
                    gameoverbool = True
                else:
                    calques[1]["persophase3"][1] = game.displaylist[collidephase3[-1]].bottom
                    perso_phase3["jumpCount"] = 0

            else:
                perso_phase3["isJump"] = True
                calques[1]["persophase3"][1] -= (perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3

        else:
            collidephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "cubebord" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"].move(0, (perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3))]
            if calques[1]["persophase3"][1] + (perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3 < 116:
                calques[1]["persophase3"][1] = 116
                perso_phase3["jumpCount"] = 0
                perso_phase3["isJump"] = False
                if objects["persophase3"].animCourante != "marche":
                    objects["persophase3"].changeAnimation("marche")
            if collidephase3:
                if game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).top > game.displaylist["persophase3"].centery :
                    calques[1]["persophase3"][1] = game.displaylist[collidephase3[-1]].top - 74
                    perso_phase3["jumpCount"] = 0
                elif game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).left > game.displaylist["persophase3"].centerx and game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).height > 30:
                    gameoverbool = True
                else:
                    calques[1]["persophase3"][1] = game.displaylist[collidephase3[-1]].bottom
                    perso_phase3["jumpCount"] = 0
                    perso_phase3["isJump"] = False
                    if objects["persophase3"].animCourante != "marche":
                        objects["persophase3"].changeAnimation("marche")
            else:
                perso_phase3["isJump"] = True
                calques[1]["persophase3"][1] += (perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3

        if calques[1]["persophase3"][1] < 116:
            calques[1]["persophase3"][1] = 116
            perso_phase3["jumpCount"] = 0

        if calques[1]["persophase3"][1] > 350:
            calques[1]["persophase3"][1] = 350
            perso_phase3["jumpCount"] = 0

    if perso_phase3["dash"]:
        calques[1]["persophase3"][1] = perso_phase3["posydash"]
        calques[3][perso_phase3["objectdash"]][0] = camera[0] + calques[1]["persophase3"][0] - 10

    

def loopafterupdate():
    global pause, gameovertimer, camera, collidephase3, collidemortphase3, collideorbephase3, collidepiquephase3, collidegroundphase3, gameoverbool, longboss, vitessecam
    objects["pause"].activate(game.displaylist["pause"])
    if objects["play"].visible:
        objects["play"].activate(game.displaylist["play"])
    if objects["retour"].visible:
        objects["retour"].activate(game.displaylist["retour"])
    if objects["recommencer"].visible:
        objects["recommencer"].activate(game.displaylist["recommencer"])

    for element in game.displaylist:
        if element in objects and isinstance(objects[element], Actif) and "boss" in objects[element].tags:
            if "hit" in objects[element].tags:
                calques[3][element][0] = ((float(element[4:]))*vitessecam/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 200
            elif "bosslong" in objects[element].tags:
                if pygame.mixer.music.get_pos()-float(element[4:]) < 0:
                    calques[3][element][0] = ((float(element[4:]))*vitessecam/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 200
                elif pygame.mixer.music.get_pos()-float(objects[element].tags[-1]) < 0:
                    objects[element].suivreScene = True
                    calques[3][element][0] = 200
                else:
                    longboss = False
                    objects[element].tags.insert(0, "finlong")
                    objects[element].suivreScene = True
                    calques[3][element][0] -= 40

    
    if game.displaylist["premierFond"].right <= 0:
        calques[0]["premierFond"][0] += 1920
    if game.displaylist["premierFondbis"].right <= 0:
        calques[0]["premierFondbis"][0] += 1920
    if game.displaylist["deuxiemeFond"].right <= 0:
        calques[0]["deuxiemeFond"][0] += 1920
    if game.displaylist["deuxiemeFondbis"].right <= 0:
        calques[0]["deuxiemeFondbis"][0] += 1920
    if game.displaylist["troisiemeFond"].right <= 0:
        calques[0]["troisiemeFond"][0] += 1920
    if game.displaylist["troisiemeFondbis"].right <= 0:
        calques[0]["troisiemeFondbis"][0] += 1920
    if game.displaylist["quatriemeFond"].right <= 0:
        calques[0]["quatriemeFond"][0] += 1920
    if game.displaylist["quatriemeFondbis"].right <= 0:
        calques[0]["quatriemeFondbis"][0] += 1920
    if "sol" in game.displaylist:
        if game.displaylist["solbis"].right <= 0:
            calques[0]["solbis"][0] += 1920
        if game.displaylist["sol"].right <= 0:
            calques[0]["sol"][0] += 1920
    if "solhaut" in game.displaylist:
        if game.displaylist["solbishaut"].right <= 0:
            calques[0]["solbishaut"][0] += 1920
        if game.displaylist["solhaut"].right <= 0:
            calques[0]["solhaut"][0] += 1920