import pygame

DeltaTime = float
Clock = None
CameraSize_X = 0
CameraSize_y = 0
Screen = None

def Init():
    global Screen, Clock

    Clock = pygame.time.Clock()
    Clock.tick(60) # limits FPS to 60
    Screen = pygame.display.set_mode((CameraSize_X, CameraSize_y), pygame.SCALED | pygame.FULLSCREEN, vsync=1)

def Updated():
    global DeltaTime
    DeltaTime = Clock.tick(60) / 1000

def CameraSize(camera_width, camera_height):
    global CameraSize_X, CameraSize_y
    CameraSize_X = camera_width
    CameraSize_y = camera_height
