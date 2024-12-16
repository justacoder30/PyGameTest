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
        self.rect = None
        self.old_rect = None

    def get_center(self):
        return pygame.Vector2(self.pos.x + self.animationManager.Animation.FrameWidth/2,self.pos.y + self.animationManager.Animation.FrameHeight/2)
    
    def caculate_bound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0],
                           pos.y + self.OFFSET[1],
                           self.texture_width - self.OFFSET[0] * 2,
                           self.texture_height - self.OFFSET[1])

    def GetAttackBound(self):
        if self.animationManager.Isflip:
            return pygame.Rect(self.pos.x, self.pos.y + self.OFFSET[1], self.OFFSET[0], self.texture_height - self.OFFSET[1])
        return pygame.Rect(self.pos.x + self.texture_width - self.OFFSET[0], self.pos.y + self.OFFSET[1], self.OFFSET[0], self.texture_height - self.OFFSET[1])
    
    def ObjectDistance(self, player):
        x = math.pow(self.get_center().x - player.get_center().x, 2)
        y = math.pow(self.get_center().y - player.get_center().y, 2)
        return math.sqrt(x + y)
    
    def GravityBound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0], pos.y + self.texture_height, self.texture_width - self.OFFSET[0] * 2, 5)
    
    def ColliderDetetiveBound(self):
        rect = self.caculate_bound(self.pos)
        pos_x = rect.left-1 if self.animationManager.Isflip else rect.right
        return pygame.Rect(pos_x, rect.top, 1, rect.height)

    def IsFalling(self):
        newRect = self.GravityBound(self.pos)

        # for collider in self.map_colliders:
        #     if newRect.colliderect(collider):
        #         return False
            
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
    
    def CheckOutOfMap(self):
        # print(self.pos.x, Globals.MapSize.width - self.OFFSET[0])
        self.pos.x  = pygame.math.clamp(self.pos.x, -self.OFFSET[0], Globals.MapSize.width - self.texture_width + self.OFFSET[0])
        if self.pos.y > Globals.MapSize.height:
            Globals.GameOver = True

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage

    def DrawSprite(self, texture, pos):
        if Camera.rect.colliderect(self.rect):
            Globals.Surface.blit(texture, (pos.x + Globals.camera.x, pos.y + Globals.camera.y))

    def Draw(self):
        color = "white"

        if self.IsHurt:
            color = "red"

        if Camera.rect.colliderect(self.rect):
            Globals.Surface.blit(pygame.transform.flip(self.changColor(self.animationManager.Animation.texture, color),
                                                    self.animationManager.Isflip, 0), 
                                                    (self.pos.x + Globals.camera.x, self.pos.y + Globals.camera.y), 
                                                    self.animationManager.Rect())
            
        cnt = 0
        rect = pygame.Rect(self.pos.x, self.pos.y, self.texture_width , self.texture_height * 1.2)
        for collider in self.map_colliders:
            cnt+=1
            if rect.colliderect(collider.rect):
                pygame.draw.rect(Globals.Surface, (255, 0, 0), (collider.rect.x + Globals.camera.x, collider.rect.y + Globals.camera.y, collider.rect.width, collider.rect.height), 1)
        # print(cnt)
        pygame.draw.rect(Globals.Surface, (0, 255, 0), (self.pos.x + Globals.camera.x, self.pos.y + Globals.camera.y, self.texture_width , self.texture_height * 1.2), 1)
        atkRect = self.GetAttackBound()
        pygame.draw.rect(Globals.Surface, (0, 0, 255), (atkRect.x + Globals.camera.x, atkRect.y + Globals.camera.y, atkRect.w , atkRect.h), 1)
        self_rect = self.caculate_bound(self.pos)
        pygame.draw.rect(Globals.Surface, (0, 255, 0), (self_rect.x + Globals.camera.x, self_rect.y + Globals.camera.y, self_rect.w , self_rect.h), 1)
        g_rect = self.GravityBound(self.pos)
        pygame.draw.rect(Globals.Surface, (0, 0, 255), (g_rect.x + Globals.camera.x, g_rect.y + Globals.camera.y, g_rect.w , g_rect.h), 1)
        
class State(Enum):
    Idle = "Idle"
    Run = "Run"
    Walk = "Walk"
    Hurt = "Hurt"
    Fall = "Fall"
    Jump = "Jump"
    Attack = "Attack"
    Die = "Die"

