import sys
sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *
import Globals, pygame

class Player(Entity):
    PreviousKey = None
    CurrentKey = None

    def __init__(self):
        super().__init__()

        self.speed = 150
        self.jump = 400
        self.OFFSET = [52, 42]
        self.Gravity = 1000
        self.falling = False

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

        self.state = State
        
    def ApplyGravity(self):
        self.velocity.y += self.Gravity * Globals.DeltaTime

    def UpdateVelocity(self):
        self.velocity.x = 0 
        self.ApplyGravity()

        Player.PreviousKey = Player.CurrentKey
        Player.CurrentKey = pygame.key.get_pressed()

        if Player.CurrentKey[pygame.K_SPACE] and self.falling == False:
            self.velocity.y = -self.jump
            self.falling = True
        if Player.CurrentKey[pygame.K_a]:
            self.velocity.x = -self.speed
        if Player.CurrentKey[pygame.K_d]:
            self.velocity.x = self.speed

    def UpdatePosition(self):
        map_colliders = Map.GetListBound("MapCollider")
        newPos = pygame.Rect(0, 0, 0, 0)
        newPos = self.pos + self.velocity * Globals.DeltaTime
        newRect = pygame.Rect(0, 0, 0, 0)

        for collider in map_colliders:
            collider = pygame.Rect(collider["left"], collider["top"], collider["right"], collider["bottom"])

            if (newPos.x != self.pos.x):
                newRect = super().caculate_bound(pygame.Vector2(newPos.x, self.pos.y))
                if(newRect.colliderect(collider)):
                    if self.velocity.x > 0:
                        newPos.x = collider.left - self.texture_width + self.OFFSET[0]
                    elif self.velocity.x < 0:
                        newPos.x = collider.right -  self.OFFSET[0]
                    continue
            
            if (newPos.y != self.pos.y):
                newRect = super().caculate_bound(pygame.Vector2(self.pos.x, newPos.y))
                if(newRect.colliderect(collider)):
                    if self.velocity.y > 0:
                        newPos.y = collider.top - self.texture_height 
                        self.velocity.y = 0
                        self.falling = False
                    elif self.velocity.y < 0:
                        newPos.y = collider.bottom - self.OFFSET[1]
                        self.velocity.y = 0
                    continue
        
        self.pos = newPos

    def UpdateAnimation(self):
        if self.velocity.x > 0:
            self.animationManager.Isflip = False
        elif self.velocity.x < 0:
            self.animationManager.Isflip = True

        if self.velocity.y == 0 :
            if self.velocity.x != 0:
                self.state["Run"] = True
            else:
                self.state["Idle"] = True
        elif self.velocity.y > 0 :
            self.state["Jump"] = True
        else: 
            self.state["Fall"] = True

    def SetAnimation(self):
        self.UpdateAnimation()

        match self.state:
            case self.state.get("Idle"):
                self.animationManager.Play(self.animations["Idle"])
            case self.state.get("Run"):
                self.animationManager.Play(self.animations["Run"])
            case self.state.get("Fall"):
                self.animationManager.Play(self.animations["Fall"])
            case self.state.get("Jump"):
                self.animationManager.Play(self.animations["Jump"])
        
        self.animationManager.Update()



    def Update(self):
        self.UpdateVelocity()
        self.UpdatePosition()
        self.SetAnimation()

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     # self.pos.y -= self.speed * Globals.DeltaTime
        #     pass
        # if keys[pygame.K_s]:
        #     # self.pos.y += self.speed * Globals.DeltaTime
        #     pass
        # if keys[pygame.K_a]:
        #     # self.pos.x -= self.speed * Globals.DeltaTime
        #     self.animationManager.Play(self.animations['Run'])
        #     # self.animationManager.Isflip = True
        # elif keys[pygame.K_d]:
        #     # self.pos.x += self.speed * Globals.DeltaTime
        #     self.animationManager.Play(self.animations['Run'])
        #     # self.animationManager.Isflip = False
        # else:
        #     self.animationManager.Play(self.animations['Idle'])

        # self.animationManager.Update()
