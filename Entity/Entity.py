import Globals, pygame, sys
import math

sys.path.append('..')

from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *
from enum import Enum
from Camera import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = 0
        self.color = "white"
        self.animations = { }
        self.animationManager: AnimationManager
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.texture_width = 0
        self.texture_height = 0
        self.OFFSET = [0, 0]
        self.IsNearPlayer = False
        self.IsHurt = False
        self.timer = 0 
        self.hp = 0
        self.attackTime = 0
        self.Time = 0
        self.HurtTime = 0
        self.IsRemoved = False
        self.isplatfrom = False
        self.enemyZone = [0, 0]
        self.atkSize = [0, 0]
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
    
    def edge_rect(self):
        size = 3
        if self.animationManager.Isflip:
            return pygame.Rect(self.rect.left - size, self.rect.bottom, size, size)
        return pygame.Rect(self.rect.right, self.rect.bottom, size, size)
    
    def wall_rect(self):
        pos_x = self.rect.left-2 if self.animationManager.Isflip else self.rect.right
        return pygame.Rect(pos_x, self.rect.top, 3, self.rect.height)

    def GetAttackBound(self):
        if self.animationManager.Isflip:
            return pygame.Rect(self.rect.left - self.atkSize[0], self.rect.top, self.atkSize[0], self.atkSize[1])
        return pygame.Rect(self.rect.right, self.rect.top, self.atkSize[0], self.atkSize[1])
    
    def ObjectDistance(self, player):
        x = math.pow(self.get_center().x - player.get_center().x, 2)
        y = math.pow(self.get_center().y - player.get_center().y, 2)
        return math.sqrt(x + y)
    
    def GravityBound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0], pos.y + self.texture_height, self.texture_width - self.OFFSET[0] * 2, 3)

    def IsFalling(self):
        rect = self.GravityBound(self.pos)
        collision_sprites = Globals.static_quadtree.query(rect)
        if collision_sprites:
            return False
        return True

    def IsObjRight(self, obj):
        return True if obj.get_center().x > self.get_center().x else False

    def SetPosition(self, pos):
        self.pos = pos

    def FrameSpeed(self, frame_end = 0):
        frame_end = self.animationManager.Animation.FrameCount if frame_end == 0 else frame_end 
        return self.animationManager.Animation.FrameSpeed * frame_end

    def HitFrame(self, frame):
        return frame-1 if not self.animationManager.Isflip else self.animationManager.Animation.FrameCount-frame

    def BeingHurt(self, damge):
        if self.hp <= 0:
            return
        self.velocity.y = -100
        self.velocity.x = 50 if self.animationManager.Isflip else -50
        self.IsHurt = True
        self.hp -= damge

    def FrameEnd(self):
        self.Time += Globals.DeltaTime
        if self.Time >= Entity.FrameSpeed(self):
            self.Time = 0
            return True
        return False
    
    def Collision(self, direction):
        self.rect = self.caculate_bound(self.pos)
        
        static_sprites = Globals.static_quadtree.query(self.rect)
        moving_sprites = Globals.moving_quadtree.query(self.rect)
        if static_sprites or moving_sprites:
            collision_sprites = static_sprites + moving_sprites
            for collider in collision_sprites:
                if direction == 'vertical':
                    # collision on the top
                    if self.rect.top <= collider.rect.bottom and self.old_rect.top >= collider.old_rect.bottom:
                        self.velocity.y = 0
                        self.rect.top = collider.rect.bottom
                        self.pos.y = collider.rect.bottom - self.OFFSET[1]

                    # collision on the bottom
                    if self.rect.bottom >= collider.rect.top and self.old_rect.bottom <= collider.old_rect.top:
                        self.velocity.y = 0
                        self.rect.bottom = collider.rect.top 
                        self.pos.y = collider.rect.top - self.texture_height
                        self.falling = False
                else:
                    # collision on the right
                    if self.rect.right >= collider.rect.left and self.old_rect.right <= collider.old_rect.left:
                        self.rect.right = collider.rect.left 
                        self.pos.x = collider.rect.left - self.texture_width + self.OFFSET[0]

                    # collision on the left
                    if self.rect.left <= collider.rect.right and self.old_rect.left >= collider.old_rect.right:
                        self.rect.left = collider.rect.right
                        self.pos.x = collider.rect.right -  self.OFFSET[0]
    
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

    def DrawOnly(self, texture, pos, rect):
        cam_rect = pygame.Rect(0, 0, Camera.width, Camera.height)
        if cam_rect.colliderect(rect):
            Globals.Surface.blit(texture, (pos[0] , pos[1]))

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

        self.DrawRect((0, 0, 255), self.GetAttackBound())
        self.DrawRect((255, 0, 0), self.caculate_bound(self.pos))
        # self.DrawRect((0, 255, 255), self.GravityBound(self.pos))
        # self.DrawRect((0, 0, 255), self.wall_rect())
        # self.DrawRect((0, 0, 255), self.edge_rect())
        # center = self.get_center() + + Globals.camera
        # # pygame.draw.circle(Globals.Surface, (0, 0, 255), center, self.enemyZone[0], 1)
        
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

