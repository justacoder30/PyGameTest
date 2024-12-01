import pygame, Globals

DeltaTime = float
Clock = None
CameraSize_X = 0
CameraSize_Y = 0
Surface = None
P_pos = None
scroll_x = 0
scroll_y = 0
camera = pygame.Vector2
camera_bg = pygame.Vector2
running = True
IsLevelEnd = False
display = None

def Init():
    global Surface, Clock, CameraSize_X, CameraSize_Y


    Clock = pygame.time.Clock()
    Surface = pygame.Surface((CameraSize_X, CameraSize_Y))

def Updated():
    global DeltaTime, scroll_x, scroll_y

    DeltaTime = Clock.tick() / 1000


def CameraSize(camera_width, camera_height):
    global CameraSize_X, CameraSize_Y
    CameraSize_X = camera_width
    CameraSize_Y = camera_height
