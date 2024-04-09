import pygame
from pygame.locals import *

from classes import *
import game

from pathlib import PurePath

import keyboard
import time

pause = 0
button = 0
gameovertimer = 0

pygame.mixer.music.load(PurePath("levelfiles/testniveau_music.wav"))
pygame.mixer.music.play()

game.initscene1()


while game.active:
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False

        
        if event.type == KEYDOWN and event.key == K_f and gameovertimer == 0:
            game.scenes[game.scenecourante].calques[1]["pers1"][1] = 100

        if event.type == KEYDOWN and event.key == K_j and gameovertimer == 0:
            game.scenes[game.scenecourante].calques[1]["pers1"][1] = 280
        
        if event.type == MOUSEBUTTONDOWN:
            print(event.pos)

        if event.type == game.objects["pause"].CLICKED and game.scenecourante == "scene1" and gameovertimer == 0:
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

        if event.type == game.objects["replay"].CLICKED and game.scenecourante == "gameover":
            game.initscene1()
            game.scenecourante = "scene1"
            game.scenes[game.scenecourante].camera = [0, 0]
            pygame.mixer.music.play(start=0.0)

        if event.type == game.objects["rejouer"].CLICKED and game.scenecourante == "victoire":
            game.initscene1()
            game.scenecourante = "scene1"
            game.scenes[game.scenecourante].camera = [0, 0]
            pygame.mixer.music.play(start=0.0)

        if event.type == KEYDOWN and event.key == K_a:
            pygame.mixer.music.stop()
            game.objects["gameoverscreen"].visible = True
            gameovertimer = time.time()

        if event.type == KEYDOWN and event.key == K_v and game.scenecourante == "scene1":
            game.scenecourante = "victoire"
            game.scenes[game.scenecourante].camera = [0, 0]
            pygame.mixer.music.stop()

    if (time.time() - gameovertimer) > 5 and gameovertimer != 0:
        game.initgameover()
        game.scenecourante = "gameover"
        game.scenes[game.scenecourante].camera = [0, 0]
        gameovertimer = 0

    for element in game.displaylist:
        if element in game.objects and isinstance(game.objects[element], Actif) and "boss" in game.objects[element].tags and game.scenes["scene1"].calques[2][element][0]-(game.scenes["scene1"].camera[0]+960) < 0:
            game.scenes["scene1"].calques[2][element][0] -= 10
            
    if pause == 0 and game.scenecourante == "scene1" and gameovertimer == 0:
        game.scenes[game.scenecourante].camera[0] = pygame.mixer.music.get_pos()*600/1000
    game.update()

    # Activation des boutons
    if game.scenecourante == "scene1":
        game.objects["pause"].activate(game.displaylist["pause"])
    if game.scenecourante == "gameover":
        game.objects["replay"].activate(game.displaylist["replay"])
    if game.scenecourante == "victoire":
        game.objects["rejouer"].activate(game.displaylist["rejouer"])
    button = 0


    
    # Boucle de fond
    
    if game.displaylist["premierFond"].right == 0:
        game.scenes[game.scenecourante].calques[0]["premierFond"][0] += 1920
    if game.displaylist["premierFondbis"].right == 0:
        game.scenes[game.scenecourante].calques[0]["premierFondbis"][0] += 1920
    if game.displaylist["deuxiemeFond"].right == 0:
        game.scenes[game.scenecourante].calques[0]["deuxiemeFond"][0] += 1920
    if game.displaylist["deuxiemeFondbis"].right == 0:
        game.scenes[game.scenecourante].calques[0]["deuxiemeFondbis"][0] += 1920
    if game.displaylist["troisiemeFond"].right == 0:
        game.scenes[game.scenecourante].calques[0]["troisiemeFond"][0] += 1920
    if game.displaylist["troisiemeFondbis"].right == 0:
        game.scenes[game.scenecourante].calques[0]["troisiemeFondbis"][0] += 1920
    if game.displaylist["quatriemeFond"].right == 0:
        game.scenes[game.scenecourante].calques[0]["quatriemeFond"][0] += 1920
    if game.displaylist["quatriemeFondbis"].right == 0:
        game.scenes[game.scenecourante].calques[0]["quatriemeFondbis"][0] += 1920
    if game.displaylist["solbis"].right == 0:
        game.scenes[game.scenecourante].calques[0]["solbis"][0] += 1920
    if game.displaylist["sol"].right == 0:
        game.scenes[game.scenecourante].calques[0]["sol"][0] += 1920


    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()