import sys
sys.path.append('..')
import pygame, Globals, Renderder
import Entity.Map as Map
import Manager.SoundManager as SoundManager
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Entity.Item import *
from Entity.BackGround import *
from Entity.Enemy import *

class EntityManager:
    def __init__(self, level):
        Globals.score = 0
        self.all_sprites = pygame.sprite.Group()
        Globals.static_quadtree = Globals.Quadtree(Globals.MapSize, 10)

        BackGround(self.all_sprites)
        Map(level, self.all_sprites)

        for rect in Map.GetRectList("MovingPlatform"):
            Movingplatform(rect, self.all_sprites)

        player = Player(self.all_sprites)

        for pos in Map.GetListPosition("SkeletonPosition"):
            Skeleton(pos, self.all_sprites, player, level)
        
        for pos in Map.GetListPosition("SlimePosition"):
            Slime(pos, self.all_sprites, player, level)

        for pos in Map.GetListPosition("HeartPosition"):
            Heart(pos, self.all_sprites, player)
        
        for pos in Map.GetListPosition("CoinPosition"):
            Coin(pos, self.all_sprites, player)

        for pos in Map.GetListPosition("GemPosition"):
            Gem(pos, self.all_sprites, player)

        Flag(self.all_sprites, player)
        self.camera = Camera(player)
        HP(self.all_sprites, player)

        

    def Updated(self):
        Globals.moving_quadtree = Globals.Quadtree(Globals.MapSize, 1)
        # Globals.static_quadtree = Globals.Quadtree(Globals.MapSize, 10)

        for sprite in self.all_sprites:
            sprite.Update()
            if sprite.IsRemoved:
                Globals.score+=sprite.score
                SoundManager.PlaySound("coin")
                sprite.kill()
            
        self.camera.Update()

    def Draw(self):
        for sprite in self.all_sprites:
            sprite.Draw()
        # Globals.moving_quadtree.draw()
        # Globals.static_quadtree.draw()
        