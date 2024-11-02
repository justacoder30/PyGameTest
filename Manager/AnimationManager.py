import pygame, sys

sys.path.append('..')

import Animation, Globals

class AnimationManager:
    _timer = 0
    _step = int
    def __init__(self, animation):
        self.Animation = animation
        self.IsAnimationRunning = bool
        self.Isflip = False

    def Play(self, animation):
        if self.Animation == animation:
            return
        self.Animation = animation
        self.Animation.CurrentFrame = 0
        self._timer = 0

    def Update(self):
        self._step = -1 if self.Isflip == True else 1

        self._timer += Globals.DeltaTime
        if(self._timer > self.Animation.FrameSpeed):
            self._timer = 0;
            self.Animation.CurrentFrame+=self._step

            if(self.Animation.CurrentFrame >= self.Animation.FrameCount and self.Isflip != True):
                self.Animation.CurrentFrame = 0;
            elif(self.Animation.CurrentFrame < 0 and self.Isflip == True):
                self.Animation.CurrentFrame = self.Animation.FrameCount-1;
                # IsAnimationRunning = False

    def Rect(self):
        return pygame.Rect(self.Animation.CurrentFrame * self.Animation.FrameWidth, 0 , self.Animation.FrameWidth, self.Animation.FrameWidth)