import sys
sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Manager.AnimationManager import *
import Globals, pygame
import random

class Skeleton(Entity):
    PreviousKey = None
    CurrentKey = None

    def __init__(self, pos):
        super().__init__()

        self.speed = 60
        self.OFFSET = [39, 18]
        self.hp = 30
        self.damage = 10
        self.player = None
        self.enemyZone = [200, 0]
        self.IsAttacking = False
        self.attackCoolDown = 1

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

        self.Skeleton_colliders = Map.GetListBound("EnemyCollider")
        self.timechange = random.randint(1, 3)

    def IsNearPlayer(self):
        if super().ObjectDistance(self.player) <= self.enemyZone[0] and super().caculate_bound(self.pos).bottom == self.player.caculate_bound(self.player.pos).bottom:
            return True
        else:
            return False

    def IsAttackRange(self):
        atk_rect = super().GetAttackBound()
        p_rect = self.player.caculate_bound(self.player.pos)
        if atk_rect.colliderect(p_rect):
            self.IsAttacking = True
            return True
        return False

    def FollowPlayer(self):
        self.timer = 0 
        if Skeleton.IsAttackRange(self) or self.IsHurt or self.hp <= 0:
            self.velocity.x = 0
        else:
            self.velocity.x = -self.speed if self.player.get_center().x < super().get_center().x else self.speed

    def UpdateVelocity(self):
        self.timer += Globals.DeltaTime

        if not Skeleton.IsNearPlayer(self):
            self.timechange = random.randint(1, 3)
            if self.IsAttacking :
                self.velocity.x = 0
            elif self.velocity.x != 0 and self.timer >= self.timechange:
                self.velocity.x = 0
                self.timer = 0
            elif self.velocity.x == 0 and self.timer >= self.timechange:
                self.velocity.x = random.choice([-self.speed, self.speed])
                self.timer = 0
        else:
            self.FollowPlayer()

    def UpdatePosition(self):
        
        newPos = self.pos + self.velocity * Globals.DeltaTime
        newRect: pygame.Rect

        for collider in self.Skeleton_colliders:
            newRect = super().caculate_bound(pygame.Vector2(newPos.x, self.pos.y))
            if(newRect.colliderect(collider)):
                if self.velocity.x > 0:
                    newPos.x = collider.left - self.texture_width + self.OFFSET[0]
                elif self.velocity.x < 0:
                    newPos.x = collider.right -  self.OFFSET[0]
                if Skeleton.IsNearPlayer(self): 
                    self.velocity.x = 0
                else: 
                    self.velocity.x *= -1
                continue
        
        self.pos = newPos

    def Attack(self):
        self.attackTime += Globals.DeltaTime
        self.state = State.Attack
        if self.attackTime >= self.attackCoolDown and self.IsAttackRange():
            self.player.BeingHit(self.damage)
            self.player.animationManager.Isflip = False if self.player.get_center().x < self.get_center().x else True
        if self.attackTime >= self.attackCoolDown:
            self.attackTime = 0 



    def UpdateAnimation(self):
        if self.velocity.x > 0:
            self.animationManager.Isflip = False
        elif self.velocity.x < 0:
            self.animationManager.Isflip = True

        if self.hp <= 0:
            self.state = State.Die
            self.animationManager.SetLoop(self.animations["Death"])
            self.IsRemoved = not self.animationManager.Isloop
        elif self.IsHurt:
            self.state = State.Hurt
            self.animationManager.SetLoop(self.animations["Hurt"])
            self.IsHurt = self.animationManager.Isloop
        elif self.velocity.x != 0:
            self.state = State.Walk
        else:
            if self.IsAttacking:
                self.Attack()
                self.animationManager.SetLoop(self.animations["Attack"])
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

    def Update(self, player):
        self.player = player
        self.UpdateVelocity()
        self.UpdatePosition()
        self.SetAnimation()
