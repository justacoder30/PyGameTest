import Entity.Entity
import sys, pygame, Globals
sys.path.append('..')
from Entity.Entity import *

class Block(Entity):
    def __init__(self, x, y, w, h, direction, groups):
        super().__init__(groups)
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x, y, w, h)
        self.old_rect = self.rect.copy()
        self.speed = 90
        self.velocity = pygame.math.Vector2((1, 1))
        self.img = pygame.transform.scale(pygame.image.load('resource/img/Button/Button.png'), (w, h))
        self.img.fill("red")
        self.direction = direction

    # @classmethod
    # def GetObj(cls):
    #     return cls.Obj

    def Update(self):
        self.old_rect = self.rect.copy() # previous frame
        
        if self.direction == 'vertical':
            if self.rect.bottom > 544.00:
                self.rect.bottom = 544.00
                self.pos.y = self.rect.y
                self.velocity.y*=-1
            if self.rect.top < 320.00:
                self.rect.top = 320.00
                self.pos.y = self.rect.y
                self.velocity.y*=-1

            self.pos.y += self.velocity.y * self.speed * Globals.DeltaTime

        if self.direction == 'horizontal':
            
            if self.rect.right < 320.00:
                self.rect.right = 320.00
                self.pos.x = self.rect.x
                self.velocity.x*=-1
            if self.rect.left > 480.00:
                self.rect.left = 480.00
                self.pos.x = self.rect.x
                self.velocity.x*=-1
            self.pos.x += self.velocity.x * self.speed * Globals.DeltaTime

        
        self.pos.y = round(self.pos.y)
        self.rect.y = round(self.pos.y)
        self.pos.x = round(self.pos.x)
        self.rect.x = round(self.pos.x)
        Globals.quadtree.insert(self)
        

    def Draw(self):
        Globals.Surface.blit(self.img, (self.pos.x + Globals.camera.x, self.pos.y + Globals.camera.y))