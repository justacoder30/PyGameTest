import pygame, Globals, sys
sys.path.append("..")
import Entity.Map as TiledMap


class Camera:
    def __init__(self):
        self.width = TiledMap.Map.get_width()
        self.height = TiledMap.Map.get_height()
        self.camera_rect = pygame.Rect(0, 0, self.width, self.width)
    
    def Update(self, player):
        x = max(Globals.CameraSize_X - self.width, min(0, int(Globals.CameraSize_X/2) - player.get_center().x))
        y = max(Globals.CameraSize_Y - self.height, min(0, int(Globals.CameraSize_Y/2) - player.get_center().y))

        self.camera_rect = pygame.Rect(x, y, self.width, self.height)
        Globals.camera_rect = self.camera_rect