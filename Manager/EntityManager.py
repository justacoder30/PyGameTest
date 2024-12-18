import sys
sys.path.append('..')
import pygame, Renderder, Globals, Renderder
import Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Entity.Item import *
from Entity.Block import *
from Entity.BackGround import *
from Entity.Enemy import *

class EntityManager:
    def __init__(self, level):
        self.all_sprites = pygame.sprite.Group()
        Globals.static_quadtree = Globals.Quadtree(Globals.MapSize, 10)

        BackGround(self.all_sprites)
        Map(level, self.all_sprites)

        for rect in Map.GetRectList("MovingPlatform"):
            Movingplatform(rect, self.all_sprites)
        # Block(416.00, 256.00, 48.00, 32.00, 'vertical', self.all_sprites)

        self.player = Player(self.all_sprites)

        for pos in Map.GetListPosition("SkeletonPosition"):
            Skeleton(pos, self.all_sprites, self.player)

        # self.flag = Flag(self.player)
        self.camera = Camera(self.player)

        

    def Updated(self):
        Globals.moving_quadtree = Globals.Quadtree(Globals.MapSize, 1)
        # Globals.static_quadtree = Globals.Quadtree(Globals.MapSize, 10)

        for sprite in self.all_sprites:
            sprite.Update()
            if sprite.IsRemoved:
                sprite.kill()
        self.camera.Update()

    def Draw(self):
        for sprite in self.all_sprites:
            sprite.Draw()
        # Globals.moving_quadtree.draw()