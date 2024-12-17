import pygame, Globals, sys
sys.path.append("..")
import Entity.Map as TiledMap

class Camera:
    def __init__(self, player):
        self.player = player
        
        Camera.rect = pygame.Rect(0, 0, Globals.CameraSize_X / 2, Globals.CameraSize_Y)
        self.current_pos = pygame.Vector2(0, 0)
        self.previous_pos = self.current_pos
        self.speed = 0.05

    @classmethod
    def SetSize(cls, width, height):
        Camera.width = width
        Camera.height = height
        Globals.CameraSize(Camera.width, Camera.height)
    
    def Update(self):
        self.current_pos.x = pygame.math.clamp(Globals.CameraSize_X/2 - self.player.get_center().x, Globals.CameraSize_X - Globals.MapSize.width, 0)
        self.current_pos.y = pygame.math.clamp(Globals.CameraSize_Y/2 - self.player.get_center().y, Globals.CameraSize_Y - Globals.MapSize.height, 0)

        x = round(pygame.math.lerp(self.previous_pos.x, self.current_pos.x, self.speed))
        y = round(pygame.math.lerp(self.previous_pos.y, self.current_pos.y, self.speed))

        Globals.camera_bg = pygame.Vector2(self.current_pos.x, self.current_pos.y)
        Camera.rect = pygame.Rect(-x, -y, Globals.CameraSize_X, Globals.CameraSize_Y)
        Globals.camera = pygame.Vector2(x, y)
        self.previous_pos = Globals.camera