import pygame, sys
sys.path.append('..')
import State.GameState as GameState
from State.StopSate import *
from Manager.EntityManager import *
from Manager.InputManager import *
import Game

class RunningState(GameState.GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.enityManager = EntityManager()
        self.bg = pygame.image.load('resource/Background/Background2.png')

    def __del__(self):
        return super().__del__()

    def Update(self):
        if InputManager.CurrentKey[pygame.K_ESCAPE] and not InputManager.PreviousKey[pygame.K_ESCAPE]:
            self.game.SaveState()
            self.game.ChangeState(StopSate(self.game)) 

        self.enityManager.Updated()

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        self.enityManager.Draw()