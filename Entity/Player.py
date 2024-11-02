import Entity.Entity
import Globals, pygame, sys, Entity

sys.path.append('..')

from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 150

        self.animations = {
            'Run' : Animation.Animation('resource/img/Player/Run.png', 10, 0.049),
            'Idle' : Animation.Animation('resource/img/Player/Idle.png', 10),
            'Attack' : Animation.Animation('resource/img/Player/Attack.png', 6, 0.05),
            'Death' : Animation.Animation('resource/img/Player/Death.png', 10, 0.05),
            'Fall' : Animation.Animation('resource/img/Player/Fall.png', 3),
            'Jump' : Animation.Animation('resource/img/Player/Jump.png', 3)
        }

        self.animationManager = AnimationManager(self.animations['Idle'])
        self.pos = pygame.Vector2(Globals.Screen.get_width() / 2, Globals.Screen.get_height() / 2)
        

    def UpdateVelocity(self):
        self.velocity = 0 

        keys = pygame.key.get_pressed()

        PreviousKey = CurrentKey
        CurrentKey = pygame.key.get_pressed()

        if CurrentKey[pygame.K_w]:
            self.pos.y -= self.speed * Globals.DeltaTime
        elif CurrentKey[pygame.K_s]:
            self.pos.y += self.speed * Globals.DeltaTime
        elif CurrentKey[pygame.K_a]:
            self.pos.x -= self.speed * Globals.DeltaTime
            self.animationManager.Isflip = True
        elif CurrentKey[pygame.K_d]:
            self.pos.x += self.speed * Globals.DeltaTime
            self.animationManager.Isflip = False
        elif CurrentKey[pygame.K_ESCAPE]:
            self.running = False

    def Update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= self.speed * Globals.DeltaTime
        elif keys[pygame.K_s]:
            self.pos.y += self.speed * Globals.DeltaTime
        elif keys[pygame.K_a]:
            self.pos.x -= self.speed * Globals.DeltaTime
            self.animationManager.Play(self.animations['Run'])
            self.animationManager.Isflip = True
        elif keys[pygame.K_d]:
            self.pos.x += self.speed * Globals.DeltaTime
            self.animationManager.Play(self.animations['Run'])
            self.animationManager.Isflip = False
        elif keys[pygame.K_ESCAPE]:
            self.running = False
        else:
            self.animationManager.Play(self.animations['Idle'])

        self.animationManager.Update()