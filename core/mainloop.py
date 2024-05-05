import pygame
from pygame.locals import *

# Importation des objets du jeu et des variables globales
from classes import *
import game

# Importation des fichiers scènes
import scene1, gameover, victoire, ecranTitre, selectionniveau, infoNiveau, parametres, ecran_touches, infoPerso, tuto

from pathlib import PurePath
import shutil
import os

import time

# La scène en train d'être afficher
sceneloop = ""

# Procédure update() -> Affiche les objets à l'écran selon leurs propriété
def update():
    # On remplit en noir
    game.displaylist["BACKGROUND"] = game.ecran.fill(globals()[sceneloop].fond)
    # Pour chaque calque de la scène courante
    for calque in globals()[sceneloop].calques:
        # Pour chaque objet du calque
        for objet in globals()[sceneloop].calques[calque]:
            # Si l'objet est un Actif
            if isinstance(globals()[sceneloop].objects[objet], Actif) and globals()[sceneloop].objects[objet].visible:
                # On augmente son compteur d'animation
                globals()[sceneloop].objects[objet].cptframe += 1

                # S'il ne suit pas l'écran (et non la scène, problème de nommage des variables), la variable camera de la scène affecte la position de l'objet
                if not globals()[sceneloop].objects[objet].suivreScene:
                    # On applique l'objet sur l'écran en le mettant dans game.displaylist puis en faisant blit
                    game.displaylist[objet] = pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderActif(),(globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)).get_rect(topleft=(globals()[sceneloop].calques[calque][objet][0]-(globals()[sceneloop].camera[0]*globals()[sceneloop].objects[objet].parallax[0]),globals()[sceneloop].calques[calque][objet][1]-(globals()[sceneloop].camera[1]*globals()[sceneloop].objects[objet].parallax[1])))
                    if game.displaylist[objet].left <= 960 or game.displaylist[objet].right >= 0 or game.displaylist[objet].top <= 540 or game.displaylist[objet].bottom >= 0:
                        game.ecran.blit(pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderActif(),(globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)), game.displaylist[objet])
                else:
                    game.displaylist[objet] = pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderActif(),(globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)).get_rect(topleft=(globals()[sceneloop].calques[calque][objet][0],globals()[sceneloop].calques[calque][objet][1]))
                    if game.displaylist[objet].left <= 960 or game.displaylist[objet].right >= 0 or game.displaylist[objet].top <= 540 or game.displaylist[objet].bottom >= 0:
                        game.ecran.blit(pygame.transform.scale_by(globals()[sceneloop].objects[objet].renderActif(),(globals()[sceneloop].objects[objet].taillex, globals()[sceneloop].objects[objet].tailley)), game.displaylist[objet])

            # Si l'objet est un Text
            if isinstance(globals()[sceneloop].objects[objet], Text) and globals()[sceneloop].objects[objet].visible:
                # S'il ne suit pas l'écran 
                if not globals()[sceneloop].objects[objet].suivreScene:
                    # S'il y a une ombre
                    if globals()[sceneloop].objects[objet].shadow:
                        # Blit l'ombre avant le text
                        game.displaylist[objet+ "_SHADOW"] = game.ecran.blit(globals()[sceneloop].objects[objet].renderShadow(), (globals()[sceneloop].calques[calque][objet][0]+globals()[sceneloop].objects[objet].sx-globals()[sceneloop].camera[0], globals()[sceneloop].calques[calque][objet][1]+globals()[sceneloop].objects[objet].sy-globals()[sceneloop].camera[1]))
                    # Blit le texte
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



# Tant que la boucle de jeu est active
while game.active:
    # Si la scène courante a changé
    if sceneloop != game.scenecourante:
        # Lancer la fonction init de la scène courante
        globals()[game.scenecourante].init()
        # Effacer tout événement (le init peut prendre un certain temps)
        pygame.event.clear()
        # Indiquer à update d'afficher la scène courante
        sceneloop = game.scenecourante

    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Si le dossier level généré en lancant un niveau existe
            if os.path.exists("level"):
                # Le supprimer
                shutil.rmtree("level")
            # Fin de boucle, fermeture
            game.active = False

        # Si clic n'importe où
        if event.type == MOUSEBUTTONDOWN:
            # Afficher le x et y de la souris (debug)
            print(event.pos)

        # Tester les évènements de la scène
        globals()[sceneloop].loopevent(event)
    
    # Instructions de la scène avant le update
    globals()[sceneloop].loopbeforeupdate()

    # On affiche à l'écran
    update()

    # Instructions de la scène après le update
    globals()[sceneloop].loopafterupdate()
    
    # L'horloge avance au plus à 60 images par secondes
    game.horloge.tick(game.FPS)

# On ferme l'écran
pygame.display.quit()
pygame.quit()