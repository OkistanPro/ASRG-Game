import pygame
import pygame.freetype
from pygame.locals import *
from classes import *
from os import listdir
from os.path import isfile, join


pygame.init()

# Définition globale
titreJeu = "A Simple Rhythm Game"
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (400, 300)
ecran = pygame.display.set_mode(tailleEcran)

# Définition de l'horloge
horloge = pygame.time.Clock()
FPS = 60

# Définition des sprites
# D'abord, les animations --> dictionnaire (nomAnimation : liste de chemins vers images)
# Ensuite, les propriétés --> dictionnaire (nomAnimation : [enBoucle : vitesse en images/sec])
mario_animations = {
    "animation0" : ['catrunx4-0.png', 'catrunx4-1.png', 'catrunx4-2.png', 'catrunx4-3.png', 'catrunx4-4.png', 'catrunx4-5.png']
}
mario_proprietes = {
    "animation0" : [True, 5]
}
luigi_animations = {
    "idle" : ["idle\\NightBorne_idle-"+str(i)+".png" for i in range(9)],
    "attack" : ["attack\\NightBorne_attack-"+str(i)+".png" for i in range(12)]
}
luigi_proprietes = {
    "idle" : [True, 5],
    "attack" : [False, 5]
}

# Définition des textes
# Text(texte, chemin vers police, taille, couleur, position)
testtext = Text("", "fonts\LTSaeada-Regular.otf", 15, (0, 0, 0), (300, 100))


# Définition des objets
mario = Object(mario_animations, mario_proprietes, (200,0))
luigi = Object(luigi_animations, luigi_proprietes, (0,0))

# Définition des scènes
scene1 = Scene([luigi, mario, testtext])

scenes = [scene1]
scenecourante = 0

active = True

def update():
    # Pour chaque calque de la scène courante
    for calque in scenes[scenecourante].calques:
        # Pour chaque objet du calque
        for object in scenes[scenecourante].calques[calque]:
            # Si c'est un objet
            if isinstance(object, Object):
                # On augmente le compteur de temps pour chaque objet et on calcule l'animation
                object.cptframe += 1
                object.frame()

                # On imprime sur l'écran
                ecran.blit(object.sprite[object.animCourante][object.imageCourante], object.rect)
            # Si c'est un texte
            if isinstance(object, Text):
                # On crée un couple (Surface, Rect)
                render = object.rendering(15, (0, 0, 0))
                # On imprime sur l'écran
                ecran.blit(render[0], render[1])
    
    # On affiche les modifications
    pygame.display.flip()

while active:
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == QUIT:
            # Fin de boucle, fermeture
            active = False
            pygame.display.quit()
            pygame.quit()
        if event.type == KEYDOWN and event.key == K_h:
            luigi.changeAnimation("attack")
        if event.type == luigi.END_ANIMATION and event.animation == "attack":
            luigi.changeAnimation("idle")

    
    testtext.text = str(luigi.animCourante)

    # Fond vert
    ecran.fill("green")
    update()

    # L'horloge avance à 60 FPS
    horloge.tick(FPS)