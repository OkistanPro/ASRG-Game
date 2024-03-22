import pygame
from pygame.locals import *
from classes import *

pygame.init()

# Définition globale
titreJeu = "A Simple Rhythm Game"
iconeJeu = ""
tailleEcran = largeurEcran, hauteurEcran = (400, 300)
ecran = pygame.display.set_mode(tailleEcran)

# Définition de l'horloge
horloge = pygame.time.Clock()
FPS = 60

# Définition des objets
mario = Object(['catrunx4-0.png', 'catrunx4-1.png', 'catrunx4-2.png', 'catrunx4-3.png', 'catrunx4-4.png', 'catrunx4-5.png'])

# Définition des scènes
scene1 = Scene(mario)

scenes = [scene1]
scenecourante = 0

active = True

def update():
    # Pour chaque calque de la scène courante
    for calque in scenes[scenecourante].calques:
        # Pour chaque objet du calque
        for object in scenes[scenecourante].calques[calque]:
            # On augmente le compteur de temps pour chaque objet et on calcule l'animation
            object.cptframe += 1
            object.frame()

            # On imprime sur l'écran
            ecran.blit(object.sprite[object.animCourante][object.imageCourante], object.rect)
    
    # On affiche les modifications
    pygame.display.flip()

while active:
    # Evénements
    for event in pygame.event.get():
        # Clic sur la croix rouge
        if event.type == pygame.QUIT:
            # Fin de boucle, fermeture
            running = False
            pygame.display.quit()
            pygame.quit()
    
    # Fond vert
    ecran.fill("green")
    update()

    # L'horloge avance à 60 FPS
    horloge.tick(FPS)