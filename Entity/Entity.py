import Globals, pygame, sys
import math

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
        self.animationManager: AnimationManager
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.texture_width = 0
        self.texture_height = 0
        self.OFFSET = []
        self.IsNearPlayer = False
        self.IsHurt = False
        self.timer = 0 
        self.hp = 0
        self.attackTime = 0
        self.Time = 0
        self.HurtTime = 0
        self.IsRemoved = False
        self.map_colliders = None
        self.map_hodler_colliders = None

    def get_center(self):
        return pygame.Vector2(self.pos.x + self.animationManager.Animation.FrameWidth/2,self.pos.y + self.animationManager.Animation.FrameHeight/2)
    
    def caculate_bound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0],
                           pos.y + self.OFFSET[1],
                           self.texture_width - self.OFFSET[0] * 2,
                           self.texture_height - self.OFFSET[1])

    def GetAttackBound(self):
        if self.animationManager.Isflip:
            return pygame.Rect(self.pos.x, self.pos.y + self.OFFSET[1], self.OFFSET[0], self.OFFSET[1])
        return pygame.Rect(self.pos.x + self.texture_width - self.OFFSET[0], self.pos.y + self.OFFSET[1], self.OFFSET[0], self.OFFSET[1])
    
    def ObjectDistance(self, player):
        x = math.pow(self.get_center().x - player.get_center().x, 2)
        y = math.pow(self.get_center().y - player.get_center().y, 2)
        return math.sqrt(x + y)
    
    def GravityBound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0], pos.y + self.texture_height, self.texture_width - self.OFFSET[0] * 2, 1)
    
    def ColliderDetetiveBound(self):
        rect = self.caculate_bound(self.pos)
        pos_x = rect.left-1 if self.animationManager.Isflip else rect.right
        return pygame.Rect(pos_x, rect.top, 1, rect.height)

    def IsFalling(self):
        newRect = self.GravityBound(self.pos)

        for collider in self.map_colliders:
            if newRect.colliderect(collider):
                return False
            
        for collider in self.map_hodler_colliders:
            if newRect.colliderect(collider):
                return False
        return True

    def IsObjRight(self, obj):
        return True if obj.get_center().x > self.get_center().x else False

    def SetPosition(self, pos):
        self.pos = pos

    def FrameSpeed(self, frame_end = 0):
        frame_end = self.animationManager.Animation.FrameCount if frame_end == 0 else frame_end 
        return self.animationManager.Animation.FrameSpeed * frame_end

    def BeingHurt(self, damge):
        if self.hp <= 0:
            return
        self.velocity.y = -150
        self.velocity.x = 50 if self.animationManager.Isflip else -50
        self.IsHurt = True
        self.hp -= damge

    def FrameEnd(self):
        self.Time += Globals.DeltaTime
        if self.Time >= Entity.FrameSpeed(self):
            self.Time = 0
            return True
        return False

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage

    def DrawSprite(self, texture, pos):
        Globals.Surface.blit(texture, (pos.x + Globals.camera_rect.x, pos.y + Globals.camera_rect.y))

    def Draw(self):
        color = "white"

        if self.IsHurt:
            color = "red"

        Globals.Surface.blit(pygame.transform.flip(self.changColor(self.animationManager.Animation.texture, color),
                                                   self.animationManager.Isflip, 0), 
                                                   (self.pos.x + Globals.camera_rect.x, self.pos.y + Globals.camera_rect.y), 
                                                    self.animationManager.Rect())
        
class State(Enum):
    Idle = "Idle"
    Run = "Run"
    Walk = "Walk"
    Hurt = "Hurt"
    Fall = "Fall"
    Jump = "Jump"
    Attack = "Attack"
    Die = "Die"

