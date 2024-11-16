import sys
sys.path.append('..')
import pygame, Renderder, Globals, Renderder
import Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Entity.Flag import *
from Entity.BackGround import *
from Manager.EnemyManager import *

class EntityManager:
    def __init__(self, level):
        self.map = Map(level)
        self.player = Player()
        self.enemy = EnemyManager()
        self.camera = Camera()
        self.flag = Flag()
        self.bg = BackGround()

    def Updated(self):
        self.camera.Update(self.player)
        self.bg.Update()
        self.enemy.Update(self.player)
        self.player.Update()
        self.flag.Update(self.player)

    def Draw(self):
        self.bg.Draw()
        self.map.Draw()
        self.enemy.Draw()
        self.flag.Draw()
        self.player.Draw()