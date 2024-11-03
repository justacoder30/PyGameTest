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
            'Attack' : Animation.Animation('resource/img/Player/Attack.png', 6, 0.05, True),
            'Death' : Animation.Animation('resource/img/Player/Death.png', 10, 0.05),
            'Fall' : Animation.Animation('resource/img/Player/Fall.png', 3),
            'Jump' : Animation.Animation('resource/img/Player/Jump.png', 3)
        }

        self.animationManager = AnimationManager(self.animations['Idle'])
        self.pos = Map.GetPosition("PlayerPosition")
        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.state = State

        self.map_colliders = Map.GetListBound("MapCollider")
        self.map_hodler_colliders = Map.GetListBound("HolderCollider")
        
    def ApplyGravity(self):
        newRect = super().GravityBound(self.pos)

        for collider in self.map_colliders:
            collider = pygame.Rect(collider["left"], collider["top"], collider["right"], collider["bottom"])
            if newRect.colliderect(collider):
                return
            
        for collider in self.map_hodler_colliders:
            collider = pygame.Rect(collider["left"], collider["top"], collider["right"], collider["bottom"])
            if newRect.colliderect(collider):
                return

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
        
        newPos = self.pos + self.velocity * Globals.DeltaTime
        newRect = pygame.Rect(0, 0, 0, 0)

        for collider in self.map_hodler_colliders:
            collider = pygame.Rect(collider["left"], collider["top"], collider["right"], collider["bottom"])
            if self.velocity.y > 0:
                newRect = super().caculate_bound(pygame.Vector2(self.pos.x, newPos.y))
                if(newRect.colliderect(collider)):
                    newPos.y = collider.top - self.texture_height 
                    self.velocity.y = 0
                    self.falling = False
                    continue

        for collider in self.map_colliders:
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
                self.state = State.Run
            else:
                if Player.CurrentKey[pygame.K_j] and Player.PreviousKey[pygame.K_j] == False and self.animationManager.Isloop == False:
                    self.state = State.Attack
                    self.animationManager.Isloop = True
                if self.state == State.Attack and self.animationManager.Isloop:
                    self.state = State.Attack
                else:
                    self.state = State.Idle
        elif self.velocity.y > 0 :
            self.state = State.Fall
        else: 
            self.state = State.Jump

    def SetAnimation(self):
        self.UpdateAnimation()

        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["Idle"])
            case State.Run:
                self.animationManager.Play(self.animations["Run"])
            case State.Fall:
                self.animationManager.Play(self.animations["Fall"])
            case State.Jump:
                self.animationManager.Play(self.animations["Jump"])
            case State.Attack:
                self.animationManager.Play(self.animations["Attack"])
            case _:
                print("f{self.state} is not valid!")
        
        self.animationManager.Update()

    def Update(self):
        self.UpdateVelocity()
        self.UpdatePosition()
        self.SetAnimation()
