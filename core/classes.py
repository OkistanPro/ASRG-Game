import pygame
from pygame.locals import *

class Actif:
    def __init__(self, sprites, proprietes, defaultanimation, tags=None):
        self.sprites = {key : [(pygame.image.load(value), pygame.image.load(value).get_rect()) for value in anim] for key, anim in sprites.items()}
        self.proprietes = proprietes

        self.cptframe = 0
        self.imageCourante = 0
        self.animCourante = defaultanimation

        self.direction = 0.0

        self.visible = True
        self.opacite = 100.0

        self.parallax = [1.0, 1.0]

        self.tags = tags or []

        self.END_ANIMATION = pygame.event.custom_type()
        
    def renderActif(self):
        if self.cptframe > self.spriteProprietes[self.animCourante][1]:
            self.cptframe = 0
            
            if self.imageCourante == len(self.sprite[self.animCourante])-1  and self.spriteProprietes[self.animCourante][0]:
                self.imageCourante = 0
            elif self.imageCourante < len(self.sprite[self.animCourante])-1:
                self.imageCourante += 1
            else:
                pygame.event.post(pygame.event.Event(self.END_ANIMATION, {"animation":self.animCourante}))

        return self.sprites[animCourante][imageCourante]
    
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
    
    def renderText(self):
        self.render = self.font.render(self.text, self.font_color, None, size=self.font_size)
        self.render[1].topleft = self.position
        return self.render*

class Bouton:
    cptframe = 0
    imageCourante = 0
    etat = 0

    def __init__(self, imagesboutons, proprietesboutons):
        self.images = [[(pygame.image.load(i), pygame.image.load(i).get_rect()) for i in etats] for etats in imagesboutons]
        self.proprietes = proprietesboutons
    
    def renderButton(self):
        if self.cptframe > self.proprietes[self.etat][2]:
            self.cptframe = 0
            
            if self.imageCourante == len(self.images[self.etat])-1  and self.proprietes[self.etat][0]:
                self.imageCourante = self.proprietes[self.etat][1]
            elif self.imageCourante < len(self.images[self.etat])-1:
                self.imageCourante += 1

        return self.images[self.etat][imageCourante]

    def activate(self, event, cam):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos[0]+cam[0], event.pos[1]+cam[1]):
            self.etat = 1
        elif pygame.mouse.get_focused() and self.rect.collidepoint(pygame.mouse.get_pos()[0]+cam[0], pygame.mouse.get_pos()[1]+cam[1]):
            self.etat = 4
        else:
            self.etat = 0

class Scene:

    camera = [0, 0]

    def __init__(self, taille, calq):
        self.tailleScene = taille
        self.calques = calq