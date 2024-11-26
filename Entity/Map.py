import pygame, pytmx, sys
from pytmx.util_pygame import load_pygame
sys.path.append('..')

from Entity.Entity import *
from Entity.Block import *

TileSize = 16

class MapTile(Entity):
    
    def __init__(self, x, y, img, Tiles):
        self.pos = pygame.Vector2(x, y)
        self.img = img
        self.img.fill('red')
        self.rect = self.img.get_rect(topleft = self.pos)
        self.old_rect = self.rect.copy()
        Tiles.append(self)

    def Update():
        pass

    def Draw(self):
        super().DrawSprite(self.img, self.pos)

class Map(Entity):
    map_img = None
    tiled_map = None
    Tiles = []
    def __init__(self, level):
        super().__init__()
        Map.Tiles = []
        tiled_map = load_pygame(f'resource/Map/Map{level}.tmx')
        map_img = pygame.image.load('resource/Map/Map1.png').convert_alpha()

        for x, y, img in tiled_map.get_layer_by_name('Tile Layer 1').tiles():
            MapTile(x * TileSize, y * TileSize, img, Map.Tiles)

        Map.tiled_map = tiled_map
        Map.map_img = map_img

    @classmethod
    def get_width(cls):
        return cls.map_img.get_rect().width

    @classmethod
    def get_height(cls):
        return cls.map_img.get_rect().height
    
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
    def GetListBound(cls, obj_name):
        obj_group = cls.tiled_map.get_layer_by_name(obj_name)
        list_bound = []
        for obj in obj_group:
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            list_bound.append(rect)
        return list_bound
    
    @classmethod 
    def GetTilesBound(cls):
        list_bound = []
        for obj in Map.Tiles:
            list_bound.append(obj.rect)
        return list_bound
    
    def Update(self):
        pass

    def Draw(self):
        for tile in Map.Tiles:
            tile.Draw()

