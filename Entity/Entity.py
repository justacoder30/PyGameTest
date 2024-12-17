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
        self.color = "white"
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
        self.direction = ""

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
        rect = self.GravityBound(self.pos)
        collision_sprites = Globals.quadtree.query(rect)
        if collision_sprites:
            for collider in collision_sprites:
                if collider.direction == 'vertical':
                    self.pos.y += collider.velocity.y * collider.speed * Globals.DeltaTime
                    self.pos.y = round(self.pos.y)
                else:
                    self.pos.x += collider.velocity.x * collider.speed * Globals.DeltaTime
                    self.pos.x = round(self.pos.x)
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
        self.pos.x  = pygame.math.clamp(self.pos.x, -self.OFFSET[0], Globals.MapSize.width - self.texture_width + self.OFFSET[0])
        if self.pos.y > Globals.MapSize.height:
            Globals.GameOver = True

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage
    
    def DrawRect(self, color, rect: pygame.Rect):
        pygame.draw.rect(Globals.Surface, color, (rect.x + Globals.camera.x, rect.y + Globals.camera.y, rect.width , rect.height), 1)

    def DrawSprite(self, texture, pos):
        if Camera.rect.colliderect(self.rect):
            Globals.Surface.blit(texture, (pos.x + Globals.camera.x, pos.y + Globals.camera.y))

    def Draw(self):

        if Camera.rect.colliderect(self.rect):
            Globals.Surface.blit(pygame.transform.flip(self.changColor(self.animationManager.Animation.texture, self.color),
                                                    self.animationManager.Isflip, 0), 
                                                    (self.pos.x + Globals.camera.x, self.pos.y + Globals.camera.y), 
                                                    self.animationManager.Rect())
            
        # rect = pygame.Rect(self.pos.x, self.pos.y, self.texture_width , self.texture_height * 1.2)
        # for collider in self.map_colliders:
        #     if rect.colliderect(collider.rect):
        #         pygame.draw.rect(Globals.Surface, (255, 0, 0), (collider.rect.x + Globals.camera.x, collider.rect.y + Globals.camera.y, collider.rect.width, collider.rect.height), 1)

        # self.DrawRect((0, 0, 255), self.GetAttackBound())
        # self.DrawRect((0, 255, 0), self.caculate_bound(self.pos))
        # self.DrawRect((0, 0, 255), self.GravityBound(self.pos))
        
        # rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4)
        # collision_sprites = Globals.quadtree.query(rect)
        # if collision_sprites:
        #     for collider in collision_sprites:
        #         self.DrawRect((255, 0, 0), collider.rect)
        
class State(Enum):
    Idle = "Idle"
    Run = "Run"
    Walk = "Walk"
    Hurt = "Hurt"
    Fall = "Fall"
    Jump = "Jump"
    Attack = "Attack"
    Die = "Die"

