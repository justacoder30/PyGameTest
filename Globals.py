import pygame, Globals

P_pos = None
camera = pygame.Vector2
camera_bg = pygame.Vector2
running = True
IsLevelEnd = False
ShowText = False
display = None
Text = pygame.Surface

def Init():
    global Surface, Text, Clock, CameraSize_X, CameraSize_Y


    Clock = pygame.time.Clock()
    Surface = pygame.Surface((CameraSize_X, CameraSize_Y), pygame.SRCALPHA)

def Updated():
    global DeltaTime, scroll_x, scroll_y

    DeltaTime = Clock.tick() / 1000


def CameraSize(camera_width, camera_height):
    global CameraSize_X, CameraSize_Y
    CameraSize_X = camera_width
    CameraSize_Y = camera_height
