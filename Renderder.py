import Globals, pygame

FullScreen = None
display = None
width = 0
height = 0
scale = 0 


def FullScreenToggle():
    global FullScreen, display
    
    if FullScreen:
        Globals.display = pygame.display.set_mode((width, height), vsync=1)
    else:
        Globals.display = pygame.display.set_mode((width, height), flags, vsync=1)

    FullScreen = not FullScreen

def SetResolution(_width, _height, _fullScreen=False):
    global display, FullScreen, width, height, scale, flags

    FullScreen = _fullScreen
    width, height = _width, _height

    scale_x = width / Globals.CameraSize_X
    scale_y = height / Globals.CameraSize_Y

    scale = min(scale_x, scale_y)

    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF


    if(FullScreen):
        Globals.display = pygame.display.set_mode((width, height), flags, vsync=1)
    else:
        Globals.display = pygame.display.set_mode((width, height), vsync=1) 

    # Globals.Text = pygame.Surface(Globals.display.get_size(), pygame.SRCALPHA)

def render():
    Globals.display.blit(pygame.transform.scale(Globals.Surface, Globals.display.get_size(), Globals.display), Globals.Surface.get_rect())
    if Globals.ShowText:
        Globals.display.blit(pygame.transform.scale(Globals.Text, Globals.display.get_size()), Globals.Text.get_rect())
        Globals.ShowText = False