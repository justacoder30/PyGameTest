import pygame, Renderder, Globals, Renderder
import Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Entity.Flag import *
from Entity.Block import *
from Entity.BackGround import *
from Manager.EnemyManager import *

list = [1, 'a', 2.4, 2, 8,3]

nums = [i for i in list if type(i) == int]
print(nums)

# bg = BackGround()
rect = Block(240.00, 592.00, 80.00, 32.00, 'vertical')
rect2 = Block(320.00, 320.00, 80.00, 32.00,'horizontal')
player = Player()
enemy = EnemyManager(player)
flag = Flag(player)
camera = Camera(player)

entities = [
    bg,
    rect,
    rect2,
    enemy,
    flag,
    player,
]

blocks = [entity for entity in entities if type(entity) == Block]

print(blocks)