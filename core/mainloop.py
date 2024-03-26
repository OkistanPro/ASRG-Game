import pygame
import pygame.freetype
from pygame.locals import *

from classes import *
import game

while game.active:
    game.ecran.fill("black")

    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False
            pygame.display.quit()
            pygame.quit()

        if event.type == KEYDOWN and event.key == K_a:
            game.luigi.changeAnimation("attack")
        if event.type == KEYDOWN and event.key == K_RIGHT:
            game.scenes[game.scenecourante].camera[0] += 10

        if event.type == game.luigi.END_ANIMATION and event.animation == "attack":
            game.luigi.changeAnimation("idle")

        game.button1.activate(event, game.scenes[game.scenecourante].camera)
        game.button2.activate(event, game.scenes[game.scenecourante].camera)

    game.text01.text = str(game.scenecourante)
    game.update()

    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)