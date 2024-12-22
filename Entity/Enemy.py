import sys
sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *

class Skeleton(Entity):
    PreviousKey = None
    CurrentKey = None

    def __init__(self, pos, groups, player):
        super().__init__(groups)

        self.speed = 60
        self.OFFSET = [39, 18]
        self.hp = 30
        self.damage = 10
        self.enemyZone = [150, 50]
        self.attackCoolDown = 0.5
        self.Gravity = 1000
        self.player = player
        self.atkSize = [30, 20]
        self.score = 20

        self.animations = {
            'Walk' : Animation.Animation('resource/img/Enemy/Skeleton/Walk.png', 10),
            'Idle' : Animation.Animation('resource/img/Enemy/Skeleton/Idle.png', 8),
            'Attack' : Animation.Animation('resource/img/Enemy/Skeleton/Attack.png', 10, 0.1, True),
            'Death' : Animation.Animation('resource/img/Enemy/Skeleton/Death.png', 13, 0.08, True),
            'Hurt' : Animation.Animation('resource/img/Enemy/Skeleton/Hurt.png', 5, 0.08, True)
        }

        self.animationManager = AnimationManager(self.animations['Idle'])
        self.pos = pos
        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.state = State
        self.rect = self.caculate_bound(self.pos)
    
    def UpdateAnimation(self):
        if not self.IsHurt:
            if self.velocity.x > 0:
                self.animationManager.Isflip = False
            elif self.velocity.x < 0:
                self.animationManager.Isflip = True

        if self.hp <= 0:
            self.state = State.Die
            self.animationManager.Play(self.animations["Death"])
            self.IsRemoved = not self.animationManager.Isloop
            self.IsHurt = False
        elif self.IsHurt:
            self.state = State.Hurt
            self.animationManager.Play(self.animations["Hurt"])
            self.IsHurt = self.animationManager.Isloop
        elif self.velocity.x != 0:
            self.state = State.Walk
        else:
            if self.IsAttacking:
                self.Attack(self.player, atk_frame=6)
                self.animationManager.Play(self.animations["Attack"])
                self.IsAttacking = self.animationManager.Isloop
            else:
                self.state = State.Idle

    def SetAnimation(self):
        self.animationManager.Update()
        self.UpdateAnimation()
        
        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["Idle"])
            case State.Walk:
                self.animationManager.Play(self.animations["Walk"])
            case State.Attack:
                self.animationManager.Play(self.animations["Attack"])
            case State.Hurt:
                self.animationManager.Play(self.animations["Hurt"])
            case State.Die:
                self.animationManager.Play(self.animations["Death"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.Hurt(self.player)
        self.UpdateEnemyVelocity(self.player)
        self.UpdatePosition()
        self.SetAnimation()

class Slime(Entity):
    PreviousKey = None
    CurrentKey = None

    def __init__(self, pos, groups, player):
        super().__init__(groups)

        self.speed = 40
        self.OFFSET = [8, 10]
        self.hp = 20
        self.damage = 10
        self.enemyZone =[100, 50]
        self.attackCoolDown = 0.5
        self.Gravity = 1000
        self.player = player
        self.atkSize = [5, 15]
        self.score = 15

        self.animations = {
            'Idle' : Animation.Animation('resource/img/Enemy/Slime/Idle.png', 4, 0.15),
            'Walk' : Animation.Animation('resource/img/Enemy/Slime/Walk.png', 4),
            'Attack' : Animation.Animation('resource/img/Enemy/Slime/Attack.png', 4, 0.15, True),
            'Death' : Animation.Animation('resource/img/Enemy/Slime/Death.png', 5, 0.1, True),
            'Hurt' : Animation.Animation('resource/img/Enemy/Slime/Hurt.png', 4, 0.1, True)
        }

        self.animationManager = AnimationManager(self.animations['Idle'])
        self.pos = pos
        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.state = State
        self.rect = self.caculate_bound(self.pos)

    def edge_rect(self):
        size = 3
        if not self.animationManager.Isflip:
            return pygame.Rect(self.rect.left - size, self.rect.bottom, size, size)
        return pygame.Rect(self.rect.right, self.rect.bottom, size, size)
    
    def wall_rect(self):
        pos_x = self.rect.left-2 if not self.animationManager.Isflip else self.rect.right
        return pygame.Rect(pos_x, self.rect.top, 3, self.rect.height)

    def GetAttackBound(self):
        if not self.animationManager.Isflip:
            return pygame.Rect(self.rect.left - self.atkSize[0], self.rect.top, self.atkSize[0], self.atkSize[1])
        return pygame.Rect(self.rect.right, self.rect.top, self.atkSize[0], self.atkSize[1])
    
    def BeingHurt(self, entity):
        if self.hp <= 0:
            return
        SoundManager.PlaySound("Hurt")
        self.velocity.y = -120
        self.velocity.x = 50 if not self.animationManager.Isflip else -50
        self.IsHurt = True
        self.hp -= entity.damage

    def FrameSpeed(self, frame_end = 0):
        frame_end = self.animationManager.Animation.FrameCount if frame_end == 0 else frame_end 
        return self.animationManager.Animation.FrameSpeed * frame_end

    def HitFrame(self, frame):
        return frame-1 if self.animationManager.Isflip else self.animationManager.Animation.FrameCount-frame
    
    def UpdateAnimation(self):
        if not self.IsHurt:
            if self.velocity.x > 0:
                self.animationManager.Isflip = True
            elif self.velocity.x < 0:
                self.animationManager.Isflip = False

        if self.hp <= 0:
            self.state = State.Die
            self.animationManager.Play(self.animations["Death"])
            self.IsRemoved = not self.animationManager.Isloop
            self.IsHurt = False
        elif self.IsHurt:
            self.state = State.Hurt
            self.animationManager.Play(self.animations["Hurt"])
            self.IsHurt = self.animationManager.Isloop
        elif self.velocity.x != 0:
            self.state = State.Walk
        else:
            if self.IsAttacking:
                self.Attack(self.player, atk_frame=3)
                self.animationManager.Play(self.animations["Attack"])
                self.IsAttacking = self.animationManager.Isloop
            else:
                self.state = State.Idle

    def SetAnimation(self):
        self.animationManager.Update()
        self.UpdateAnimation()
        
        match self.state:
            case State.Idle:
                self.animationManager.Play(self.animations["Idle"])
            case State.Walk:
                self.animationManager.Play(self.animations["Walk"])
            case State.Attack:
                self.animationManager.Play(self.animations["Attack"])
            case State.Hurt:
                self.animationManager.Play(self.animations["Hurt"])
            case State.Die:
                self.animationManager.Play(self.animations["Death"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.Hurt(self.player)
        self.UpdateEnemyVelocity(self.player)
        self.UpdatePosition()
        self.SetAnimation()
