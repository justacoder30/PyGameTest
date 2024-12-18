import sys
sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *
import Globals, pygame

class Movingplatform(Entity):
    def __init__(self, rect: pygame.Rect, groups):
        super().__init__(groups)
        self.active_zone = rect
        self.direction = 'y' if self.active_zone.w < self.active_zone.h else 'x'
        self.speed = 65

        self.animations = {
            'Idle' : Animation.Animation('resource/img/MovingPlatform/Idle.png', 4)
        }

        self.animationManager = AnimationManager(self.animations['Idle'])

        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.state = State.Idle

        self.pos = pygame.Vector2(rect.x, rect.y)
        self.rect = self.caculate_bound(self.pos)
        self.velocity = pygame.Vector2(0, 1) if self.direction == 'y' else pygame.Vector2(1, 0)

    def UpdatePosition(self):
        # print(self.direction)
        self.old_rect = self.rect.copy()
        # self.pos += self.velocity * self.speed * Globals.DeltaTime

        if self.direction == 'y':
            if self.rect.bottom >= self.active_zone.bottom and self.velocity.y == 1:
                # self.rect.bottom = self.active_zone.bottom
                # self.pos.y = self.rect.y
                self.velocity.y = -1
            if self.rect.top <= self.active_zone.top and self.velocity.y == -1:
                # self.rect.top = self.active_zone.top
                # self.pos.y = self.rect.y
                self.velocity.y = 1
            # self.pos.y += self.velocity.y * self.speed * Globals.DeltaTime

        if self.direction == 'x':
            if self.rect.right >= self.active_zone.right and self.velocity.x == 1:
                # self.rect.right = self.active_zone.right
                # self.pos.x = self.rect.x
                self.velocity.x = -1
            if self.rect.left <= self.active_zone.left and self.velocity.x == -1:
                # self.rect.left = self.active_zone.left
                # self.pos.x = self.rect.x
                self.velocity.x = 1
            # self.pos.x += self.velocity.x * self.speed * Globals.DeltaTime

        
        # self.pos.y = round(self.pos.y, 1)
        # self.pos.x = round(self.pos.x, 1)
        self.rect = self.caculate_bound(self.pos)
        # self.pos = pygame.Vector2(self.rect.topleft)

    def UpdateAnimation(self):
        self.animationManager.Update()
        self.animationManager.Play(self.animations["Idle"])

    def Update(self):
        self.UpdatePosition()
        self.UpdateAnimation()        
        # Globals.static_quadtree.insert(self)
        Globals.moving_quadtree.insert(self)
        
    def Draw(self):
        return super().Draw()

class Flag(Entity):
    def __init__(self, player):
        super().__init__()
        self.pos = Map.GetPosition("FlagPosition")
        self.OFFSET = [0, 0]

        self.animations = {
            "No Flag": Animation.Animation('resource/img/Item/No Flag.png', 1),
            "Flag Out": Animation.Animation('resource/img/Item/Flag Out.png', 26, 0.07, True)
        }

        self.animationManager = AnimationManager(self.animations['No Flag'])

        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.player = None
        self.state = State.Idle
        
        self.player = player
        self.rect = self.caculate_bound(self.pos)

    def IsTouched(self):
        p_Rect = self.player.caculate_bound(self.player.pos)

        if self.rect.colliderect(p_Rect):
            return True

        return False

    def UpdateAnimation(self):

        if self.state == State.Run and not self.animationManager.Isloop:
            Globals.IsLevelEnd = True

        if not self.IsTouched() and self.state == State.Idle:
            self.state = State.Idle
        else:
            self.state = State.Run

    def SetAnimation(self):
        self.animationManager.Update()
        self.UpdateAnimation()
        
        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["No Flag"])
            case State.Run:
                self.animationManager.Play(self.animations["Flag Out"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.SetAnimation()