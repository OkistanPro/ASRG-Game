import pygame
from pygame.locals import *

from classes import *
import game
import scene1, gameover, victoire

from pathlib import PurePath

#import keyboard
import time

sceneloop = ""


def update():
    game.displaylist["BACKGROUND"] = game.ecran.fill(globals()[game.scenecourante].fond)
    # Pour chaque calque de la scène courante
    for calque in globals()[game.scenecourante].calques:
        # Pour chaque objet du calque
        for objet in globals()[game.scenecourante].calques[calque]:
            # Si l'objet est un Actif
            if isinstance(game.objects[objet], Actif) and game.objects[objet].visible:
                # On augmente son compteur d'animation
                game.objects[objet].cptframe += 1

                if not game.objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(game.objects[objet].renderActif(),
                        (game.objects[objet].taillex, game.objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0]-(globals()[game.scenecourante].camera[0]*game.objects[objet].parallax[0]),globals()[game.scenecourante].calques[calque][objet][1]-(globals()[game.scenecourante].camera[1]*game.objects[objet].parallax[1]))
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(game.objects[objet].renderActif(),
                        (game.objects[objet].taillex, game.objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0],globals()[game.scenecourante].calques[calque][objet][1])
                    )
            # Si l'objet est un Text
            if isinstance(game.objects[objet], Text) and game.objects[objet].visible:

                if not game.objects[objet].suivreScene:
                    if game.objects[objet].shadow:
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(game.objects[objet].renderShadow(), (globals()[game.scenecourante].calques[calque][objet][0]+game.objects[objet].sx-globals()[game.scenecourante].camera[0], globals()[game.scenecourante].calques[calque][objet][1]+game.objects[objet].sy-globals()[game.scenecourante].camera[1]))
                    game.displaylist[objet] = game.ecran.blit(game.objects[objet].renderText(), (globals()[game.scenecourante].calques[calque][objet][0]-globals()[game.scenecourante].camera[0], globals()[game.scenecourante].calques[calque][objet][1]-globals()[game.scenecourante].camera[1]))
                else:
                    if game.objects[objet].shadow:
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(game.objects[objet].renderShadow(), (globals()[game.scenecourante].calques[calque][objet][0]+game.objects[objet].sx, globals()[game.scenecourante].calques[calque][objet][1]+game.objects[objet].sy))
                    game.displaylist[objet] = game.ecran.blit(game.objects[objet].renderText(), (globals()[game.scenecourante].calques[calque][objet][0], globals()[game.scenecourante].calques[calque][objet][1]))


            # Si l'objet est un Bouton
            if isinstance(game.objects[objet], Bouton) and game.objects[objet].visible:
                # On augmente son compteur d'animation
                game.objects[objet].cptframe += 1

                if not game.objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(game.objects[objet].renderButton(),
                        (game.objects[objet].taillex, game.objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0]-globals()[game.scenecourante].camera[0],globals()[game.scenecourante].calques[calque][objet][1]-globals()[game.scenecourante].camera[1])
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(game.objects[objet].renderButton(),
                        (game.objects[objet].taillex, game.objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0],globals()[game.scenecourante].calques[calque][objet][1])
                    )
    # On réactualise l'écran
    pygame.display.update()




while game.active:
    if sceneloop != game.scenecourante:
        globals()[game.scenecourante].init()
        sceneloop = game.scenecourante
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            game.active = False

        globals()[game.scenecourante].loopevent(event)
    
    globals()[game.scenecourante].loopbeforeupdate()
    update()
    globals()[game.scenecourante].loopafterupdate()
    
    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()