import pygame, sys
sys.path.append('..')
import Game
import Globals
from Control.Button import *
import State.RunningState as RunningState
import State.GameState as GameState
import State.MenuState as MenuState
import Manager.InputManager as InputManager

class StopSate(GameState.GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.bg = pygame.image.load('resource/Background/Background1.png').convert_alpha()
        self.resumeBtn = Button('resource/Button/Resume Button.png', pygame.Rect(176.00, 32.00, 120, 40))
        self.playBtn = Button('resource/Button/Play Button.png', pygame.Rect(176.00, 96.00, 120, 40))
        self.quitBtn = Button('resource/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))

        self.buttons = [
            self.resumeBtn,
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        for btn in self.buttons:
            btn.Update()

        if self.resumeBtn.isClick or InputManager.CurrentKey[pygame.K_ESCAPE] and not InputManager.PreviousKey[pygame.K_ESCAPE]:
            self.game.ChangeState(self.game.PreviousState) 

        if self.playBtn.isClick:
            GameState.GameSate.level = 1
            self.game.ChangeState(RunningState.RunningState(self.game, GameState.GameSate.level))

        if self.quitBtn.isClick:
            Globals.running = False

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        for btn in self.buttons:
            btn.Draw()