import pygame, sys
sys.path.append('..')
import Globals, Game
from Control.Button import *
from State.RunningState import *
import State.GameState as GameState

class MenuSate(GameState.GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.bg = pygame.image.load('resource/Background/Background1.png')
        self.playBtn = Button('resource/Button/Play Button.png', pygame.Rect(176.00, 96, 120, 40))
        self.quitBtn = Button('resource/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))

        self.buttons = [
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        for btn in self.buttons:
            btn.Update()

        if self.playBtn.isClick:
            self.game.ChangeState(RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        for btn in self.buttons:
            btn.Draw()