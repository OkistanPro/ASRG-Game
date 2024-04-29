import pygame
import pygame.freetype
from pygame.locals import *
import PIL 
from PIL import Image
from PIL import ImageFilter

imageniveau = ""

compteur = 0

import copy
from pathlib import PurePath
from math import floor
# Définition des Objects
# Exemple : objects = {"nomObjet" : Objet}
# Les types d'objets en questions :
"""
Les Images et Animations :
Actif   (   
            { 
                "nomAnim" : [PurePath("cheminImage1..."), PurePath("cheminImage2...")...], 
                "nomAnim2" : ...
            },
 
            {
                "nomAnim" : [enBoucle, vitesseAnim],
                "nomAnim2" : ...
            },

            "nomAnimParDéfaut"
        )

Les Texts :
Text(
    "blablabla", 
    PurePath("cheminVersPolice"), 
    taillePolice, 
    (R, V, B) --> couleur du Texte
)

Les Boutons :
Bouton( 0 : Normal, 1 : Enfoncé, 2 : Grisé, 3 : Sélectionné, 4 : Survolé
    {
        "nomBouton" :
        [
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...],
            [PurePath("cheminImage1..."), PurePath("cheminImage2...")...]
        ],
        "nomBouton2" : ...
    },
    {
        "nomBouton" :
        [
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
            [enBoucle, imageDébutBoucle, vitesseAnim],
        ],
        "nomBouton2" : ...
    },
    "nomBoutonParDéfaut"
)
"""

class Actif:
    # Taille de l'images
    taillex = 1.0
    tailley = 1.0

    def __init__(self, sprites, proprietes, defaultanimation, tags=None):
        global compteur, imageniveau

        self.sprites = {}

        if imageniveau == "":
            pygame.display.get_surface().blit(pygame.image.load(PurePath("images/fonds/nolevel.png")).convert(), (0, 0))
        else:
            pygame.display.get_surface().blit(pygame.image.load(PurePath("images/fonds/fond_chargement_" + imageniveau + ".png")).convert(), (0, 0))

        for key, anim in sprites.items():
            self.sprites[key] = []
            for value in anim:
                self.sprites[key].append(pygame.image.load(value).convert_alpha())
                if 0 <= compteur < 119:
                    compteur +=1
                else:
                    compteur = 0

                pygame.display.get_surface().blit(pygame.image.load(PurePath("images/fonds/animation/barrechargement/" + format(floor(compteur/10), '05d') + ".png")).convert(), (0, 460))
                pygame.display.update()

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

        render = self.sprites[self.animCourante][self.imageCourante]
        render.set_alpha(((255*self.opacite)/100))

        return render
    
    def changeAnimation(self, nomAnim):
        self.animCourante = nomAnim
        self.cptframe = 0
        self.imageCourante = 0

class Text:
    # Affiche ou pas
    visible = True
    # Suit la scène si elle se déplace ou pas
    suivreScene = False
    # Opacité du text
    opacite = 100.0

    # Ombre ou pas
    shadow = True
    # Couleur de l'ombre du text
    color_shadow = (0, 0, 0)
    # Nombre de pixels de différence de entrele textt et son ombre
    distance_shadow = 2
    # Direction de l'ombre commparé  au text
    direction_shadow = 0 #0 : bas droite, #1 : bas, #2 : bas gauche, #3 : gauche, #4 : haut gauche, #5 : haut, #6 : haut droite, #7 : droite
    sx = 0
    sy = 0

    render = None
    rendershdw = None


    def __init__(self, texte, font, fontsize, fontcolor):
        self.font = pygame.freetype.Font(font)
        self.font_size = fontsize
        self.font_color = fontcolor
        self.text = texte

    def renderText(self):
        if not self.render:
            self.render = self.font.render(self.text, self.font_color, None, size=self.font_size)
            self.render[0].set_alpha((255*self.opacite)/100)
            self.render[0].convert_alpha()
        
        return self.render[0]

    def renderShadow(self):
        if not self.rendershdw:
            if self.direction_shadow < 3 :
                self.sy = self.distance_shadow
            elif self.direction_shadow > 3 and self.direction_shadow < 7:
                self.sy = -self.distance_shadow
            
            if self.direction_shadow == 0 or self.direction_shadow == 6 or self.direction_shadow == 7:
                self.sx = self.distance_shadow
            elif self.direction_shadow == 2 or self.direction_shadow == 3 or self.direction_shadow == 4:
                self.sx = -self.distance_shadow
            
            self.rendershdw = self.font.render(self.text, self.color_shadow, None, size=self.font_size)
            self.rendershdw[0].set_alpha((255*self.opacite)/100)
            self.rendershdw[0].convert_alpha()

        return self.rendershdw[0]

    def changeTexte(self, texte):
        self.text = texte

        self.render = self.font.render(self.text, self.font_color, None, size=self.font_size)
        self.render[0].set_alpha((255*self.opacite)/100)
        self.render[0].convert_alpha()

        if self.direction_shadow < 3 :
            self.sy = self.distance_shadow
        elif self.direction_shadow > 3 and self.direction_shadow < 7:
            self.sy = -self.distance_shadow
        
        if self.direction_shadow == 0 or self.direction_shadow == 6 or self.direction_shadow == 7:
            self.sx = self.distance_shadow
        elif self.direction_shadow == 2 or self.direction_shadow == 3 or self.direction_shadow == 4:
            self.sx = -self.distance_shadow

        self.rendershdw = self.font.render(self.text, self.color_shadow, None, size=self.font_size)
        self.rendershdw[0].set_alpha((255*self.opacite)/100)
        self.rendershdw[0].convert_alpha()

