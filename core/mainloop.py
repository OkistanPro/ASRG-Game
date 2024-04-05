import pygame
from pygame.locals import *

from classes import *
import game

from pathlib import PurePath

import keyboard

pause = 0
button = 0

while game.active:
    
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False

        
        if event.type == KEYDOWN and event.key == K_UP:
            game.objects["pers1"].posy = 100

        if event.type == KEYDOWN and event.key == K_DOWN:
            game.objects["pers1"].posy = 280
        
        if event.type == MOUSEBUTTONDOWN:
            print(event.pos)

        if event.type == game.objects["pause"].CLICKED and pause == 0 and button==0:
            game.objects["pause"].visible = False
            game.objects["play"].visible = True
            pause = 1
            button = 1

        if event.type == game.objects["play"].CLICKED and pause == 1 and button==0:
            game.objects["play"].visible = False
            game.objects["pause"].visible = True
            pause = 0
            button = 1
            

    button = 0
    if pause == 0:
        game.scenes[game.scenecourante].camera[0] += 10
    game.update()

    print(game.displaylist)
    # Activation des boutons
    if game.objects["play"].visible :
        game.objects["play"].activate(game.displaylist["play"])
    if game.objects["pause"].visible:
        game.objects["pause"].activate(game.displaylist["pause"])

    # Boucle de fond
    if game.displaylist["premierFond"].right == 0:
        game.objects["premierFond"].posx += 1920
    if game.displaylist["premierFondbis"].right == 0:
        game.objects["premierFondbis"].posx += 1920
    if game.displaylist["deuxiemeFond"].right == 0:
        game.objects["deuxiemeFond"].posx += 1920
    if game.displaylist["deuxiemeFondbis"].right == 0:
        game.objects["deuxiemeFondbis"].posx += 1920
    if game.displaylist["troisiemeFond"].right == 0:
        game.objects["troisiemeFond"].posx += 1920
    if game.displaylist["troisiemeFondbis"].right == 0:
        game.objects["troisiemeFondbis"].posx += 1920
    if game.displaylist["quatriemeFond"].right == 0:
        game.objects["quatriemeFond"].posx += 1920
    if game.displaylist["quatriemeFondbis"].right == 0:
        game.objects["quatriemeFondbis"].posx += 1920
    if game.displaylist["solbis"].right == 0:
        game.objects["solbis"].posx += 1920
    if game.displaylist["sol"].right == 0:
        game.objects["sol"].posx += 1920

    # L'horloge avance à 60 FPS
    game.horloge.tick_busy_loop(game.FPS)

pygame.display.quit()
pygame.quit()