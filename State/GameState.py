import pygame, sys
sys.path.append('..')
import Game
from Control.Button import *
from Manager.EntityManager import *

class GameSate:
    level = 1
    def __init__(self, game: Game):
        self.game = game

    def __del__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass