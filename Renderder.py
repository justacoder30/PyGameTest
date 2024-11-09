import Globals
import pygame

FullScreen = None
display = None
width = 0
height = 0


def FullScreenToggle():
    global FullScreen, display
    
    if FullScreen:
        display = pygame.display.set_mode((width, height), vsync=1)
        FullScreen = False
    else:
        display = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=1)
        FullScreen = True

def SetResolution(_width, _height, _fullScreen=False):
    global display, FullScreen, width, height

    FullScreen = _fullScreen
    width, height = _width, _height

    if(FullScreen):
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
    else:
        display = pygame.display.set_mode((width, height), vsync=1) 

def render():
    display.blit(pygame.transform.scale(Globals.Surface, display.get_size()), Globals.Surface.get_rect())