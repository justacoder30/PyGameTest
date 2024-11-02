import pygame, Globals

DeltaTime = float
Clock = None
CameraSize_X = 0
CameraSize_Y = 0
Surface = None
P_pos = None
scroll_x = 0
scroll_y = 0
camera_rect = None

def Init():
    global Surface, Clock

    Clock = pygame.time.Clock()
    Clock.tick(60) # limits FPS to 60
    Surface = pygame.Surface((CameraSize_X, CameraSize_Y))

def Updated():
    global DeltaTime, scroll_x, scroll_y

    DeltaTime = Clock.tick(60) / 1000

    # scroll_x += (player.get_center().x- Globals.Surface.get_width() / 2 - scroll_x) / 30
    # scroll_y += (player.get_center().y - Globals.Surface.get_height() / 2 - scroll_y) / 30
    # scroll_x, scroll_y = int(scroll_x), int(scroll_y)


def CameraSize(camera_width, camera_height):
    global CameraSize_X, CameraSize_Y
    CameraSize_X = camera_width
    CameraSize_Y = camera_height
