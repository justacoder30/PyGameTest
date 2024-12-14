import pygame, Renderder, Globals
import Manager.InputManager as InputManager
from Manager.EntityManager import *
from Control.Button import *
from State.MenuState import *

class Game:
    def __init__(self):
        self.CurrentState = None
        self.PreviousState = None
        self.NextState = None


        # pygame setup
        pygame.init()
        Camera.SetSize(480, 270)
        Globals.Init()
        Renderder.SetResolution(1920, 1080)
        
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
        print(round(Globals.Clock.get_fps()))

    def Draw(self):
        # fill the Surface with a color to wipe away anything from last frame
        Globals.Surface.fill((0, 0, 0, 0))
        
        self.CurrentState.Draw()
        
        # flip() the display to put your work on Surface
        Renderder.render()
        pygame.display.update()
        pygame.display.flip()
        

    def Run(self):
        while Globals.running:
            self.Updated()
            self.Draw()
        pygame.quit()