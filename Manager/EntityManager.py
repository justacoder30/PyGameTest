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
        Block.Obj = []
        self.map = Map(level)
        self.bg = BackGround()
        self.rect = Block(240.00, 592.00, 80.00, 32.00, 'vertical')
        self.rect2 = Block(320.00, 320.00, 80.00, 32.00,'horizontal')
        self.player = Player()
        self.enemy = EnemyManager(self.player)
        self.flag = Flag(self.player)
        self.camera = Camera(self.player)

        self.entities = [
            self.bg,
            self.map,
            self.rect,
            self.rect2,
            self.enemy,
            self.flag,
            self.camera,
            self.player,
        ]
        # Map(level)
        # self.player = Player()
        # Camera(self.player)

    def Updated(self):
        for entity in self.entities:
            entity.Update()
        # for b in Block.Obj:
        #     b.Update()
        # self.camera.Update()

    def Draw(self):
        for entity in self.entities:
            entity.Draw()
        # for b in Block.Obj:
        #     b.Draw()