import pygame
from pygame.locals import *

from classes import *
import game
import scene1, gameover, victoire, ecranTitre, selectionniveau, infoNiveau, chargement

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
            if isinstance(globals()[game.scenecourante].objects[objet], Actif) and globals()[game.scenecourante].objects[objet].visible:
                # On augmente son compteur d'animation
                globals()[game.scenecourante].objects[objet].cptframe += 1

                if not globals()[game.scenecourante].objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[game.scenecourante].objects[objet].renderActif(),
                        (globals()[game.scenecourante].objects[objet].taillex, globals()[game.scenecourante].objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0]-(globals()[game.scenecourante].camera[0]*globals()[game.scenecourante].objects[objet].parallax[0]),globals()[game.scenecourante].calques[calque][objet][1]-(globals()[game.scenecourante].camera[1]*globals()[game.scenecourante].objects[objet].parallax[1]))
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[game.scenecourante].objects[objet].renderActif(),
                        (globals()[game.scenecourante].objects[objet].taillex, globals()[game.scenecourante].objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0],globals()[game.scenecourante].calques[calque][objet][1])
                    )
            # Si l'objet est un Text
            if isinstance(globals()[game.scenecourante].objects[objet], Text) and globals()[game.scenecourante].objects[objet].visible:

                if not globals()[game.scenecourante].objects[objet].suivreScene:
                    if globals()[game.scenecourante].objects[objet].shadow:
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(globals()[game.scenecourante].objects[objet].renderShadow(), (globals()[game.scenecourante].calques[calque][objet][0]+globals()[game.scenecourante].objects[objet].sx-globals()[game.scenecourante].camera[0], globals()[game.scenecourante].calques[calque][objet][1]+globals()[game.scenecourante].objects[objet].sy-globals()[game.scenecourante].camera[1]))
                    game.displaylist[objet] = game.ecran.blit(globals()[game.scenecourante].objects[objet].renderText(), (globals()[game.scenecourante].calques[calque][objet][0]-globals()[game.scenecourante].camera[0], globals()[game.scenecourante].calques[calque][objet][1]-globals()[game.scenecourante].camera[1]))
                else:
                    if globals()[game.scenecourante].objects[objet].shadow:
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(globals()[game.scenecourante].objects[objet].renderShadow(), (globals()[game.scenecourante].calques[calque][objet][0]+globals()[game.scenecourante].objects[objet].sx, globals()[game.scenecourante].calques[calque][objet][1]+globals()[game.scenecourante].objects[objet].sy))
                    game.displaylist[objet] = game.ecran.blit(globals()[game.scenecourante].objects[objet].renderText(), (globals()[game.scenecourante].calques[calque][objet][0], globals()[game.scenecourante].calques[calque][objet][1]))


            # Si l'objet est un Bouton
            if isinstance(globals()[game.scenecourante].objects[objet], Bouton) and globals()[game.scenecourante].objects[objet].visible:
                # On augmente son compteur d'animation
                globals()[game.scenecourante].objects[objet].cptframe += 1

                if not globals()[game.scenecourante].objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[game.scenecourante].objects[objet].renderButton(),
                        (globals()[game.scenecourante].objects[objet].taillex, globals()[game.scenecourante].objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0]-globals()[game.scenecourante].camera[0],globals()[game.scenecourante].calques[calque][objet][1]-globals()[game.scenecourante].camera[1])
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        pygame.transform.scale_by(globals()[game.scenecourante].objects[objet].renderButton(),
                        (globals()[game.scenecourante].objects[objet].taillex, globals()[game.scenecourante].objects[objet].tailley)),
                        (globals()[game.scenecourante].calques[calque][objet][0],globals()[game.scenecourante].calques[calque][objet][1])
                    )
            
            #Si l'objet est une Line
            if isinstance(globals()[game.scenecourante].objects[objet], Line) and globals()[game.scenecourante].objects[objet].visible:
                if not globals()[game.scenecourante].objects[objet].suivreScene:
                    game.displaylist[objet] = game.ecran.blit(
                        globals()[game.scenecourante].objects[objet].renderLine(),
                        (globals()[game.scenecourante].calques[calque][objet][0]-globals()[game.scenecourante].camera[0] - 50,globals()[game.scenecourante].calques[calque][objet][1]-globals()[game.scenecourante].camera[1] - 50)
                    )
                else:
                    game.displaylist[objet] = game.ecran.blit(
                        globals()[game.scenecourante].objects[objet].renderLine(),
                        (globals()[game.scenecourante].calques[calque][objet][0]-50,globals()[game.scenecourante].calques[calque][objet][1]-50)
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

        globals()[game.scenecourante].loopevent(event)
    
    globals()[game.scenecourante].loopbeforeupdate()
    update()
    globals()[game.scenecourante].loopafterupdate()
    
    # L'horloge avance à 60 FPS
    game.horloge.tick(game.FPS)

pygame.display.quit()
pygame.quit()