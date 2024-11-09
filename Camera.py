import pygame, Globals, sys
sys.path.append("..")
import Entity.Map as TiledMap

class Camera:
    def __init__(self):
        self.width = TiledMap.Map.get_width()
        self.height = TiledMap.Map.get_height()
        self.camera_rect = pygame.Rect(0, 0, self.width, self.width)
        self.current_pos = pygame.Vector2(0, 0)
        self.previous_pos = pygame.Vector2(0, 0)
        self.speed = 0.08
    
    def Update(self, player):
        self.current_pos.x = Globals.CameraSize_X/2 - player.get_center().x
        self.current_pos.y = Globals.CameraSize_Y/2 - player.get_center().y

        self.current_pos.x = pygame.math.clamp(self.current_pos.x, Globals.CameraSize_X - self.width, 0)
        self.current_pos.y = pygame.math.clamp(self.current_pos.y, Globals.CameraSize_Y - self.height, 0)

        x = pygame.math.lerp(self.previous_pos.x, self.current_pos.x, self.speed)
        y = pygame.math.lerp(self.previous_pos.y, self.current_pos.y, self.speed)

        x = round(x, 3)
        y = round(y, 3)

        Globals.camera_rect = pygame.Vector2(x, y)
        self.previous_pos = pygame.Vector2(x, y)