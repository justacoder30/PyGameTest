import Globals, pygame, sys, Entity

sys.path.append('..')

from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *
from Camera import *

class Entity:
    def __init__(self):
        self.speed = 0
        self.animations = { }
        self.animationManager = AnimationManager
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.texture_width = 0
        self.texture_height = 0
        self.OFFSET = []

    def get_center(self):
        return pygame.Vector2(self.pos.x + self.animationManager.Animation.FrameWidth/2,self.pos.y + self.animationManager.Animation.FrameHeight/2)
    
    

    def SetPosition(self, pos):
        self.pos = pos

    def Draw(self):
        Globals.Surface.blit(pygame.transform.flip(self.animationManager.Animation.texture,
                                                   self.animationManager.Isflip, 0), 
                                                   (self.pos.x + Globals.camera_rect.x, self.pos.y + Globals.camera_rect.y), 
                                                   self.animationManager.Rect())
