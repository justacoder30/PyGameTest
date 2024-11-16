import pygame, sys
sys.path.append('..')
import State.GameState as GameState
from State.StopSate import *
from State.ChangeLevelState import *
from Manager.EntityManager import *
from Manager.InputManager import *
import Game

class RunningState(GameState.GameSate):
    def __init__(self, game: Game, level):
        super().__init__(game)
        self.enityManager = EntityManager(level)

    def __del__(self):
        return super().__del__()

    def Update(self):
        if InputManager.CurrentKey[pygame.K_ESCAPE] and not InputManager.PreviousKey[pygame.K_ESCAPE]:
            self.game.SaveState()
            self.game.ChangeState(StopSate(self.game)) 

        if Globals.IsLevelEnd:
            Globals.IsLevelEnd = False
            self.game.ChangeState(ChangeLevelState(self.game))
        else:
            self.enityManager.Updated()

    def Draw(self):
        self.enityManager.Draw()