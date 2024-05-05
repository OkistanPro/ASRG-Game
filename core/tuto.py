import pygame
from pygame.locals import *
from pathlib import PurePath
from classes import *
import game
import os

camera = [0, 0]

fond = (0, 0, 0)

objects = {}

calques = {}

cptanim = 0

def init():
    global camera, fond, objects, calques
    objects.update({
        "imagetuto" : Actif(
            {
                key : value for key, value in zip([namefond[:-4] for namefond in os.listdir(PurePath("images/interface/tuto"))], [[PurePath("images/interface/tuto/" + namefond)] for namefond in os.listdir(PurePath("images/interface/tuto"))])
            },
            {
                key : [False, 1] for key in [namefond[:-4] for namefond in os.listdir(PurePath("images/interface/tuto"))]
            },
            "tuto0"
        ),
        "changetheme" : Actif(
            {"anim1" : [PurePath("images/level/animation/changetheme/" + str(i) + ".png") for i in range(6)]},
            {"anim1" : [False, 1]},
            "anim1"
        )
    })

    calques.update({
        0:{
            "imagetuto" : [0, 0],
            "changetheme" : [0, 0]
        }
    })

def loopevent(event):
    global cptanim, calques, objects
    if event.type == KEYDOWN and event.key == K_RETURN:
        if cptanim < 10:
            cptanim +=1
            objects["changetheme"].changeAnimation("anim1")
            objects["imagetuto"].changeAnimation("tuto"+str(cptanim))
            game.selectsound.play()
        else:
            filelines = []
            with open("save.asrg", "r") as filesave:
                filelines = filesave.readlines()
            
            filelines[3] = "TUTORIEL\t1\n"
            with open("save.asrg", "w") as filesave:
                filesave.writelines(filelines)
                

            game.selectsound.play()
            game.scenecourante = "selectionniveau"

def loopbeforeupdate():
    pass

def loopafterupdate():
    pass