import pygame
import pygame.freetype
from pygame.locals import *
import PIL 
from PIL import Image
from PIL import ImageFilter

# L'image de l'écran de chargement à afficher
imageniveau = ""

# Compteur d'animation de l'écran de chargement
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

    isAnimating = True

    def __init__(self, sprites, proprietes, defaultanimation, tags=None):
        global compteur, imageniveau

        self.sprites = {}

        if imageniveau == "":
            pygame.display.get_surface().blit(pygame.image.load(PurePath("images/fonds/chargementinitial.png")).convert(), (0, 0))
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

        
    # Fonction renderActif() -> Retourne la Surface correspondante selon son compteur d'animation et l'animation courante
    def renderActif(self):
        # Si le compteur à atteint le nombre d'images avant la prochaine image de l'animation
        if self.cptframe > self.proprietes[self.animCourante][1]:
            # Remise à zéro du compteur
            self.cptframe = 0
            
            # S'il a atteint la fin de l'animation et qu'il est en boucle
            if self.imageCourante == len(self.sprites[self.animCourante])-1  and self.proprietes[self.animCourante][0]:
                # Remettre l'image d'animation à 0
                self.imageCourante = 0
            # Sinon si l'animation n'est pas fini
            elif self.imageCourante < len(self.sprites[self.animCourante])-1:
                # Aller à la prochaine
                if self.isAnimating:
                    self.imageCourante += 1
            # Sinon (si l'animation est fini et qu'elle ne boucle pas)
            else:
                # Envoyer un évènement "fin d'animation"
                pygame.event.post(pygame.event.Event(self.END_ANIMATION, {"animation":self.animCourante}))

        # Récupérer la Surface correspondante
        render = self.sprites[self.animCourante][self.imageCourante]
        # Appliquer l'opacité
        render.set_alpha(((255*self.opacite)/100))

        return render

    
    # Fonction changeAnimation() -> Remet le compteur d'animation à 0 et change l'animation courante
    def changeAnimation(self, nomAnim):
        self.animCourante = nomAnim
        self.cptframe = 0
        self.imageCourante = 0

class Text:
    # Visible ou non
    visible = True
    # Suit l'écran (et pas la scène, problème de nommage des variables) ou pas
    suivreScene = False
    # Opacité du texte
    opacite = 100.0

    # Ombre
    shadow = True
    # Couleur de l'ombre du texte
    color_shadow = (0, 0, 0)
    # Nombre de pixels de différence de entre le texte et son ombre
    distance_shadow = 2
    # Direction de l'ombre comparé au text
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

    # Fonction renderText() -> Retourne le rendu du texte 
    def renderText(self):
        # Si un rendu n'a pas été fait, le faire
        if not self.render:
            self.render = self.font.render(self.text, self.font_color, None, size=self.font_size)
            self.render[0].set_alpha((255*self.opacite)/100)
            self.render[0].convert_alpha()
        
        # Retourne le rendu
        return self.render[0]

    # Fonction renderShadow() -> Calcule la position de l'ombre en fonction de la direction choisie, et retourne la surface de l'ombre
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

    # Fonction changeTexte -> Change le texte et recalcule le rendu du texte
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
    
    # Fonction renderButton() -> Retourne la Surface correspondant selon l'état du bouton
    def renderButton(self):
        if self.cptframe > self.proprietes[self.animCourante][self.etat][2]:
            self.cptframe = 0
            
            if self.imageCourante == len(self.images[self.animCourante][self.etat])-1  and self.proprietes[self.animCourante][self.etat][0]:
                self.imageCourante = self.proprietes[self.animCourante][self.etat][1]
            elif self.imageCourante < len(self.images[self.animCourante][self.etat])-1:
                self.imageCourante += 1

        return self.images[self.animCourante][self.etat][self.imageCourante]

    # Fonction activate(rect "la zone du bouton") -> Appelé après chaque fonction update(), change l'état du bouton en fonction de la souris (normal, pressé, survolé, etc...)
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
        # Position du premier point
        self.x1 = posx1
        self.y1 = posy1

        # Position du deuxième point
        self.x2 = posx2
        self.y2 = posy2

        # Couleur de la ligne + Epaisseur
        self.col = couleur
        self.radius = epaisseur

        # Propriétés de la lueur
        self.lueur = lueurBool
        self.lueurcol = couleurlueur
        self.lueurradius = 5
        self.lueuropacite = 100

        self.visible = True
        self.suivreScene = False
        self.opacite = 100.0

        # A la création d'une ligne, créer une surface de la bonne taille (avec marge pour ne pas couper la lueur)
        self.surfacerender = pygame.Surface((max(self.x1, self.x2) - min(self.x1, self.x2) + 100, max(self.y1, self.y2)-min(self.y1, self.y2)+ 100), flags=SRCALPHA)
        
        # Rendre la surface transparente
        self.surfacerender.fill((0,0,0,0))
        # Dessiner la ligne sur la surface
        pygame.draw.line(self.surfacerender, self.col, (self.x1+ 50, self.y1+ 50), (self.x2+ 50, self.y2+ 50), self.radius)

        # S'il y a la lueur
        if self.lueur:
            # On crée une nouvelle surface de la même taille
            surfaceglow = pygame.Surface((max(self.x1, self.x2) - min(self.x1, self.x2) +100, max(self.y1, self.y2)-min(self.y1, self.y2) + 100), flags=SRCALPHA)
            # On le remplit en blanc
            surfaceglow.fill((255,255,255,0))

            # On dessine la ligne de la lueur à la bonne couleur sur la surface
            pygame.draw.line(surfaceglow, self.lueurcol, (self.x1 + 50, self.y1+ 50), (self.x2+ 50, self.y2+ 50), self.radius)
            # On convertit la Surface en bytes
            imagerender = pygame.image.tobytes(surfaceglow , "RGBA", False)

            # Pour l'importer dans une image PIL
            imagepil = PIL.Image.frombytes("RGBA", surfaceglow.get_size(), imagerender)
            # On applique un flou
            imagepil = imagepil.filter(PIL.ImageFilter.GaussianBlur(self.lueurradius))
            # Puis on remet en bytes
            imagepil = imagepil.tobytes()

            # Pour le remettre dans pygame
            linebluredsurface = pygame.image.frombytes(imagepil, surfaceglow.get_size(),"RGBA")
            # On blit avec l'option de fusion "Ajout"
            self.surfacerender.blit(linebluredsurface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        self.surfacerender = self.surfacerender.convert_alpha()
    def renderLine(self):
        # On retourne le rendu de la ligne
        return self.surfacerender
