import pygame, sys
sys.path.append('..')
import Game
import Globals
from Control.Button import *
import State.RunningState as RunningState
import State.GameState as GameState
import Manager.InputManager as InputManager

class StopSate(GameState.GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.bg = pygame.image.load('resource/Background/Background1.png')
        self.continuteBtn = Button('resource/Button/Continue Button.png', pygame.Rect(176.00, 32.00, 120, 40))
        self.playBtn = Button('resource/Button/Play Button.png', pygame.Rect(176.00, 96.00, 120, 40))
        self.quitBtn = Button('resource/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))

        self.buttons = [
            self.continuteBtn,
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        for btn in self.buttons:
            btn.Update()

        if self.continuteBtn.isClick or InputManager.CurrentKey[pygame.K_ESCAPE] and not InputManager.PreviousKey[pygame.K_ESCAPE]:
            self.game.ChangeState(self.game.PreviousState) 

        if self.playBtn.isClick:
            self.game.ChangeState(RunningState.RunningState(self.game))

        if self.quitBtn.isClick:
            Globals.running = False

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        for btn in self.buttons:
            btn.Draw()