import pygame
from pygame.locals import *


class Scene:
    """
    Attributs :
        - tailleScene : couple d'entiers, taille de l'objet scène courant
            - largeurScene : entier positif
            - hauteurScene : entier positif
        - calques : dictionnaire de liste d'objets Object, la clef correspond au nom du calque
        Chaque calque correspond à un ensemble d'objets Object différents dans la scène
        - camera : couple d'entiers, position de l'écran par rapport à la scène
            - camera_x : entier positif
            - camera_y : entier positif

    Méthodes :
    constructeur __init__
    """

    tailleScene = largeurScene, hauteurScene = (1280, 720)

    # nomCalque : liste d'objets
    calques = {0:[]}

    camera = camera_x, camera_y = (0, 0)

    def __init__(self, objects):
        """
    Constructeur de la classe Scene
    @param objects : liste d'objet Object ou objet Object
    @return : ne retourne rien, crée une nouvelle un nouvel objet Scene
    """
        # Si le paramètre est une liste d'objets
        if isinstance(objects, list):
            self.calques[0] = objects
        # Si le paramètre est un objet simple
        if isinstance(objects, Object):
            self.calques[0].append(objects)        

class Object:
    # nomAnimation : liste de Surface pygame
    sprite = {"animation0":[]}
    # nomAnimation : [EnBoucle, vitesseAnim]
    spriteProprietes = {"animation0" : [True, 3]}

    END_ANIMATION = pygame.event.custom_type()

    cptframe = 0
    imageCourante = 0
    animCourante = "animation0"

    # En degrées
    direction = 0.0

    visible = True
    opacite = 100.0

    suivreScene = True

    # Ratio
    parallax = p_x, p_y = (1.0, 1.0)

    tags = []

    def __init__(self, animations, proprietes, pos):
        # Pour chaque animation
        for animation in animations:
            listImage = []
            # Pour chaque chemin vers image, crée une Surface et ajout dans une liste
            for path in animations[animation]:
                listImage.append(pygame.image.load(path))
        
            # Création de l'animation courante
            self.sprite[animation] = listImage
        
        # Première animation du dictionnaire = animation courante
        self.animCourante = list(animations.keys())[0]
        
        # Création du rect selon la première image
        self.rect = self.sprite[self.animCourante][self.imageCourante].get_rect()
        self.rect.topleft = pos

        # Définition des propriétés
        self.spriteProprietes = proprietes
    
    def frame(self): # Calcul de l'animation
        # Si on a atteint la vitesse de l'animation
        if self.cptframe > self.spriteProprietes[self.animCourante][1]:
            # Remise à zéro
            self.cptframe = 0
            
            # Si l'animation est en boucle et qu'on atteint la fin de l'animation
            if self.imageCourante == len(self.sprite[self.animCourante])-1  and self.spriteProprietes[self.animCourante][0]:
                # On recommence
                self.imageCourante = 0
            # Sinon si l'animation n'est pas fini
            elif self.imageCourante < len(self.sprite[self.animCourante])-1:
                # On avance l'animation
                self.imageCourante += 1
            # Sinon (si l'animation est fini et qu'il n'est pas en boucle)
            else:
                pygame.event.post(pygame.event.Event(self.END_ANIMATION, {"animation":self.animCourante}))
        
    def changeAnimation(self, nomAnim):
        self.animCourante = nomAnim
        self.cptframe = 0
        self.imageCourante = 0
    
class Text:
    def __init__(self, texte, font, fontsize, fontcolor, pos):
        self.font = pygame.freetype.Font(font)
        self.font_size = fontsize
        self.font_color = fontcolor
        self.text = texte
        self.position = pos
    
    def rendering(self):
        self.render = self.font.render(self.text, fontcolor, None, size=fontsize)
        self.render[1].topleft = self.position
        return self.render