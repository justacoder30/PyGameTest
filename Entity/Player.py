import Globals, pygame, sys

sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *

class Player(Entity):
    PreviousKey = None
    CurrentKey = None

    def __init__(self):
        super().__init__()

        self.speed = 150
        self.jump = 400
        self.OFFSET = [52, 42]

        self.animations = {
            'Run' : Animation.Animation('resource/img/Player/Run.png', 10, 0.049),
            'Idle' : Animation.Animation('resource/img/Player/Idle.png', 10),
            'Attack' : Animation.Animation('resource/img/Player/Attack.png', 6, 0.05),
            'Death' : Animation.Animation('resource/img/Player/Death.png', 10, 0.05),
            'Fall' : Animation.Animation('resource/img/Player/Fall.png', 3),
            'Jump' : Animation.Animation('resource/img/Player/Jump.png', 3)
        }

        self.animationManager = AnimationManager(self.animations['Idle'])
        self.pos = Map.GetPosition("PlayerPosition")
        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight
        
    def caculate_bound(self, pos):
        return pygame.Rect(pos.x + self.OFFSET[0], pos.y + self.OFFSET[1], self.texture_width - self.OFFSET[0] * 2, self.texture_height - self.OFFSET[1])

    def UpdateVelocity(self):
        self.velocity = pygame.Vector2(0, 0)

        Player.PreviousKey = Player.CurrentKey
        Player.CurrentKey = pygame.key.get_pressed()

        if Player.CurrentKey[pygame.K_SPACE] and Player.PreviousKey[pygame.K_SPACE] != True:
            self.velocity.y = -self.speed
        if Player.CurrentKey[pygame.K_s]:
            self.velocity.y = self.speed
        if Player.CurrentKey[pygame.K_a]:
            self.velocity.x = -self.speed
            self.animationManager.Isflip = True
        if Player.CurrentKey[pygame.K_d]:
            self.velocity.x = self.speed
            self.animationManager.Isflip = False

    def UpdatePosition(self):
        map_colliders = Map.GetListBound("MapCollider")
        newPos = self.pos + self.velocity * Globals.DeltaTime
        newRect = pygame.Rect(0, 0, 0, 0)

        for collider in map_colliders:
            # if (newPos.x != self.pos.x):
            #     newRect = self.caculate_bound(pygame.Vector2(newPos.x, self.pos.x))
            #     if(newRect.colliderect(collider)):
            #         if self.velocity.x > 0:
            #             newPos = collider["left"] - self.texture_width + self.OFFSET[0]
            #         else:
            #             newPos = collider["right"] -  self.OFFSET[0]
            #         pass
            
            # if(newPos.y != self.pos.y):
            #     newRect = self.caculate_bound(pygame.Vector2(self.pos.x, newPos.y))
            #     if(newRect.colliderect(collider)):
            #         if self.velocity.y > 0:
            #             newPos = collider["top"] - self.texture_height 
            #         else:
            #             newPos = collider["bottom"] - self.OFFSET[1]

            print(collider["left"])
        
        self.pos = newPos



    def Update(self):
        self.UpdateVelocity()
        self.UpdatePosition()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            # self.pos.y -= self.speed * Globals.DeltaTime
            pass
        if keys[pygame.K_s]:
            # self.pos.y += self.speed * Globals.DeltaTime
            pass
        if keys[pygame.K_a]:
            # self.pos.x -= self.speed * Globals.DeltaTime
            self.animationManager.Play(self.animations['Run'])
            # self.animationManager.Isflip = True
        elif keys[pygame.K_d]:
            # self.pos.x += self.speed * Globals.DeltaTime
            self.animationManager.Play(self.animations['Run'])
            # self.animationManager.Isflip = False
        else:
            self.animationManager.Play(self.animations['Idle'])

        self.animationManager.Update()
    
    def Draw(self):
        return super().Draw()