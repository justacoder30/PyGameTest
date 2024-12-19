import pygame, sys
sys.path.append('..')
import Game
import Globals
from Control.Button import *
import State.RunningState as RunningState
import State.GameState as GameState
import State.MenuState as MenuState
import Manager.InputManager as InputManager

class ChangeLevelState(GameState.GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.continuteBtn = Button('resource/img/Button/Continue Button.png', pygame.Rect(176.00, 32.00, 120, 40))
        self.playBtn = Button('resource/img/Button/New game Button.png', pygame.Rect(176.00, 96.00, 120, 40))
        self.quitBtn = Button('resource/img/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))

        self.buttons = [
            self.continuteBtn,
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        for btn in self.buttons:
            btn.Update()

        if self.continuteBtn.isClick:
            GameState.GameSate.level+=1
            print(GameState.GameSate.level)
            self.game.ChangeState(RunningState.RunningState(self.game, GameState.GameSate.level)) 

        if self.playBtn.isClick:
            GameState.GameSate.level = 1
            self.game.ChangeState(RunningState.RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        for btn in self.buttons:
            btn.Draw()