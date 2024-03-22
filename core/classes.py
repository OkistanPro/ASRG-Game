import pygame
from pygame.locals import *


class Scene:
    tailleScene = largeurScene, hauteurScene = (1280, 720)

    # nomCalque : liste d'objets
    calques = {0:[]}

    camera = camera_x, camera_y = (0, 0)

    def __init__(self, objects):
        # Si le paramètre est une liste d'objets
        if isinstance(objects, list):
            self.calques[0] = objects
        # Si le paramètre est un objet simple
        if isinstance(objects, Object):
            self.calques[0].append(objects)        

class Object:
    # nomAnimation : liste de Surface pygame
    sprite = {"animation0":[]}
    cptframe = 0
    imageCourante = 0
    animCourante = "animation0"

    # Vitesse en image/secondes
    vitesseAnim = 6

    # En degrées
    direction = 0.0

    visible = True
    opacite = 100.0

    suivreScene = True

    # Ratio
    parallax = p_x, p_y = (1.0, 1.0)

    tags = []

    def __init__(self, image):
        # Si le paramètre est une liste de chemins vers des images
        if isinstance(image, list):
            # Pour chaque chemin vers image, crée une Surface et ajout dans une liste
            listImage = []
            for path in image:
                listImage.append(pygame.image.load(path))
            
            # Création de l'animation courante
            self.sprite[self.animCourante] = listImage
            
            # Création du rect selon la première image
            self.rect = self.sprite[self.animCourante][self.imageCourante].get_rect()

        # Si le paramètre est un seul chemin vers une image
        if isinstance(image, str):
            # On ajoute l'image dans l'animation courante
            self.sprite[self.animCourante].append(pygame.image.load(image))
            # Création du rect selon l'image'
            self.rect = self.sprite[self.animCourante][0].get_rect()
    
    def frame(self): # Calcul de l'animation
        # Si on a atteint la vitesse de l'animation
        if self.cptframe >= self.vitesseAnim:
            # Remise à zéro
            self.cptframe = 0
            
            # Changement de l'image courante
            if self.imageCourante == len(self.sprite[self.animCourante])-1:
                self.imageCourante = 0
            else:
                self.imageCourante += 1
    