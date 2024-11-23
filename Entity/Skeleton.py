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

    def __init__(self, pos, player):
        super().__init__()

        self.speed = 60
        self.OFFSET = [39, 18]
        self.hp = 30
        self.damage = 10
        self.player = None
        self.enemyZone = [200, 0]
        self.IsAttacking = False
        self.attackCoolDown = 0.5
        self.Gravity = 1000
        self.player = player

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
        self.map_colliders = Map.GetListBound("MapCollider")
        self.map_hodler_colliders = Map.GetListBound("HolderCollider")

    def IsNearPlayer(self):
        if self.ObjectDistance(self.player) <= self.enemyZone[0] and abs(self.get_center().y - self.player.get_center().y) <= self.GetAttackBound().height:
            return True
        else:
            return False

    def IsAttackRange(self):
        atk_rect = self.GetAttackBound()
        p_rect = self.player.caculate_bound(self.player.pos)
        if atk_rect.colliderect(p_rect):
            self.IsAttacking = True
            return True
        return False

    def FollowPlayer(self):
        self.timer = 0 
        rect = self.ColliderDetetiveBound()
        if self.IsHurt:
            pass
        elif self.hp <= 0 or Skeleton.IsAttackRange(self) and not self.IsHurt:
            self.velocity.x = 0
        else:
            self.velocity.x = self.speed if self.IsObjRight(self.player) else -self.speed

        for collider in self.Skeleton_colliders:
            if rect.colliderect(collider):
                if self.animationManager.Isflip and not self.IsObjRight(self.player) or not self.animationManager.Isflip and self.IsObjRight(self.player):
                    self.velocity.x = 0  

    def UpdateVelocity(self):
        self.timer += Globals.DeltaTime

        if not Skeleton.IsNearPlayer(self):
            self.timechange = random.randint(1, 4)
            if self.IsAttacking:
                self.velocity.x = 0
            elif self.velocity.x != 0 and self.timer >= self.timechange:
                self.velocity.x = 0
                self.timer = 0
            elif self.velocity.x == 0 and self.timer >= self.timechange:
                self.velocity.x = random.choice([-self.speed, self.speed])
                self.timer = 0
        else:
            self.FollowPlayer()

        if self.IsFalling():
            self.velocity.y += self.Gravity * Globals.DeltaTime

    def UpdatePosition(self):
        newPos = self.pos + self.velocity * Globals.DeltaTime

        newRect = self.caculate_bound(pygame.Vector2(newPos.x, self.pos.y))
        for collider in self.Skeleton_colliders:
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

        newRect = super().caculate_bound(pygame.Vector2(self.pos.x, newPos.y))
        for collider in self.map_colliders:
            if (newPos.y != self.pos.y):
                if(newRect.colliderect(collider)):
                    if self.velocity.y > 0:
                        newPos.y = collider.top - self.texture_height 
                        self.falling = False
                    elif self.velocity.y < 0:
                        newPos.y = collider.bottom - self.OFFSET[1]
                    self.velocity.y = 0
                    continue
        self.pos = newPos

    def HitFrame(self, frame):
        return frame-1 if not self.animationManager.Isflip else self.animationManager.Animation.FrameCount-frame

    def Attack(self):
        self.attackTime += Globals.DeltaTime
        self.state = State.Attack
        if self.attackTime >= self.FrameSpeed(6) and self.animationManager.Animation.CurrentFrame == self.HitFrame(6) and self.IsAttackRange():
            self.player.BeingHurt(self.damage)
            self.player.animationManager.Isflip = False if self.player.get_center().x < self.get_center().x else True
            self.attackTime = 0 

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
                self.Attack()
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
        self.UpdateVelocity()
        self.UpdatePosition()
        self.SetAnimation()
