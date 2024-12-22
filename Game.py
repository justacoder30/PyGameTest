import pygame, Renderder, Globals
import Manager.InputManager as InputManager
import Manager.SoundManager as SoundManager
from Manager.EntityManager import *
from Control.Button import *
from State.GameState import *

class Game:
    def __init__(self):
        self.CurrentState = None
        self.PreviousState = None
        self.NextState = None

        # pygame setup
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()
        SoundManager.Init()
        Camera.SetSize(480, 270)
        # Camera.SetSize(560, 315)
        Globals.Init()
        Renderder.SetResolution(1920, 1080)
        # Renderder.SetResolution(1280, 720, True)
        # Renderder.SetResolution(960, 540)
        
        self.CurrentState = MenuSate(self)

    def ChangeState(self, state):
        self.NextState = state

    def SaveState(self):
        self.PreviousState = self.CurrentState

    def Updated(self):
        Globals.Updated()
        InputManager.Update()

        if self.NextState != None:
            self.CurrentState = self.NextState
            self.NextState = None

        self.CurrentState.Update()
        # print(round(Globals.Clock.get_fps()))

    def Draw(self):
        Globals.Surface.fill((0, 0, 0, 0))
        
        self.CurrentState.Draw()
        
        Renderder.render()
        pygame.display.update()
        

    def Run(self):
        while Globals.running:
            self.Updated()
            self.Draw()
        pygame.quit()