import pygame, pytmx, sys
sys.path.append('..')

from Entity.Entity import *

class Map(Entity):
    map_img = pygame.image.load('resource/Map/Dungeon Map.png')
    tiled_map = pytmx.TiledMap('resource/Map/Map.tmx')
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)

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

    def Draw(self):
        super().DrawSprite(self.map_img, self.pos)

