import pygame
#from pygame_geometry.curves import BezierCurve
from pygame.locals import *
from pathlib import PurePath
import levelfiles.levelmaker as levelmaker
from classes import *
import createcube

import game

import time

import copy

stats_perso = {
    "score" : 0,
    "pv" : 200,

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

    "passphase2" : 0
}

camera = [0, 0]
vitessecam = 600
mousesave = None
fond = (0, 0, 0)
pos_pers = 1

pause = 0
button = 0
gameoverbool = False
gameovertimer = 0

flagliee = False
autreliee = False
positionliee = [0, 0]
intervallecourant = [0, 0]

timesave = 0
flagtimesave = True

phaseindex = 0

mapphase3 = {}

perso_phase3 = {
    "jumpCount" : 0,
    "isJump" : False,
    "reverse" : False,
    "dash" : False,
    "objectdash" : "",
    "posydash" : 0
}

collidephase3 = []
collidemortphase3 = []
collideorbephase3 = []
collidepiquephase3 = []
collidegroundphase3 = []

objects = {"bandeau_haut" : Actif(
    {"bandeau_haut" : [PurePath("images/interface/bandeau.png")]},
    {"bandeau_haut" : [True, 1]}, #Ne change rien car image fixe
    "bandeau_haut"
),
"bandeau_bas" : Actif(
    {"bandeau_bas" : [PurePath("images/interface/bandeau.png")]},
    {"bandeau_bas" : [True, 1]},
    "bandeau_bas"
),
"pers1" : Actif(
    {"debout" : [PurePath("images/level/personnage.png")]},
    {"debout" : [True, 5]}, #Au hazard
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
    ], "play" : [
        [PurePath("images/interface/boutonplay.png")],
        [PurePath("images/interface/boutonplay.png")],
        [PurePath("images/interface/boutonplay.png")],
        [PurePath("images/interface/boutonplay.png")],
        [PurePath("images/interface/boutonplay.png")]
    ]},
    {"pause" : [
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5],
        [False, 0, 5]
    ], "play" : [
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
        "anim1" : [PurePath("images/fonds/premierPlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"premierFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/premierPlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"deuxiemeFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/deuxiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"deuxiemeFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/deuxiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"troisiemeFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/troisiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"troisiemeFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/troisiemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"quatriemeFond" : Actif(
    {
        "anim1" : [PurePath("images/fonds/quatriemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"quatriemeFondbis" : Actif(
    {
        "anim1" : [PurePath("images/fonds/quatriemePlan.png")]
    },
    {"anim1" : [True, 5]},
    "anim1"
),
"sol" : Actif(
    {"anim1" : [PurePath("images/fonds/sol.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"solbis" : Actif(
    {"anim1" : [PurePath("images/fonds/sol.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"solhaut" : Actif(
    {"anim1" : [PurePath("images/fonds/sol.png")]},
    {"anim1" : [False, 5]},
    "anim1"
),
"solbishaut" : Actif(
    {"anim1" : [PurePath("images/fonds/sol.png")]},
    {"anim1" : [False, 5]},
    "anim1"
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
    {"anim1" : [PurePath("images/level/persophase3.png")]},
    {"anim1" : [False, 5]},
    "anim1"
)
}

objects["premierFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["premierFondbis"].sprites["anim1"][0], 1, 0)
objects["deuxiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["deuxiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["troisiemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["troisiemeFondbis"].sprites["anim1"][0], 1, 0)
objects["quatriemeFondbis"].sprites["anim1"][0] = pygame.transform.flip(objects["quatriemeFondbis"].sprites["anim1"][0], 1, 0)
objects["solhaut"].sprites["anim1"][0] = pygame.transform.flip(objects["solhaut"].sprites["anim1"][0], 0, 1)
objects["solbishaut"].sprites["anim1"][0] = pygame.transform.flip(objects["solbishaut"].sprites["anim1"][0], 0, 1)


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
            "ligne" : [171 - (objects["ligne"].sprites["anim1"][0].get_rect().width / 2), 0],
            "curseur" : [130, 235],
            "persophase3" : [50, 350],
            "pers1" : [50, 280]
        },
        2:{},
        "border":{},
        3:{},
        4:{
            "fondpause" : [0, 0],
            "bandeau_haut" : [0, 0], 
            "bandeau_bas" : [0, 470], 
            "cadreProgression" : [480 - (objects["cadreProgression"].sprites["anim1"][0].get_rect().width / 2), 492],
            "cadrePV" : [480 - (objects["cadrePV"].sprites["anim1"][0].get_rect().width / 2), 7], 
            "jaugeProgression" : [480 - (objects["jaugeProgression"].sprites["anim1"][0].get_rect().width / 2), 497], 
            "jaugeRougePV" : [480 - (objects["jaugeRougePV"].sprites["anim1"][0].get_rect().width / 2), 11], 
            "jaugeVertPV" : [480 - (objects["jaugeVertPV"].sprites["anim1"][0].get_rect().width / 2), 11], 
            "PV" : [480 - (objects["PV"].renderText().get_rect().width / 2), 10], 
            "score" : [10, 40],
            "numscore" : [10, 10],
            "combo" : [480 - (objects["combo"].renderText().get_rect().width / 2), 40],
            "pause" : [890, 0]
        }}

calques = copy.deepcopy(initcalques)

levelelements = levelmaker.getelements(PurePath("levelfiles/testniveau3.csv"))



"""
matricephase3 = [[0], [0], [0], [0], [0], [0]]

for element in levelelements["cube"]:
    linematrice = [[0], [0], [0], [0], [0], [0]]
    linematrice[element[0]].append([0, element[1]])
    matricephase3 = numpy.stack((matricephase3, linematrice), axis=0)

print(matricephase3)
"""
def creerCoeur(temps, posy):
    global objects, calques
    objects["coeur"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/coeurRouge.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "coeur"]
    )
    calques[3]["coeur"+str(temps)] = [(temps * 600 / 1000) + 150, posy]
    
def creerNote(temps, posy) :
    objects["note"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/note.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "note"]
    )
    calques[3]["note"+str(temps)] = [(temps * 600 / 1000) + 150, posy]

def creerSmall(temps, placement) :
    if placement == "up":
        objects["smallu"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/placeholder/small.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "small"]
        )
        calques[3]["smallu"+str(temps)] = [(temps * 600 / 1000) + 150, 160]
        if temps in levelelements["small"]['down']:
            objects["double"+str(temps)] = Actif(
            {"anim1" : [PurePath("images/level/barredouble.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "elementup", "double"]
            )
            calques[3]["double"+str(temps)] = [(temps * 600 / 1000) + 150, 210]
    elif placement == "down":
        objects["smalld"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/placeholder/small.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementdown", "small"]
        )
        calques[3]["smalld"+str(temps)] = [(temps * 600 / 1000) + 150, 340]

def creerLarge(temps, placement) :
    if placement == "up":
        objects["large"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "large"]
        )
        calques[3]["large"+str(temps)] = [(temps * 600 / 1000) + 150, 135]
    if placement == "down":
        objects["large"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/placeholder/large.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementdown", "large"]
        )
        calques[3]["large"+str(temps)] = [(temps * 600 / 1000) + 150, 315]

def creerLong(temps, placement) :
    if placement == "up":
        objects["longstart"+str(temps[0])] = Actif(
            {"anim1" : [PurePath("images/level/placeholder/longd.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "long", "start", "up"]
        )
        objects["longend"+str(temps[1])] = Actif(
            {"anim1" : [PurePath("images/level/placeholder/longf.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "long", "end", "up"]
        )
        objects["longmiddle"+str(temps[0])] = Actif(
            {"anim1" : [PurePath("images/level/placeholder/longm.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "long", "middle", "up"]
        )
                            
        objects["longmiddle"+str(temps[0])].taillex = (((temps[1] * 600 / 1000) + 100) - ((temps[0] * 600 / 1000) + 200)) / 50
        calques[3]["longstart"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150, 160]
        calques[3]["longmiddle"+str(temps[0])] = [(temps[0] * 600 / 1000) + 200, 160]
        calques[3]["longend"+str(temps[1])] = [(temps[1] * 600 / 1000) + 100, 160]
    elif placement == "down":
        objects["longstart"+str(temps[0])] = Actif(
            {"anim1" : [PurePath("images/level/placeholder/longd.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "long", "start", "down"]
            )
        objects["longend"+str(temps[1])] = Actif(
            {"anim1" : [PurePath("images/level/placeholder/longf.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "long", "end", "down"]
            )
        objects["longmiddle"+str(temps[0])] = Actif(
            {"anim1" : [PurePath("images/level/placeholder/longm.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "long", "middle", "down"]
            )
        objects["longmiddle"+str(temps[0])].taillex = (((temps[1] * 600 / 1000) + 100) - ((temps[0] * 600 / 1000) + 200)) / 50
        calques[3]["longstart"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150, 340]
        calques[3]["longmiddle"+str(temps[0])] = [(temps[0] * 600 / 1000) + 200, 340]
        calques[3]["longend"+str(temps[1])] = [(temps[1] * 600 / 1000) + 100, 340]

def creerBoss(temps, typeelement) :
    if typeelement == "hit":
        objects["boss"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/boss.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "boss", "hit"]
        )
        calques[3]["boss"+str(temps)] = [(temps * 600 / 1000) + 420, 100]
    elif typeelement == "long":
        objects["boss"+str(temps[0])] = Actif(
        {"anim1" : [PurePath("images/level/boss.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "boss", "long", str(temps[1])]
        )
        calques[3]["boss"+str(temps[0])] = [(temps[0] * 600 / 1000) + 420, 100]

def creerFantome(temps, typeelement) :
    if typeelement == "up":
        objects["fantome"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/fantome.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "fantome"]
        )
        calques[3]["fantome"+str(temps)] = [(temps * 600 / 1000) + 150, 160]
    elif typeelement == "down":
        objects["fantome"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/fantome.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementdown", "fantome"]
        )
        calques[3]["fantome"+str(temps)] = [(temps * 600 / 1000) + 150, 340]

def creerNotePhase2(temps, element, note, offsetx, offsety) :
    global flagliee, autreliee, positionliee, intervallecourant
    precision = levelmaker.precision
    if temps[1]-temps[0] <= 8*precision:
        objects["noire"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/noire.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "noire", element, str(temps[1])]
            )
        calques[3]["noire"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150, note]
        if temps[1]-temps[0] <= 2*precision:
            objects["dblcroche"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/doublecroche.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "dblcroche"]
            )
            if offsety==0:
                objects["dblcroche"+str(temps[0])].sprites["anim1"][0] = pygame.transform.flip(objects["dblcroche"+str(temps[0])].sprites["anim1"][0], 0, 1)
            calques[2]["dblcroche"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150 + offsetx, note - offsety]
        elif temps[1]-temps[0] <= 4*precision:
            objects["croche"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/croche.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "croche"]
            )
            if offsety==0:
                objects["croche"+str(temps[0])].sprites["anim1"][0] = pygame.transform.flip(objects["croche"+str(temps[0])].sprites["anim1"][0], 0, 1)
            calques[2]["croche"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150 + offsetx, note - offsety]
        else:
            objects["lignenote"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/lignenote.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "lignenote"]
            )
            calques[2]["lignenote"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150 + offsetx, note - offsety]
    elif temps[1]-temps[0] <= 16*precision:
        objects["blanche"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/blanche.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "blanche", element, str(temps[1])]
            )
        objects["lignenote"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/lignenote.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "lignenote"]
            )
        objects["line"+str(temps[0])] = Line(
                    0, 
                    0, 
                    (temps[1]-temps[0])*600/1000,
                    0,
                    (255, 255, 255), 
                    5, 
                    lueurBool=True, 
                    couleurlueur=(0, 255, 0)
                )
        calques[2]["lignenote"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150 + offsetx, note - offsety]
        calques[3]["line"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150, note + 15]
        calques[3]["blanche"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150, note]

    elif temps[1]-temps[0] <= 32*precision:
        objects["ronde"+str(temps[0])] = Actif(
                {"anim1" : [PurePath("images/level/ronde.png")]},
                {"anim1" : [False, 5]},
                "anim1",
                tags=["element", "ronde", element, str(temps[1])]
            )
        calques[3]["ronde"+str(temps[0])] = [(temps[0] * 600 / 1000) + 150, note]
    for intervalle in levelelements["liee"]["flagliee"]:
        if temps[0] >= intervalle[0] and temps[0] <= intervalle[1]:
            flagliee = True
        else:
            flagliee = False
            if intervalle != intervallecourant:
                continue
        if flagliee:
            if not autreliee:
                positionliee = [(temps[0] * 600 / 1000) + 150 + 15, note + 15]
                autreliee = True
                intervallecourant = intervalle
            else:
                objects["liee"+str(temps[0])] = Line(
                    0, 
                    0, 
                    (temps[0] * 600 / 1000) + 150 + 15 - positionliee[0],
                    note + 15 - positionliee[1],
                    (255, 255, 255), 
                    5, 
                    lueurBool=True, 
                    couleurlueur=(0, 255, 0)
                )
                calques[3]["liee"+str(temps[0])] = positionliee
                positionliee = [(temps[0] * 600 / 1000) + 150 + 15, note + 15]
        else:
            autreliee = False

def creerSilence(temps, placement) :
    if placement == "up":
        objects["silence"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/silence.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementup", "silence"]
        )
        calques[3]["silence"+str(temps)] = [(temps * 600 / 1000) + 150, 125]
    elif placement == "middle":
        objects["silence"+str(temps)] = Actif(
            {"anim1" : [PurePath("images/level/silence.png")]},
            {"anim1" : [False, 5]},
            "anim1",
            tags=["element", "elementup", "silence"]
        )
        calques[3]["silence"+str(temps)] = [(temps * 600 / 1000) + 150, 215]
    elif placement == "down":
        objects["silence"+str(temps)] = Actif(
        {"anim1" : [PurePath("images/level/silence.png")]},
        {"anim1" : [False, 5]},
        "anim1",
        tags=["element", "elementdown", "silence"]
        )
        calques[3]["silence"+str(temps)] = [(temps * 600 / 1000) + 150, 305]

def init():
    global calques, initcalques, camera, fond, pause, button, gameovertimer, levelelements, pos_pers, flagliee, autreliee, positionliee, gameoverbool, perso_phase3
    
    perso_phase3 = {
        "jumpCount" : 0,
        "isJump" : False,
        "reverse" : False,
        "dash" : False,
        "objectdash" : "",
        "posydash" : 0
    }
    
    gameoverbool = False
    perso_phase3["reverse"] = False
    collidephase3 = []

    pygame.mixer.music.load(PurePath("levelfiles/testniveau_music.wav"))
    pygame.mixer.music.play()
    # Setup les objets (changement des propriétés de chaque objet)
    
    calques = copy.deepcopy(initcalques)
    # print(init)
    #Tailles objets
    objects["pers1"].taillex = 0.5
    objects["pers1"].tailley = 0.5
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

    for object in calques[1]:
        objects[object].suivreScene = True

    for object in calques[4]:
        objects[object].suivreScene = True

    objects["fondpause"].visible = False
    objects["portee_haut"].visible = False
    objects["portee_bas"].visible = False
    objects["ligne"].visible = False
    objects["curseur"].visible = False
    
    objects["gameoverscreen"].visible = False
    objects["gameoverscreen"].suivreScene = True


    pygame.mouse.get_rel()
    objects["pause"].animCourante = "pause"
    objects["pause"].imageCourante = 0
    objects["pause"].cptframe = 0
    objects["fondpause"].visible = False
    pause = 0

    for element in levelelements:
        match element:
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

            case "items":
                for note in levelelements[element]:
                    match note:
                        case "C5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 432)
                        case "C#5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 382)
                        case "D5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 332)
                        case "D#5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 282)
                        case "E5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 232)
                        case "F5":
                            for time in levelelements[element][note]:
                                creerCoeur(time, 182)
                        case "C6":
                            for time in levelelements[element][note]:
                                creerNote(time, 432)
                        case "C#6":
                            for time in levelelements[element][note]:
                                creerNote(time, 382)
                        case "D6":
                            for time in levelelements[element][note]:
                                creerNote(time, 332)
                        case "D#6":
                            for time in levelelements[element][note]:
                                creerNote(time, 282)
                        case "E6":
                            for time in levelelements[element][note]:
                                creerNote(time, 232)
                        case "F6":
                            for time in levelelements[element][note]:
                                creerNote(time, 182)
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
                            creerNotePhase2([note[1], note[2]], element, 388, 0, 0)
                        case "45" :
                            creerNotePhase2([note[1], note[2]], element, 376, 0, 0)
                        case "47" :
                            creerNotePhase2([note[1], note[2]], element, 365, 0, 0)
                        case "48" :
                            creerNotePhase2([note[1], note[2]], element, 353, 0, 0)
                        case "50" :
                            creerNotePhase2([note[1], note[2]], element, 341, 0, 0)
                        case "52" :
                            creerNotePhase2([note[1], note[2]], element, 330, 0, 0)
                        case "53" :
                            creerNotePhase2([note[1], note[2]], element, 319, 0, 0)
                        case "55" :
                            creerNotePhase2([note[1], note[2]], element, 307, 0, 0)
                        case "57" :
                            creerNotePhase2([note[1], note[2]], element, 296, 0, 0)
                        case "59" :
                            creerNotePhase2([note[1], note[2]], element, 281, 0, 0)
                        case "60" :
                            creerNotePhase2([note[1], note[2]], element, 252, 26, 70)
                        case "62" :
                            creerNotePhase2([note[1], note[2]], element, 221, 26, 70)
                        case "64" :
                            creerNotePhase2([note[1], note[2]], element, 208, 26, 70)
                        case "65" :
                            creerNotePhase2([note[1], note[2]], element, 196, 26, 70)
                        case "67" :
                            creerNotePhase2([note[1], note[2]], element, 185, 26, 70)
                        case "69" :
                            creerNotePhase2([note[1], note[2]], element, 173, 26, 70)
                        case "71" :
                            creerNotePhase2([note[1], note[2]], element, 161, 26, 70)
                        case "72" :
                            creerNotePhase2([note[1], note[2]], element, 161, 26, 70)
                        case "74" :
                            creerNotePhase2([note[1], note[2]], element, 139, 26, 70)
                        case "76" :
                            creerNotePhase2([note[1], note[2]], element, 127, 26, 70)
                        case "77" :
                            creerNotePhase2([note[1], note[2]], element, 116, 26, 70)
            case "silence":
                for time in levelelements[element]['up']:
                        creerSilence(time, "up")
                for time in levelelements[element]['middle']:
                        creerSilence(time, "middle")
                for time in levelelements[element]['down']:
                        creerSilence(time, "down")

            case "cube":
                keys = list(levelelements[element].values())
                i = 0
                adjcubes = []
                for time, poslist in levelelements[element].items():
                    for cube in range(len(poslist)):
                        if poslist[cube] == 1:
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
                            objects["cube"+str(cube)+str(float(time))].taillex = ((levelelements["mincube"]*600/1000))/50
                            objects["cubebord"+str(cube)+str(float(time))].taillex = ((levelelements["mincube"]*600/1000))/50
                            calques[3]["cube"+str(cube)+str(float(time))] = [(float(time) * 600 / 1000) + 150, 371-(50*(cube))]
                            calques["border"]["cubebord"+str(cube)+str(float(time))] = [(float(time) * 600 / 1000) + 145, 366-(50*(cube))]
                            i+=1

            case "pique":
                for time, poslist in levelelements[element].items():
                    for pique in range(len(poslist)):
                        if poslist[pique] == 1:
                            objects["pique"+str(pique)+str(float(time))] = Actif(
                            {"anim1" : [PurePath("images/level/pique.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["element", "pique"]
                            )
                            objects["pique"+str(pique)+str(float(time))].taillex = ((levelelements["mincube"]*600/1000))/50
                            if pique == 5 or (time in levelelements["cube"] and levelelements["cube"][time][pique+1]):
                                objects["pique"+str(pique)+str(float(time))].sprites["anim1"][0] = pygame.transform.flip(objects["pique"+str(pique)+str(float(time))].sprites["anim1"][0], 0, 1)
                            calques[3]["pique"+str(pique)+str(float(time))] = [(float(time) * 600 / 1000) + 150, 371-(50*(pique))]


            case "orbe":
                for time, poslist in levelelements[element].items():
                    for orbe in range(len(poslist[0])):
                        if poslist[0][orbe] == 1:
                            if int(poslist[1]) > 100:
                                objects["orbe"+str(orbe)+str(float(time))] = Actif(
                                {"anim1" : [PurePath("images/level/orbe_reverse.png")]},
                                {"anim1" : [False, 5]},
                                "anim1",
                                tags=["element", "orbe", "orbereverse"]
                                )
                                objects["orbe"+str(orbe)+str(float(time))].taillex = ((levelelements["mincube"]*600/1000))/50
                                calques[3]["orbe"+str(orbe)+str(float(time))] = [(float(time) * 600 / 1000) + 150, 371-(50*(orbe))]
                            else:
                                objects["orbe"+str(orbe)+str(float(time))] = Actif(
                                {"anim1" : [PurePath("images/level/orbe.png")]},
                                {"anim1" : [False, 5]},
                                "anim1",
                                tags=["element", "orbe", "orbesaut"]
                                )
                                objects["orbe"+str(orbe)+str(float(time))].taillex = ((levelelements["mincube"]*600/1000))/50
                                calques[3]["orbe"+str(orbe)+str(float(time))] = [(float(time) * 600 / 1000) + 150, 371-(50*(orbe))]

            
            case "dash":
                for time, poslist in levelelements[element].items():
                    for dash in range(len(poslist)):
                        if poslist[dash] == 1:
                            objects["dash"+str(dash)+str(float(time))] = Actif(
                            {"anim1" : [PurePath("images/level/dash.png")]},
                            {"anim1" : [False, 5]},
                            "anim1",
                            tags=["element", "dash"]
                            )
                            objects["dash"+str(dash)+str(float(time))].taillex = ((levelelements["mincube"]*600/1000))/50
                            calques[3]["dash"+str(dash)+str(float(time))] = [(float(time) * 600 / 1000) + 150, 371-(50*(dash))]


def loopevent(event):
    global calques, initcalques, camera, fond, pause, button, gameovertimer, mousesave, pos_pers, gameoverbool
    if event.type == KEYDOWN and event.key == K_f and gameovertimer == 0 and objects["curseur"].visible == False and pause != 1:
        pos_pers = 0
        

    if event.type == KEYDOWN and event.key == K_j and gameovertimer == 0 and objects["curseur"].visible == False and pause != 1:
        pos_pers = 1
        
    if (event.type == objects["pause"].CLICKED or (event.type == KEYDOWN and event.key == K_ESCAPE))\
        and gameovertimer == 0:
        if pause == 0:
            objects["pause"].animCourante = "play"
            objects["pause"].imageCourante = 0
            objects["pause"].cptframe = 0
            objects["fondpause"].visible = True
            pygame.mixer.music.pause()
            pause = 1
            pygame.mouse.set_visible(True)
        elif pause == 1:
            pygame.mouse.get_rel()
            objects["pause"].animCourante = "pause"
            objects["pause"].imageCourante = 0
            objects["pause"].cptframe = 0
            objects["fondpause"].visible = False
            pygame.mixer.music.unpause()
            pause = 0
    
    if (event.type == KEYDOWN and event.key == K_a):
            pygame.mixer.music.stop()
            objects["gameoverscreen"].visible = True
            gameovertimer = time.time()

    if event.type == KEYDOWN and event.key == K_v:
            game.scenecourante = "victoire"
            camera = [0, 0]
            pygame.mixer.music.stop()

    if event.type == KEYDOWN and event.key == K_SPACE:
        perso_phase3["jumpCount"] = 8
        perso_phase3["isJump"] = True
        collideorbephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "orbe" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"])]
        collidedashphase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "dash" in objects[element].tags and objects[element].visible and game.displaylist[element].colliderect(game.displaylist["persophase3"])]

        if collideorbephase3:
            perso_phase3["reverse"] = not perso_phase3["reverse"]
            objects["persophase3"].sprites["anim1"][0] = pygame.transform.flip(objects["persophase3"].sprites["anim1"][0], 0, 1)

        if collidedashphase3:
            perso_phase3["dash"] = True
            perso_phase3["objectdash"] = collidedashphase3[-1]
            perso_phase3["posydash"] = calques[1]["persophase3"][1]

    if event.type == KEYUP and event.key == K_SPACE:
        if perso_phase3["dash"]:
            perso_phase3["dash"] = False
            perso_phase3["jumpCount"] = 0
            objects[perso_phase3["objectdash"]].visible = False


def loopbeforeupdate():
    global pause, button, gameovertimer, camera, levelelements, pos_perso, vitessecam, phaseindex, timesave, flagtimesave, gameoverbool

    collidephase3 = []
    collidepiquephase3 = []


    if not gameoverbool:
        collidephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "cubebord" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"])]
        collidepiquephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "pique" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"])]


    perso_phase3["move"] = True
    perso_phase3["newposy"] = 0

    if (time.time() - gameovertimer) > 2 and gameovertimer != 0:
        if perso_phase3["reverse"]:
            objects["persophase3"].sprites["anim1"][0] = pygame.transform.flip(objects["persophase3"].sprites["anim1"][0], 0, 1)
        game.scenecourante = "gameover"
        camera = [0, 0]
        gameovertimer = 0
    if pause == 0 and gameovertimer == 0:
        camera[0] = pygame.mixer.music.get_pos()*vitessecam/1000 + timesave
    if objects["curseur"].visible and pause != 1:
        if calques[1]["curseur"][1] <= 460 and calques[1]["curseur"][1] >= 65:
            rel = pygame.mouse.get_rel()
            calques[1]["curseur"][1] += rel[1]
        elif calques[1]["curseur"][1] > 460:
            calques[1]["curseur"][1] = 460
        else :
            calques[1]["curseur"][1] = 65
        calques[1]["pers1"][1] = calques[1]["curseur"][1]-75
        pygame.mouse.set_pos([480, 270])
    for phaseindex in range(len(levelelements["phase"])):
        if pygame.mixer.music.get_pos() < levelelements["phase"][phaseindex][1]:
            if levelelements["phase"][phaseindex-1][0] == "phase1":
                vitessecam = 600
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
                if pos_pers == 0:
                    calques[1]["pers1"][1] = 100
                else:
                    calques[1]["pers1"][1] = 280
                calques[1]["pers1"][0] = 50
                pygame.mouse.set_visible(True)
            elif levelelements["phase"][phaseindex-1][0] == "phase2" and pause != 1:
                vitessecam = 600
                objects["portee_haut"].visible = True
                objects["portee_bas"].visible = True
                objects["ligne"].visible = True
                objects["sol"].visible = False
                objects["persophase3"].visible = False
                objects["pers1"].visible = True
                objects["solbis"].visible = False
                objects["solhaut"].visible = False
                objects["solbishaut"].visible = False
                objects["cible_haut"].visible = False
                objects["cible_bas"].visible = False
                objects["curseur"].visible = True
                pygame.mouse.set_visible(False)
                pygame.mouse.get_rel()
                calques[1]["pers1"][0] = 80
            elif levelelements["phase"][phaseindex-1][0] == "phase3" and pause != 1:
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
                for timephase in mapphase3:
                    if pygame.mixer.music.get_pos()*1000 >= float(timephase):
                        vitessecam = (1000/mapphase3[timephase][1]) * 50
                        break
            break
        elif phaseindex == len(levelelements["phase"])-1:
            if levelelements["phase"][phaseindex][0] == "phase1":
                vitessecam = 600
                objects["portee_haut"].visible = False
                objects["portee_bas"].visible = False
                objects["ligne"].visible = False
                objects["sol"].visible = True
                objects["solbis"].visible = True
                objects["cible_haut"].visible = True
                objects["persophase3"].visible = False
                objects["pers1"].visible = True
                objects["cible_bas"].visible = True
                objects["curseur"].visible = False
                if pos_pers == 0:
                    calques[1]["pers1"][1] = 100
                else:
                    calques[1]["pers1"][1] = 280
                calques[1]["pers1"][0] = 50
                pygame.mouse.set_visible(True)
            elif levelelements["phase"][phaseindex][0] == "phase2"  and pause != 1:
                vitessecam = 600
                objects["portee_haut"].visible = True
                objects["portee_bas"].visible = True
                objects["ligne"].visible = True
                objects["sol"].visible = False
                objects["solbis"].visible = False
                objects["cible_haut"].visible = False
                objects["cible_bas"].visible = False
                objects["persophase3"].visible = False
                objects["pers1"].visible = True
                objects["curseur"].visible = True
                pygame.mouse.set_visible(False)
                pygame.mouse.get_rel()
                calques[1]["pers1"][0] = 80
            elif levelelements["phase"][phaseindex][0] == "phase3" and pause != 1:
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
                for timephase in mapphase3:
                    if pygame.mixer.music.get_pos()*1000 >= float(timephase):
                        vitessecam = (1000/mapphase3[timephase][1]) * 50
                        break
                flagtimesave = False
            break

    if not flagtimesave:
        timesave = pygame.mixer.music.get_pos()*vitessecam/1000
        flagtimesave = True

    if gameoverbool == True:
        pygame.mixer.music.stop()
        objects["gameoverscreen"].visible = True
        gameovertimer = time.time()
        gameoverbool = False

    if not objects["gameoverscreen"].visible and objects["persophase3"].visible and not perso_phase3["dash"] and pause !=1:
        if perso_phase3["jumpCount"] > -11:
            perso_phase3["jumpCount"] -= 0.5
        if not perso_phase3["reverse"]:
            collidephase3 = [element for element in game.displaylist if element in objects and isinstance(objects[element], Actif) and "cubebord" in objects[element].tags and game.displaylist[element].colliderect(game.displaylist["persophase3"].move(0, -(perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3))]
            if calques[1]["persophase3"][1] - (perso_phase3["jumpCount"] * abs(perso_phase3["jumpCount"])) * 0.3 > 350:
                calques[1]["persophase3"][1] = 350
                perso_phase3["jumpCount"] = 0
                perso_phase3["isJump"] = False
            if collidephase3:
                if game.displaylist[collidephase3[-1]].clip(game.displaylist["persophase3"]).top > game.displaylist["persophase3"].centery :
                    calques[1]["persophase3"][1] = game.displaylist[collidephase3[-1]].top - 74
                    perso_phase3["jumpCount"] = 0
                    perso_phase3["isJump"] = False
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
        calques[3][perso_phase3["objectdash"]][0] += 10

def loopafterupdate():
    global pause, button, gameovertimer, camera, collidephase3, collidemortphase3, collideorbephase3, collidepiquephase3, collidegroundphase3, gameoverbool
    objects["pause"].activate(game.displaylist["pause"])

    for element in game.displaylist:
        if element in objects and isinstance(objects[element], Actif) and "boss" in objects[element].tags:
            if "hit" in objects[element].tags:
                calques[3][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 90
            elif "long" in objects[element].tags:
                if pygame.mixer.music.get_pos()-float(element[4:]) < 0:
                    calques[3][element][0] = ((float(element[4:]))*600/1000) - ((pygame.mixer.music.get_pos()-float(element[4:]))) + 90
                elif pygame.mixer.music.get_pos()-float(objects[element].tags[-1]) < 0:
                    objects[element].suivreScene = True
                    calques[3][element][0] = 90
                else:
                    objects[element].suivreScene = True
                    calques[3][element][0] -= 60
    
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
    if "solhaut" in game.displaylist:
        if game.displaylist["solbishaut"].right == 0:
            calques[0]["solbishaut"][0] += 1920
        if game.displaylist["solhaut"].right == 0:
            calques[0]["solhaut"][0] += 1920