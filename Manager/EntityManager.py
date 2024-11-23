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
from Entity.Block import *
from Entity.BackGround import *
from Manager.EnemyManager import *

class EntityManager:
    def __init__(self, level):
        self.map = Map(level)
        self.bg = BackGround()
        self.rect = Block(240.00, 592.00, 80.00, 32.00, 'vertical')
        self.rect2 = Block(320.00, 320.00, 80.00, 32.00,'horizontal')
        self.player = Player()
        self.enemy = EnemyManager(self.player)
        self.flag = Flag(self.player)
        self.camera = Camera(self.player)

        self.enities = [
            
        ]

    def Updated(self):
        self.rect.Update()
        self.rect2.Update()
        self.camera.Update()
        self.bg.Update()
        self.enemy.Update()
        self.player.Update()
        self.flag.Update()

    def Draw(self):
        self.bg.Draw()
        self.map.Draw()
        self.enemy.Draw()
        self.flag.Draw()
        self.rect.Draw()
        self.rect2.Draw()
        self.player.Draw()