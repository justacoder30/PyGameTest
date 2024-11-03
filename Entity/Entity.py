import Globals, pygame, sys

sys.path.append('..')

from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *
from enum import Enum
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
    
    def caculate_bound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0],
                           pos.y + self.OFFSET[1],
                           self.texture_width - self.OFFSET[0] * 2,
                           self.texture_height - self.OFFSET[1])
    def GravityBound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0], pos.y + self.texture_height, self.texture_width - self.OFFSET[0] * 2, 1)

    def SetPosition(self, pos):
        self.pos = pos

    def DrawSprite(self, texture, pos):
        Globals.Surface.blit(texture, (pos.x + Globals.camera_rect.x, pos.y + Globals.camera_rect.y))

    def Draw(self):
        Globals.Surface.blit(pygame.transform.flip(self.animationManager.Animation.texture,
                                                   self.animationManager.Isflip, 0), 
                                                   (self.pos.x + Globals.camera_rect.x, self.pos.y + Globals.camera_rect.y), 
                                                    self.animationManager.Rect())
        
class State(Enum):
    Idle = "Idle"
    Run = "Run"
    Fall = "Fall"
    Jump = "Jump"
    Attack = "Attack"
    Die = "Die"

