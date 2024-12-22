import pygame, pytmx, sys, Globals
# from pytmx.util_pygame import load_pygame
import pytmx
sys.path.append('..')

from Entity.Entity import *
from Camera import *

TileSize = 16

layers = {
    'Terrain': 0,
    'Trap': 1,
    'Decorate': 2,
}

class MapTile(Entity):
    def __init__(self, pos: pygame.Vector2, img: pygame.surface.Surface, groups, isplatfrom = True, isTrap = False):
        super().__init__(groups)
        self.pos = pos
        self.isplatfrom = isplatfrom
        self.isTrap = isTrap
        self.img = img
        # self.img.fill("red")
        self.rect = self.img.get_rect(topleft = self.pos)
        self.old_rect = self.rect.copy()

    def Update(self):
        # Globals.static_quadtree.insert(self)
        pass

    def Draw(self):
        self.DrawSprite(self.img, self.pos)

class Map():
    def __init__(self, level, groups):
        Map.max_x, Map.max_y = 0, 0
        Map.tiled_map = pytmx.load_pygame(f'resource/Map1/map{level}.tmx')
        for layer in layers:
            isplatfrom = True if layer == 'Terrain' else False
            isTrap = True if layer == 'Trap' else False
            for x, y, img in Map.tiled_map.get_layer_by_name(layer).tiles():
                Map.max_x = x if x > Map.max_x else Map.max_x
                Map.max_y = y if y > Map.max_y else Map.max_y
                pos = pygame.Vector2(x * TileSize, y * TileSize)
                MapTile(pos, img, groups, isplatfrom, isTrap)

        Globals.MapSize.w= Map.get_width()
        Globals.MapSize.h = Map.get_height()

        for sprite in groups:
            if not sprite.isplatfrom and not sprite.isTrap :
                continue
            Globals.static_quadtree.insert(sprite)

    @classmethod
    def get_width(cls):
        return (Map.max_x + 1) * TileSize

    @classmethod
    def get_height(cls):
        return (Map.max_y + 1) * TileSize
    
    @classmethod   
    def GetPosition(cls, obj_name):
        obj_group = cls.tiled_map.get_layer_by_name(obj_name)
        for obj in obj_group:
            return pygame.Vector2(obj.x, obj.y)
    
    @classmethod   
    def GetListPosition(cls, obj_name):
        obj_group = cls.tiled_map.get_layer_by_name(obj_name)
        pos_list = []
        for obj in obj_group:
            pos_list.append(pygame.Vector2(obj.x, obj.y))
        return pos_list
        
    @classmethod 
    def GetRectList(cls, obj_name):
        obj_group = cls.tiled_map.get_layer_by_name(obj_name)
        rect_list = []
        for obj in obj_group:
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            rect_list.append(rect)
        return rect_list
    
    # def Update(self):
    #     pass

    # def Draw(self):
    #     Globals.Surface.blit(self.map, (0 + Globals.camera.x, 0 + Globals.camera.y))

