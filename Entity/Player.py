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

    def __init__(self, groups):
        super().__init__(groups)

        self.speed = 150
        self.jump = 400
        self.OFFSET = [52, 42]
        self.Gravity = 1000
        self.falling = False
        self.attackTime = 0 
        self.hp = 30
        self.damage = 10
        self.atkSize = [42, 38]

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

        self.rect = self.caculate_bound(self.pos)
        self.old_rect = self.rect.copy()


    def UpdateVelocity(self):
        if self.state == State.Die:
            self.velocity.x = 0 
            self.velocity.y = 0 
            return
        
        self.velocity.x = 0

        if self.IsFalling() and not self.IsOnMovingPlatform():
            self.falling = True
            self.velocity.y += self.Gravity * Globals.DeltaTime

        Player.PreviousKey = Player.CurrentKey
        Player.CurrentKey = pygame.key.get_pressed()
        
        if Player.CurrentKey[pygame.K_SPACE] and not self.falling:
            self.velocity.y = -self.jump
        if Player.CurrentKey[pygame.K_a]:
            self.velocity.x = -self.speed
        if Player.CurrentKey[pygame.K_d]:
            self.velocity.x = self.speed

    def OnTrap(self):
        collision_sprites = Globals.static_quadtree.query(self.rect)
        if not collision_sprites:
            return
        traps = [trap for trap in collision_sprites if trap.isTrap]
        if traps:
            self.BeingHurt(None, 5)

    def UpdatePosition(self):
        self.old_rect = self.rect.copy()
        
        self.pos.x += self.velocity.x * Globals.DeltaTime
        self.Collision('x')
        self.pos.y += self.velocity.y * Globals.DeltaTime
        self.Collision('y')  
        self.OnTrap()

    def BeingHurt(self, entity: None, damage: None):
        if self.HurtTime != 0:
            return
        if entity != None:
            self.animationManager.Isflip = False if self.get_center().x < entity.get_center().x else True
        SoundManager.PlaySound("Hurt")
        self.IsHurt = True
        self.hp -= damage

    def Attack(self, enity, atk_frame):
        if not self.IsAttackRange(enity.rect):
            return

        self.attackTime += Globals.DeltaTime
        self.state = State.Attack
        if self.attackTime >= self.FrameSpeed(atk_frame) and self.animationManager.Animation.CurrentFrame == self.HitFrame(atk_frame):
            enity.BeingHurt(self)
            self.attackTime = 0

    def SetState(self):
        if self.velocity.x > 0:
            self.animationManager.Isflip = False
        elif self.velocity.x < 0:
            self.animationManager.Isflip = True

        if self.IsHurt:
            self.HurtTime += Globals.DeltaTime
            if self.HurtTime >= 0.3:
                self.HurtTime = 0
                self.IsHurt = False
            
        if self.velocity.y == 0 :
            if self.velocity.x != 0:
                self.state = State.Run
            else:
                if Player.CurrentKey[pygame.K_j] and not Player.PreviousKey[pygame.K_j] or self.animationManager.Isloop:
                    self.state = State.Attack
                else:
                    self.state = State.Idle
        elif self.velocity.y > 0 :
            self.state = State.Fall
        else: 
            self.state = State.Jump

        if self.hp <= 0:
            self.state = State.Die
            if super().FrameEnd():
                Globals.GameOver = True

    def UpdateAnimation(self):
        self.animationManager.Update()
        self.SetState()

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
                
    def UpdateSound(self):
        if(self.PreviousState != State.Attack and self.state == State.Attack): SoundManager.PlaySound("attack")
        if(self.PreviousState == State.Fall and self.state != State.Fall): SoundManager.PlaySound("landing")

    def Update(self):
        self.PreviousState = self.state
        self.UpdateVelocity()
        self.UpdatePosition()
        self.UpdateAnimation()
        self.UpdateSound()
        self.CheckOutOfMap()
        self.HurtColor("red")