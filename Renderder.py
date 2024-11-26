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
        FullScreen = False
    else:
        Globals.display = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=1)
        FullScreen = True

def SetResolution(_width, _height, _fullScreen=False):
    global display, FullScreen, width, height, scale, bg1, pos1, pos2

    FullScreen = _fullScreen
    width, height = _width, _height

    scale_x = width / Globals.CameraSize_X
    scale_y = width / Globals.CameraSize_Y

    scale = min(int(scale_x), int(scale_y))

    if(FullScreen):
        Globals.display = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=1)
    else:
        Globals.display = pygame.display.set_mode((width, height), vsync=1) 

    bg1 = pygame.image.load('resource/Background/Background2.png')

    pos1 = pygame.Vector2(0, 0)
    pos2 = pygame.Vector2(Globals.CameraSize_X, 0)

def render():
    Globals.display.blit(Globals.Surface, Globals.Surface.get_rect())