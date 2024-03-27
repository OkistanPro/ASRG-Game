import pygame
import pygame.freetype
from pygame.locals import *

from classes import *

from pathlib import Path

pygame.init()

# Définition globale
titreJeu = "Pos-Module"
pygame.display.set_caption(titreJeu)
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (960, 540)
ecran = pygame.display.set_mode(tailleEcran)

# Définition de l'horloge
horloge = pygame.time.Clock()
FPS = 60

# Définition des sprites
# D'abord, les animations --> dictionnaire (nomAnimation : liste de chemins vers images)
# Exemple : sprite0_animations = {"anim0" : ["img1.png", "img2.png", "img3.png"...]}

# Ensuite, les propriétés --> dictionnaire (nomAnimation : [enBoucle, vitesse en images/sec])
# Exemple : sprite0_proprietes = {"anim0" : [False, 5]}

# Définition des Text
# Exemple : text01 = Text(texte, chemin vers police, taille, couleur, position)

# Définition des Objects
# Exemple : sprite = Object(sprite0_animations, sprite0_proprietes, (posx, posy))

# Définition des boutons
# D'abord, les animations 
# Exemple : bouton1_images = [["btn0.png"(, "btn1.png", "btn2.png"...)], ["btn1.png"...], ["btn2.png"...], ["btn3.png"...], ["btn4.png"...]]
# 0 Normal, 1 Enfoncé, 2 Grisé, 3 Sélectionné, 4 Survolé
buttonAjouter_images = [["buttonAjouter.png"], ["buttonAjouter.png"], ["buttonAjouter.png"], ["buttonAjouter.png"], ["buttonAjouter.png"]]
buttonSupprimer_images = [["buttonSupprimer.png"], ["buttonSupprimer.png"], ["buttonSupprimer.png"], ["buttonSupprimer.png"], ["buttonSupprimer.png"]]

# Ensuite, les propriétés 
# Exemple : bouton1_proprietes = [[False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1]]
# [enBoucle (booléen), début de la boucle (index de l'image), vitesse]
buttonAjouter_proprietes = [[False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1]]
buttonSupprimer_proprietes = [[False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1]]


# Création des Bouton
# Exemple : bouton1 = Bouton(images, propriétés, (posx, posy))
buttonAjouter = Bouton(buttonAjouter_images, buttonAjouter_proprietes, (750, 450))
buttonSupprimer = Bouton(buttonSupprimer_images, buttonSupprimer_proprietes, (750, 500))

# Définition des scènes
# Exemple : scene1 = Scene([sprite, bouton1...])
# Plus l'index de l'objet est grand, plus il sera devant
scene1 = Scene({0:[buttonAjouter, buttonSupprimer]})

scenes = [scene1]
scenecourante = 0

active = True

def update(): # Appelé à chaque boucle de jeu
    # Pour chaque calque de la scène courante
    for calque in scenes[scenecourante].calques:
        # Pour chaque objet du calque
        for object in scenes[scenecourante].calques[calque]:
            # Si c'est un objet
            if isinstance(object, Object):
                # On augmente le compteur de temps pour chaque objet et on calcule l'animation
                object.cptframe += 1
                object.renderObject()

                # On imprime sur l'écran
                ecran.blit(object.sprite[object.animCourante][object.imageCourante], object.rect.move(-scenes[scenecourante].camera[0], -scenes[scenecourante].camera[1]))
            
            # Si c'est un texte
            if isinstance(object, Text):
                # On crée un couple (Surface, Rect)
                couplerender = object.renderText()
                # On imprime sur l'écran
                ecran.blit(couplerender[0], couplerender[1].move(-scenes[scenecourante].camera[0], -scenes[scenecourante].camera[1]))

            # Si c'est un bouton
            if isinstance(object, Bouton):
                # On augmente le compteur de temps pour chaque objet et on calcule l'animation
                object.cptframe += 1
                object.renderButton()
                # On imprime sur l'écran
                ecran.blit(object.images[object.etat][object.imageCourante], object.rect.move(-scenes[scenecourante].camera[0], -scenes[scenecourante].camera[1]))
    
    # On affiche les modifications
    pygame.display.flip()
