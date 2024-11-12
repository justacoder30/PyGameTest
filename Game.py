import pygame, Renderder, Globals
import Manager.InputManager as InputManager
from Manager.EntityManager import *
from Control.Button import *

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        Globals.CameraSize(480, 270)
        Globals.Init()
        Renderder.SetResolution(1920, 1080)

        self.running = True
        self.entityManager = EntityManager()
        self.bg = pygame.image.load('resource/Background/Background1.png')
        self.btn = Button('resource/Button/Play Button.png', (176.00, 96, 120, 40))
        self.playgame = False
        self.color: None

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage

    def Updated(self):
        Globals.Updated()
        InputManager.Update()
        self.entityManager.Updated()
        self.btn.Update()

    def Draw(self):
        # fill the Surface with a color to wipe away anything from last frame
        Globals.Surface.fill("blue")

        # RENDER YOUR GAME HERE
        self.entityManager.Draw()
        if not self.playgame:
            Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
            self.btn.Draw()
        
        # flip() the display to put your work on Surface
        Renderder.render()
        pygame.display.update()
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
        pygame.quit()