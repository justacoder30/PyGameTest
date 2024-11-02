import pygame, Renderder, Globals, Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
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
        self.map = Map()
        self.player = Player()
        self.camera = Camera()
        # print(self.map.GetPosition("PlayerPosition"))

    def LoadContent():
        pass

    def Updated(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        
        self.camera.Update(self.player)
        Globals.Updated()
        InputManager.Update()
        self.player.Update()

        

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.running = False


    def Draw(self):
        # fill the Surface with a color to wipe away anything from last frame
        Globals.Surface.fill("blue")

        # RENDER YOUR GAME HERE
        self.map.Draw()
        self.player.Draw()
        
        # flip() the display to put your work on Surface
        Renderder.render()
        pygame.display.update()
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
            # pygame.display.update()
        pygame.quit()