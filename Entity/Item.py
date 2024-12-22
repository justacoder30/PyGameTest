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
        self.speed = 85

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
        # Globals.moving.insert(self)

    def UpdatePosition(self):
        self.old_rect = self.rect.copy()
        self.pos += self.velocity * self.speed * Globals.DeltaTime

        if self.direction == 'y':
            if self.rect.bottom >= self.active_zone.bottom and self.velocity.y == 1:
                self.rect.bottom = self.active_zone.bottom
                self.velocity.y = -1
            if self.rect.top <= self.active_zone.top and self.velocity.y == -1:
                self.rect.top = self.active_zone.top
                self.velocity.y = 1

        if self.direction == 'x':
            if self.rect.right >= self.active_zone.right and self.velocity.x == 1:
                self.rect.right = self.active_zone.right
                self.velocity.x = -1
            if self.rect.left <= self.active_zone.left and self.velocity.x == -1:
                self.rect.left = self.active_zone.left
                self.velocity.x = 1

        
        self.pos.y = round(self.pos.y)
        self.pos.x = round(self.pos.x)
        self.rect = self.caculate_bound(self.pos)

    def UpdateAnimation(self):
        self.animationManager.Update()
        self.animationManager.Play(self.animations["Idle"])

    def Update(self):
        self.UpdatePosition()
        self.UpdateAnimation()        
        Globals.moving_quadtree.insert(self)

class Flag(Entity):
    def __init__(self, groups, player):
        super().__init__(groups)
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
        if self.rect.colliderect(self.player.rect):
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

class HP(Entity):
    def __init__(self, groups, player):
        super().__init__(groups)

        self.img = self.GetImg('resource/img/Item/hearts.png')
        self.width = self.img.get_width()

        self.player = player
        self.hp = player.hp
    
    def GetImg(self, f_path):
        return pygame.transform.scale(pygame.image.load(f_path).convert_alpha(), (8, 8))

    def Update(self):
        self.hp = self.player.hp - 1
        self.count = int((self.hp / 10) + 1)

    def Draw(self):
        for i in range(self.count):
            Globals.Surface.blit(self.img, (i * self.width, 0))

class Heart(Entity):
    def __init__(self, pos: pygame.Vector2, groups, player):
        super().__init__(groups)
        self.pos = pos

        self.animations = {
            "Idle": Animation.Animation('resource/img/Item/Big Heart Idle (18x14).png', 8),
        }

        self.animationManager = AnimationManager(self.animations["Idle"])

        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.player = player
        self.state = State.Idle
        self.rect = self.caculate_bound(self.pos)
        self.hp = 10
        self.score = 5

    def IsTouched(self):
        if self.rect.colliderect(self.player.rect):
            return True
        return False

    def UpdateAnimation(self):

        if not self.IsTouched():
            return
        
        self.player.hp += self.hp
        self.IsRemoved = True

    def SetAnimation(self):
        self.animationManager.Update()
        self.UpdateAnimation()
        
        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["Idle"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.SetAnimation()

class Coin(Entity):
    def __init__(self, pos: pygame.Vector2, groups, player):
        super().__init__(groups)
        self.pos = pos

        self.animations = {
            "Idle": Animation.Animation('resource/img/Item/Coin.png', 5),
        }

        self.animationManager = AnimationManager(self.animations["Idle"])

        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.player = player
        self.state = State.Idle
        self.rect = self.caculate_bound(self.pos)
        self.score = 10

    def IsTouched(self):
        if self.rect.colliderect(self.player.rect):
            return True
        return False

    def UpdateAnimation(self):

        if not self.IsTouched():
            return
        
        self.IsRemoved = True

    def SetAnimation(self):
        self.animationManager.Update()
        self.UpdateAnimation()
        
        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["Idle"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.SetAnimation()

class Gem(Entity):
    def __init__(self, pos: pygame.Vector2, groups, player):
        super().__init__(groups)
        self.pos = pos

        self.animations = {
            "Idle": Animation.Animation('resource/img/Item/Gem.png', 4),
        }

        self.animationManager = AnimationManager(self.animations["Idle"])

        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.player = player
        self.state = State.Idle
        self.rect = self.caculate_bound(self.pos)
        self.score = 30

    def IsTouched(self):
        if self.rect.colliderect(self.player.rect):
            return True
        return False

    def UpdateAnimation(self):
        if not self.IsTouched():
            return
        
        self.IsRemoved = True

    def SetAnimation(self):
        self.animationManager.Update()
        self.UpdateAnimation()
        
        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["Idle"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.SetAnimation()

