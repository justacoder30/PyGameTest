import sys
sys.path.append('..')
import pygame, Renderder, Globals, Renderder
import Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Manager.EnemyManager import *

class EntityManager:
    def __init__(self):
        self.map = Map()
        self.player = Player()
        self.enemy = EnemyManager()
        self.camera = Camera()

    def Updated(self):
        self.enemy.Update(self.player)
        self.player.Update()
        self.camera.Update(self.player)

    def Draw(self):
        # fill the Surface with a color to wipe away anything from last frame

        # RENDER YOUR GAME HERE
        self.map.Draw()
        self.enemy.Draw()
        self.player.Draw()