import Globals, pygame, sys, Entity

sys.path.append('..')

from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *

class Entity:
    def __init__(self):
        self.speed = 0

        self.animations = { }

        self.animationManager = AnimationManager
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)

    def Draw(self):
        Globals.Screen.blit(pygame.transform.flip(self.animationManager.Animation.texture,
                                                   self.animationManager.Isflip, 0), 
                                                   self.pos, 
                                                   self.animationManager.Rect())
