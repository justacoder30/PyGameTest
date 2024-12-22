import pygame
from quadtree import *
from Manager.SoundManager import *

camera = pygame.Vector2(0, 0)
camera_bg = pygame.Vector2
running = True
IsLevelEnd = False
GameOver = False
ShowText = False
display = None
score = 0
Text = pygame.Surface
MapSize = pygame.Rect(0, 0, 0, 0)
static_quadtree = Quadtree
moving_quadtree = Quadtree


def Init():
    global Surface, Text, Clock, CameraSize_X, CameraSize_Y, text_font

    text_font = pygame.font.SysFont("Helvetica", 70, bold=True)
    Clock = pygame.time.Clock()
    Surface = pygame.Surface((CameraSize_X, CameraSize_Y), pygame.SRCALPHA)
    Text = pygame.Surface((1920, 1080), pygame.SRCALPHA)

def Updated():
    global DeltaTime

    DeltaTime = Clock.tick() / 1000


def CameraSize(camera_width, camera_height):
    global CameraSize_X, CameraSize_Y
    CameraSize_X = camera_width
    CameraSize_Y = camera_height
