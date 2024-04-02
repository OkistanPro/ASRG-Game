import pygame
from pygame.locals import *

class Actif:
    posx = 0
    posy = 0
    taillex = 1.0
    tailley = 1.0

    def __init__(self, sprites, proprietes, defaultanimation, tags=None):
        self.sprites = {key : [pygame.image.load(value) for value in anim] for key, anim in sprites.items()}
        self.proprietes = proprietes

        self.cptframe = 0
        self.imageCourante = 0
        self.animCourante = defaultanimation

        self.direction = 0.0

        self.visible = True
        self.suivreScene = False
        self.opacite = 100.0

        self.parallax = [1.0, 1.0]

        self.tags = tags or []

        self.END_ANIMATION = pygame.event.custom_type()
        
    def renderActif(self):
        if self.cptframe > self.proprietes[self.animCourante][1]:
            self.cptframe = 0
            
            if self.imageCourante == len(self.sprites[self.animCourante])-1  and self.proprietes[self.animCourante][0]:
                self.imageCourante = 0
            elif self.imageCourante < len(self.sprites[self.animCourante])-1:
                self.imageCourante += 1
            else:
                pygame.event.post(pygame.event.Event(self.END_ANIMATION, {"animation":self.animCourante}))

        return self.sprites[self.animCourante][self.imageCourante]
    
    def changeAnimation(self, nomAnim):
        self.animCourante = nomAnim
        self.cptframe = 0
        self.imageCourante = 0

class Text:
    posx = 0
    posy = 0

    visible = True
    suivreScene = False
    opacite = 100.0

    shadow = False
    color_shadow = (0, 0, 0)
    distance_shadow = 2
    direction_shadow = 0 #0 : bas droite, #1 : bas, #2 : bas gauche, #3 : gauche, #4 : haut gauche, #5 : haut, #6 : haut droite, #7 : droite
    sx = 0
    sy = 0


    def __init__(self, texte, font, fontsize, fontcolor):
        self.font = pygame.freetype.Font(font)
        self.font_size = fontsize
        self.font_color = fontcolor
        self.text = texte
    
    def renderText(self):
        self.render = self.font.render(self.text, self.font_color, None, size=self.font_size)
        return self.render[0]

    def renderShadow(self):
        if self.direction_shadow < 3 :
            self.sy = self.distance_shadow
        elif self.direction_shadow > 3 and self.direction_shadow < 7:
            self.sy = -self.distance_shadow
        
        if self.direction_shadow == 0 or self.direction_shadow == 6 or self.direction_shadow == 7:
            self.sx = self.distance_shadow
        elif self.direction_shadow == 2 or self.direction_shadow == 3 or self.direction_shadow == 4:
            self.sx = -self.distance_shadow
        
        self.render = self.font.render(self.text, self.color_shadow, None, size=self.font_size)
        return self.render[0]

class Bouton:
    cptframe = 0
    imageCourante = 0
    etat = 0

    posx = 0
    posy = 0
    taillex = 1.0
    tailley = 1.0

    visible = True
    suivreScene = False
    opacite = 100.0


    CLICKED = pygame.event.custom_type()

    def __init__(self, imagesboutons, proprietesboutons):
        self.images = [[pygame.image.load(i) for i in etats] for etats in imagesboutons]
        self.proprietes = proprietesboutons
    
    def renderButton(self):
        if self.cptframe > self.proprietes[self.etat][2]:
            self.cptframe = 0
            
            if self.imageCourante == len(self.images[self.etat])-1  and self.proprietes[self.etat][0]:
                self.imageCourante = self.proprietes[self.etat][1]
            elif self.imageCourante < len(self.images[self.etat])-1:
                self.imageCourante += 1

        return self.images[self.etat][self.imageCourante]

    def activate(self, rect):
        if not pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.etat == 1:
            pygame.event.post(pygame.event.Event(self.CLICKED, {}))
        if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.etat = 1
        elif pygame.mouse.get_focused() and rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.etat = 4
        else:
            self.etat = 0

class Scene:

    camera = [0, 0]

    def __init__(self, calq, couleurfond):
        self.calques = calq
        self.fond = couleurfond