class Bouton:
    cptframe = 0
    imageCourante = 0
    # Dans quel état est le bouton au début
    etat = 0

    # Proportion du bouton
    taillex = 1.0
    tailley = 1.0

    visible = True
    suivreScene = False
    opacite = 100.0


    def __init__(self, imagesboutons, proprietesboutons, animCourante):
        self.images = {key : [[pygame.image.load(i).convert_alpha() for i in etats] for etats in animation] for key, animation in imagesboutons.items()}
        self.proprietes = proprietesboutons
        self.animCourante = animCourante
        self.CLICKED = pygame.event.custom_type()
    
    def renderButton(self):
        if self.cptframe > self.proprietes[self.animCourante][self.etat][2]:
            self.cptframe = 0
            
            if self.imageCourante == len(self.images[self.animCourante][self.etat])-1  and self.proprietes[self.animCourante][self.etat][0]:
                self.imageCourante = self.proprietes[self.animCourante][self.etat][1]
            elif self.imageCourante < len(self.images[self.animCourante][self.etat])-1:
                self.imageCourante += 1

        return self.images[self.animCourante][self.etat][self.imageCourante]

    def activate(self, rect):
        if not pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.etat == 1:
            pygame.event.post(pygame.event.Event(self.CLICKED, {}))
        if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.etat = 1
        elif pygame.mouse.get_focused() and rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.etat = 4
        else:
            self.etat = 0

class Line:
    def __init__(self, posx1, posy1, posx2, posy2, couleur, epaisseur, lueurBool=False, couleurlueur=(0, 0, 0), radiusLueur=5):
        self.x1 = posx1
        self.y1 = posy1
        self.x2 = posx2
        self.y2 = posy2

        self.col = couleur
        self.radius = epaisseur

        self.lueur = lueurBool
        self.lueurcol = couleurlueur
        self.lueurradius = 5
        self.lueuropacite = 100

        self.visible = True
        self.suivreScene = False
        self.opacite = 100.0

        self.surfacerender = pygame.Surface((max(self.x1, self.x2) - min(self.x1, self.x2) + 100, max(self.y1, self.y2)-min(self.y1, self.y2)+ 100), flags=SRCALPHA)
        self.surfacerender.fill((0,0,0,0))
        pygame.draw.line(self.surfacerender, self.col, (self.x1+ 50, self.y1+ 50), (self.x2+ 50, self.y2+ 50), self.radius)

        if self.lueur:
            surfaceglow = pygame.Surface((max(self.x1, self.x2) - min(self.x1, self.x2) +100, max(self.y1, self.y2)-min(self.y1, self.y2) + 100), flags=SRCALPHA)
            surfaceglow.fill((255,255,255,0))
            pygame.draw.line(surfaceglow, self.lueurcol, (self.x1 + 50, self.y1+ 50), (self.x2+ 50, self.y2+ 50), self.radius)
            imagerender = pygame.image.tobytes(surfaceglow , "RGBA", False)

            imagepil = PIL.Image.frombytes("RGBA", surfaceglow.get_size(), imagerender)
            imagepil = imagepil.filter(PIL.ImageFilter.GaussianBlur(self.lueurradius))
            imagepil = imagepil.tobytes()

            linebluredsurface = pygame.image.frombytes(imagepil, surfaceglow.get_size(),"RGBA")
            self.surfacerender.blit(linebluredsurface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        self.surfacerender = self.surfacerender.convert_alpha()
    def renderLine(self):
        return self.surfacerender
