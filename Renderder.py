import Globals, pygame
import pygame._sdl2 as sdl2

FullScreen = None
window = None
width = 0
height = 0


def FullScreenToggle():
    global FullScreen, window

    if FullScreen:
        window.set_windowed()
        FullScreen = False
    else:
        window.set_fullscreen()
        FullScreen = True

def Init():
    pass
    # screen_infor = pygame.display.Info()
    # screen_infor.current_w
    # screen_infor.current_h

def SetResolution(width, height, _fullScreen=True):
    global window, FullScreen

    FullScreen = _fullScreen

    scaleX = width / Globals.CameraSize_X
    scaleY = height / Globals.CameraSize_y

    scale = scaleX if scaleX < scaleY else scaleY

    new_width = Globals.CameraSize_X * scale
    new_height = Globals.CameraSize_y * scale

    window = sdl2.Window.from_display_module()
    window.size = (int(new_width), int(new_height))
    window.position = sdl2.WINDOWPOS_CENTERED

    if(FullScreen):
        window.set_fullscreen()
    else:
        window.set_windowed()