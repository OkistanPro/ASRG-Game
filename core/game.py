import pygame
import pygame.freetype
from pygame.locals import *

from classes import *

from pathlib import Path

pygame.init()

# Définition globale
titreJeu = "A Simple Rhythm Game"
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (960, 540)
ecran = pygame.display.set_mode(tailleEcran)

# Définition de l'horloge
horloge = pygame.time.Clock()
FPS = 60

# Définition des sprites
# D'abord, les animations --> dictionnaire (nomAnimation : liste de chemins vers images)
# Exemple : sprite0_animations = {"anim0" : ["img1.png", "img2.png", "img3.png"...]}
mario_animations = {
    "animation0" : [Path('catrunx4-0.png'), Path('catrunx4-1.png'), Path('catrunx4-2.png'), Path('catrunx4-3.png'), Path('catrunx4-4.png'), Path('catrunx4-5.png')]
}
luigi_animations = {
    "idle" : [Path("idle/NightBorne_idle-"+str(i)+".png") for i in range(9)],
    "attack" : [Path("attack/NightBorne_attack-"+str(i)+".png") for i in range(12)]
}

# Ensuite, les propriétés --> dictionnaire (nomAnimation : [enBoucle, vitesse en images/sec])
# Exemple : sprite0_proprietes = {"anim0" : [False, 5]}
mario_proprietes = {
    "animation0" : [True, 5]
}
luigi_proprietes = {
    "idle" : [True, 5],
    "attack" : [False, 5]
}

# Définition des Text
# Exemple : text01 = Text(texte, chemin vers police, taille, couleur, position)
text01 = Text("", Path("fonts/LTSaeada-Regular.otf"), 15, (255, 255, 255), (300, 100))

# Définition des Objects
# Exemple : sprite = Object(sprite0_animations, sprite0_proprietes, (posx, posy))
mario = Object(mario_animations, mario_proprietes, (400,0))
luigi = Object(luigi_animations, luigi_proprietes, (0,0))

# Définition des boutons
# D'abord, les animations 
# Exemple : bouton1_images = [["btn0.png"(, "btn1.png", "btn2.png"...)], ["btn1.png"...], ["btn2.png"...], ["btn3.png"...], ["btn4.png"...]]
# 0 Normal, 1 Enfoncé, 2 Grisé, 3 Sélectionné, 4 Survolé 
button1_images = [[Path("bouton/normal.png")], [Path("bouton/clic.png")], [Path("bouton/grisé.png")], [Path("bouton/focus.png")], [Path("bouton/survol.png")]]

# Ensuite, les propriétés 
# Exemple : bouton1_proprietes = [[False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1]]
# [enBoucle (booléen), début de la boucle (index de l'image), vitesse]
button1_proprietes = [[False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1]]

# Création des Bouton
# Exemple : bouton1 = Bouton(images, propriétés, (posx, posy))
button1 = Bouton(button1_images, button1_proprietes, (500, 200))
button2 = Bouton(button1_images, button1_proprietes, (800, 200))

# Définition des scènes
# Exemple : scene1 = Scene([sprite, bouton1...])
# Plus l'index de l'objet est grand, plus il sera devant
scene1 = Scene({0:[luigi, text01, button1]})
scene2 = Scene({0:[mario, text01, button2]})

scenes = [scene1, scene2]
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
