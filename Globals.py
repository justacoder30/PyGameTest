import pygame
from quadtree import *

P_pos = None
camera = pygame.Vector2(0, 0)
camera_bg = pygame.Vector2
running = True
IsLevelEnd = False
GameOver = False
ShowText = False
display = None
Text = pygame.Surface
MapSize = pygame.Rect(0, 0, 0, 0)
static_quadtree = Quadtree
moving_quadtree = Quadtree

def Init():
    global Surface, Text, Clock, CameraSize_X, CameraSize_Y


    Clock = pygame.time.Clock()
    Surface = pygame.Surface((CameraSize_X, CameraSize_Y), pygame.SRCALPHA)

def Updated():
    global DeltaTime

    DeltaTime = Clock.tick() / 1000


def CameraSize(camera_width, camera_height):
    global CameraSize_X, CameraSize_Y
    CameraSize_X = camera_width
    CameraSize_Y = camera_height
