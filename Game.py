import pygame, Renderder, Globals
import Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Manager.EnemyManager import *

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
        self.enemy = EnemyManager()
        self.camera = Camera()

    def Updated(self):
        
        self.camera.Update(self.player)
        Globals.Updated()
        InputManager.Update()
        self.enemy.Update(self.player)
        self.player.Update()

    def Draw(self):
        # fill the Surface with a color to wipe away anything from last frame
        Globals.Surface.fill("blue")

        # RENDER YOUR GAME HERE
        self.map.Draw()
        self.enemy.Draw()
        self.player.Draw()
        
        # flip() the display to put your work on Surface
        Renderder.render()
        pygame.display.update()
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
        pygame.quit()