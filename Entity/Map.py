import pygame, pytmx, sys
sys.path.append('..')

from Entity.Entity import *

# class Map(Entity):
#     map_img = pygame.image.load('resource/Map2/map.png')
#     tiled_map = pytmx.TiledMap('resource/Map2/map.tmx')
#     def __init__(self):
#         self.pos = (0, 0)

#     @classmethod
#     def get_width(cls):
#         return cls.map_img.get_rect().width

#     @classmethod
#     def get_height(cls):
#         return cls.map_img.get_rect().height
    
#     @classmethod   
#     def GetPosition(cls, obj_name):
#         obj_group = cls.tiled_map.get_layer_by_name(obj_name)
#         for obj in obj_group:
#             return pygame.Vector2(obj.x, obj.y)
        
#     @classmethod 
#     def GetListBound(cls, obj_name):
#         obj_group = cls.tiled_map.get_layer_by_name(obj_name)
#         dist_pos = []
#         for obj in obj_group:
#             pos = pygame.Vector2(obj.x, obj.y)
#             diction = {}
#             diction.update({"left": obj.x, 
#                             "top": obj.y,
#                             "right": obj.width,
#                             "bottom": obj.height
#                             })
#             dist_pos.append(diction)
#         return dist_pos

#     def Draw(self):
#         Globals.Surface.blit(self.map_img, (0 + Globals.camera_rect.x, 0 + Globals.camera_rect.y))

map_img = pygame.image.load('resource/Map2/map.png')
tiled_map = pytmx.TiledMap('resource/Map2/map.tmx')

def GetListBound(cls, obj_name):
        obj_group = cls.tiled_map.get_layer_by_name(obj_name)
        dist_pos = []
        for obj in obj_group:
            pos = pygame.Vector2(obj.x, obj.y)
            diction = {}
            diction.update({"left": obj.x, 
                            "top": obj.y,
                            "right": obj.width,
                            "bottom": obj.height
                            })
            dist_pos.append(diction)
        return dist_pos

for obj in GetListBound():
    print(obj["width"])
