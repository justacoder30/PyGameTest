import pygame, Renderder, Globals
import Manager.InputManager as InputManager
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        Globals.CameraSize(480, 270)
        Globals.Init()
        Renderder.SetResolution(1920, 1080)

        self.running = True

        self.player = Player()

    def LoadContent():
        pass

    def Updated(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        Globals.Updated()
        InputManager.Update()
        self.player.Update()
        

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.running = False


    def Draw(self):
        # fill the screen with a color to wipe away anything from last frame
        Globals.Screen.fill("blue")

        # RENDER YOUR GAME HERE
        self.player.Draw()

        # flip() the display to put your work on screen
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
            # pygame.display.update()
        pygame.quit()