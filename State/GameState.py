import pygame, sys
sys.path.append('..')
import Game
from Control.Button import *
from Manager.EntityManager import *

class GameSate:
    level = 1
    def __init__(self, game: Game):
        self.game = game
        self.bg = pygame.image.load('resource/Background/Background1.png').convert_alpha()
        self.Surface = pygame.Surface(Globals.display.get_size())
        self.Surface.blit(pygame.transform.scale(self.bg, Globals.display.get_size()), (0, 0))

    def __del__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass