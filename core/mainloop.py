import pygame
from pygame.locals import *

from classes import *
import game
import scene1, gameover, victoire, ecranTitre, selectionniveau, infoNiveau, chargement, parametres, ecran_touches, infoPerso

from pathlib import PurePath

#import keyboard
import time

sceneloop = ""


def update():
    game.displaylist["BACKGROUND"] = game.ecran.fill(globals()[sceneloop].fond)
    # Pour chaque calque de la scène courante
    for calque in globals()[sceneloop].calques:
        # Pour chaque objet du calque
        for objet in globals()[sceneloop].calques[calque]:
            # Si l'objet est un Actif
            if isinstance(globals()[sceneloop].objects[objet], Actif) and globals()[sceneloop].objects[objet].visible:
                # On augmente son compteur d'animation
                globals()[sceneloop].objects[objet].cptframe += 1

                if not globals()[sceneloop].objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderActif(),
                        (globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)),
                        (globals()[sceneloop].calques[calque][objet][0]-(globals()[sceneloop].camera[0]*globals()[sceneloop].objects[objet].parallax[0]),globals()[sceneloop].calques[calque][objet][1]-(globals()[sceneloop].camera[1]*globals()[sceneloop].objects[objet].parallax[1]))
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderActif(),
                        (globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)),
                        (globals()[sceneloop].calques[calque][objet][0],globals()[sceneloop].calques[calque][objet][1])
                    )
            # Si l'objet est un Text
            if isinstance(globals()[sceneloop].objects[objet], Text) and globals()[sceneloop].objects[objet].visible:

                if not globals()[sceneloop].objects[objet].suivreScene:
                    if globals()[sceneloop].objects[objet].shadow:
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(globals()[sceneloop].objects[objet].renderShadow(), (globals()[sceneloop].calques[calque][objet][0]+globals()[sceneloop].objects[objet].sx-globals()[sceneloop].camera[0], globals()[sceneloop].calques[calque][objet][1]+globals()[sceneloop].objects[objet].sy-globals()[sceneloop].camera[1]))
                    game.displaylist[objet] = game.ecran.blit(globals()[sceneloop].objects[objet].renderText(), (globals()[sceneloop].calques[calque][objet][0]-globals()[sceneloop].camera[0], globals()[sceneloop].calques[calque][objet][1]-globals()[sceneloop].camera[1]))
                else:
                    if globals()[sceneloop].objects[objet].shadow:
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(globals()[sceneloop].objects[objet].renderShadow(), (globals()[sceneloop].calques[calque][objet][0]+globals()[sceneloop].objects[objet].sx, globals()[sceneloop].calques[calque][objet][1]+globals()[sceneloop].objects[objet].sy))
                    game.displaylist[objet] = game.ecran.blit(globals()[sceneloop].objects[objet].renderText(), (globals()[sceneloop].calques[calque][objet][0], globals()[sceneloop].calques[calque][objet][1]))


            # Si l'objet est un Bouton
            if isinstance(globals()[sceneloop].objects[objet], Bouton) and globals()[sceneloop].objects[objet].visible:
                # On augmente son compteur d'animation
                globals()[sceneloop].objects[objet].cptframe += 1

                if not globals()[sceneloop].objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderButton(),
                        (globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)),
                        (globals()[sceneloop].calques[calque][objet][0]-globals()[sceneloop].camera[0],globals()[sceneloop].calques[calque][objet][1]-globals()[sceneloop].camera[1])
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderButton(),
                        (globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)),
                        (globals()[sceneloop].calques[calque][objet][0],globals()[sceneloop].calques[calque][objet][1])
                    )
            
            #Si l'objet est une Line
            if isinstance(globals()[sceneloop].objects[objet], Line) and globals()[sceneloop].objects[objet].visible:
                if not globals()[sceneloop].objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        globals()[sceneloop].objects[objet].renderLine(),
                        (globals()[sceneloop].calques[calque][objet][0]-globals()[sceneloop].camera[0] - 50,globals()[sceneloop].calques[calque][objet][1]-globals()[sceneloop].camera[1] - 50)
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        globals()[sceneloop].objects[objet].renderLine(),
                        (globals()[sceneloop].calques[calque][objet][0]-50,globals()[sceneloop].calques[calque][objet][1]-50)
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

        if event.type == MOUSEBUTTONDOWN:
            print(event.pos)

        globals()[sceneloop].loopevent(event)
    
    globals()[sceneloop].loopbeforeupdate()
    update()
    globals()[sceneloop].loopafterupdate()
    
    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()