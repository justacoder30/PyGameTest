import sys
sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Entity.Block import *
from Manager.EnemyManager import *
from Manager.AnimationManager import *
from Entity.Block import *
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
        self.attackTime = 0 
        self.hp = 50
        self.damage = 10

        self.img = pygame.transform.scale(pygame.image.load('resource/Button/Button.png'), (80.00, 32.00))

        self.animations = {
            'Run' : Animation.Animation('resource/img/Player/Run.png', 10, 0.04),
            'Idle' : Animation.Animation('resource/img/Player/Idle.png', 10, 0.05),
            'Attack' : Animation.Animation('resource/img/Player/Attack.png', 6, 0.04, True),
            'Death' : Animation.Animation('resource/img/Player/Death.png', 10, 0.05, True),
            'Fall' : Animation.Animation('resource/img/Player/Fall.png', 3),
            'Jump' : Animation.Animation('resource/img/Player/Jump.png', 3),
            'Hurt' : Animation.Animation('resource/img/Player/Hurt.png', 10, 0.08, True),
        }

        self.animationManager = AnimationManager(self.animations['Idle'])
        self.pos = Map.GetPosition("PlayerPosition")
        self.texture_width = self.animationManager.Animation.FrameWidth
        self.texture_height = self.animationManager.Animation.FrameHeight

        self.state = State

        self.map_colliders = Map.GetTilesBound()
        # self.map_hodler_colliders = Map.GetListBound("HolderCollider")

        self.rect = self.caculate_bound(self.pos)
        self.old_rect = self.rect.copy()
        # Block.Obj.append(self)

    def IsFalling(self):
        newRect = self.GravityBound(self.pos)

        for collider in self.map_colliders:
            if newRect.colliderect(collider):
                return False
            
        # for collider in self.map_hodler_colliders:
        #     if newRect.colliderect(collider):
        #         return False
            
        # for collider in Block.Obj:
        #     if newRect.colliderect(collider.rect):
        #         if collider.direction == 'vertical':
        #             self.pos.y += collider.velocity.y * collider.speed * Globals.DeltaTime
        #             self.pos.y = round(self.pos.y)
        #         else:
        #             self.pos.x += collider.velocity.x * collider.speed * Globals.DeltaTime
        #             self.pos.x = round(self.pos.x)
        #         return False
            
        return True

    def UpdateVelocity(self):
        if self.state == State.Die:
            self.velocity.x = 0 
            return
        
        self.velocity.x = 0

        if self.IsFalling():
            self.falling = True
            self.velocity.y += self.Gravity * Globals.DeltaTime

        Player.PreviousKey = Player.CurrentKey
        Player.CurrentKey = pygame.key.get_pressed()
        if Player.CurrentKey[pygame.K_SPACE] and not self.falling:
            self.velocity.y = -self.jump
        # if Player.CurrentKey[pygame.K_w]:
        #     self.velocity.y = -self.speed
        # if Player.CurrentKey[pygame.K_s]:
        #     self.velocity.y = self.speed
        if Player.CurrentKey[pygame.K_a]:
            self.velocity.x = -self.speed
        if Player.CurrentKey[pygame.K_d]:
            self.velocity.x = self.speed

    def UpdatePosition(self):
        # Tính vị trí tiếp theo của nhân vật
        self.pos += self.velocity * Globals.DeltaTime 
        self.old_rect = self.rect.copy()
        self.rect = self.caculate_bound(self.pos)

        for collider in self.map_colliders:
            if self.rect.colliderect(collider.rect):

                # collision on the top
                if self.rect.top <= collider.rect.bottom and self.old_rect.top >= collider.old_rect.bottom:
                    self.velocity.y = 0
                    self.rect.top = collider.rect.bottom
                    self.pos.y = collider.rect.bottom - self.OFFSET[1]

                # collision on the bottom
                if self.rect.bottom >= collider.rect.top and self.old_rect.bottom <= collider.old_rect.top:
                    self.velocity.y = 0
                    self.rect.bottom = collider.rect.top 
                    self.pos.y = collider.rect.top - self.texture_height
                    self.falling = False

                # collision on the right
                if self.rect.right >= collider.rect.left and self.old_rect.right <= collider.old_rect.left:
                    self.rect.right = collider.rect.left 
                    self.pos.x = collider.rect.left - self.texture_width + self.OFFSET[0]

                # collision on the left
                if self.rect.left <= collider.rect.right and self.old_rect.left >= collider.old_rect.right:
                    self.rect.left = collider.rect.right
                    self.pos.x = collider.rect.right -  self.OFFSET[0]

    def Attack(self):
        self.state = State.Attack
        if not EnemyManager.GetEnemyList():
            return

        if super().FrameEnd():
            atk_rect = super().GetAttackBound()
            for enemy in EnemyManager.GetEnemyList():
                if atk_rect.colliderect(enemy.caculate_bound(enemy.pos)):
                    enemy.BeingHurt(self.damage)

    def BeingHurt(self, damge):
        self.IsHurt = True
        self.hp -= damge

    def UpdateAnimation(self):
        if self.velocity.x > 0:
            self.animationManager.Isflip = False
        elif self.velocity.x < 0:
            self.animationManager.Isflip = True

        if self.IsHurt:
            self.HurtTime += Globals.DeltaTime
            if self.HurtTime >= 0.2:
                self.HurtTime = 0
                self.IsHurt = False
            
        if self.velocity.y == 0 :
            if self.velocity.x != 0:
                self.state = State.Run
            else:
                if self.hp <= 0:
                    self.state = State.Die
                    if super().FrameEnd():
                        Globals.GameOver = True
                elif Player.CurrentKey[pygame.K_j] and not Player.PreviousKey[pygame.K_j] or self.animationManager.Isloop:
                    Player.Attack(self)
                else:
                    self.state = State.Idle
        elif self.velocity.y > 0 :
            self.state = State.Fall
        else: 
            self.state = State.Jump

    def SetAnimation(self):
        self.animationManager.Update()
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
            case State.Die:
                self.animationManager.Play(self.animations["Death"])
            case State.Hurt:
                self.animationManager.Play(self.animations["Hurt"])
            case _:
                print("f{self.state} is not valid!")

    def Update(self):
        self.UpdateVelocity()
        self.UpdatePosition()
        self.SetAnimation()
        self.CheckOutOfMap()

    def Draw(self):
        super().Draw()
        