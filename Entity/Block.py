import sys, pygame, Globals
from Entity.Entity import *

class Block(Entity):
    Obj = []
    def __init__(self, x, y, w, h):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x, y, w, h)
        self.old_rect = self.rect.copy()
        self.speed = 100
        self.velocity = pygame.math.Vector2((0,1))
        self.img = pygame.transform.scale(pygame.image.load('resource/Button/Button.png'), (w, h))
        self.img.fill("red")
        Block.Obj.append(self)

    # @classmethod
    # def GetObj(cls):
    #     return cls.Obj

    def Update(self):
        self.old_rect = self.rect.copy() # previous frame
        
        # if self.rect.bottom > 544.00:
        #     self.rect.bottom = 544.00
        #     self.pos.y = self.rect.y
        #     self.velocity.y*=-1
        # if self.rect.top < 320.00:
        #     self.rect.top = 320.00
        #     self.pos.y = self.rect.y
        #     self.velocity.y*=-1

        # self.pos.y += self.velocity.y * self.speed * Globals.DeltaTime
        self.rect.y = round(self.pos.y)
        

    def Draw(self):
        Globals.Surface.blit(self.img, (self.pos.x + Globals.camera.x, self.pos.y + Globals.camera.y))