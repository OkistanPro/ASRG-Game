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

# Définition des boutons
# D'abord, les animations 
# --> liste (ordonnée : 0 Normal, 1 Enfoncé, 2 Grisé, 3 Sélectionné, 4 Survolé) de liste de chemins vers images
# Ensuite, les propriétés 
# --> liste (ordonnée : 0 Normal, 1 Enfoncé, 2 Grisé, 3 Sélectionné, 4 Survolé) de [enBoucle (booléen), début de la boucle (index de l'image qui va boucler), vitesse]
button1_images = [["bouton\\normal.png"], ["bouton\\clic.png"], ["bouton\\grisé.png"], ["bouton\\focus.png"], ["bouton\\survol.png"]]
button1_proprietes = [[False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1], [False, 0, 1]]
button1 = Bouton(button1_images, button1_proprietes, (100, 100))

# Définition des scènes
scene1 = Scene([luigi, mario, testtext, button1])

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
                object.renderObject()

                # On imprime sur l'écran
                ecran.blit(object.sprite[object.animCourante][object.imageCourante], object.rect.move(-scenes[scenecourante].camera_x, -scenes[scenecourante].camera_y))
            
            # Si c'est un texte
            if isinstance(object, Text):
                # On crée un couple (Surface, Rect)
                couplerender = object.renderText()
                # On imprime sur l'écran
                ecran.blit(couplerender[0], couplerender[1].move(-scenes[scenecourante].camera_x, -scenes[scenecourante].camera_y))

            # Si c'est un bouton
            if isinstance(object, Bouton):
                # On augmente le compteur de temps pour chaque objet et on calcule l'animation
                object.cptframe += 1
                object.renderButton()
                # On imprime sur l'écran
                ecran.blit(object.images[object.etat][object.imageCourante], object.rect.move(-scenes[scenecourante].camera_x, -scenes[scenecourante].camera_y))
    
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
        button1.evenement(event)

    
    testtext.text = str(luigi.animCourante)

    # Fond vert
    ecran.fill("green")
    update()

    # L'horloge avance à 60 FPS
    horloge.tick(FPS)