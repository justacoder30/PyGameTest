import pygame, sys

sys.path.append('..')
from Entity.Map import *
from Animation import *
from Entity.Entity import *
from Manager.EnemyManager import *
from Manager.AnimationManager import *
import Globals

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