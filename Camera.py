import pygame, Globals, sys
sys.path.append("..")
import Entity.Map as TiledMap

class Camera:
    def __init__(self, player):
        self.player = player
        self.width = TiledMap.Map.get_width()
        self.height = TiledMap.Map.get_height()
        # print(self.width, self.height)
        self.current_pos = pygame.Vector2(0, 0)
        self.previous_pos = self.current_pos
        self.speed = 0.05
    
    def Update(self):
        self.current_pos.x = pygame.math.clamp(Globals.CameraSize_X/2 - self.player.get_center().x, Globals.CameraSize_X - self.width, 0)
        self.current_pos.y = pygame.math.clamp(Globals.CameraSize_Y/2 - self.player.get_center().y, Globals.CameraSize_Y - self.height, 0)

        x = round(pygame.math.lerp(self.previous_pos.x, self.current_pos.x, self.speed))
        y = round(pygame.math.lerp(self.previous_pos.y, self.current_pos.y, self.speed))

        Globals.camera_bg = pygame.Vector2(self.current_pos.x, self.current_pos.y)
        Globals.camera = pygame.Vector2(x, y)
        self.previous_pos = Globals.camera