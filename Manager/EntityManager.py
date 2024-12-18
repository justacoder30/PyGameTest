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
        self.all_sprites = pygame.sprite.Group()
        BackGround(self.all_sprites)
        Map(level, self.all_sprites)
        self.player = Player(self.all_sprites)
        for pos in Map.GetListPosition("SkeletonPosition"):
            Skeleton(pos, self.all_sprites, self.player)
        # self.enemy = EnemyManager(self.player)
        # self.flag = Flag(self.player)
        self.camera = Camera(self.player)

    def Updated(self):
        for sprite in self.all_sprites:
            sprite.Update()
            if type(sprite) == Skeleton:
                sprite.pos += sprite.velocity * Globals.DeltaTime
                print(round(sprite.pos1.x), round(sprite.pos.x))
        self.camera.Update()

    def Draw(self):
        for sprite in self.all_sprites:
            sprite.Draw()
        # Globals.quadtree.draw()