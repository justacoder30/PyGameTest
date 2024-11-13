import pygame, sys
sys.path.append('..')
import Game
from Control.Button import *

class GameSate:
    def __init__(self, game: Game):
        self.game = game

    def __del__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass