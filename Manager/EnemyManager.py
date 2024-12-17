import sys
sys.path.append('..')

from Entity.Skeleton import *
from Entity.Map import *

class EnemyManager:
    enemy_list = []
    def __init__(self, player):
        enemy_list = []
        self.player = player
        
        for pos in Map.GetListPosition("SkeletonPosition"):
            skeleton = Skeleton(pos, self.player)
            enemy_list.append(skeleton)

        EnemyManager.enemy_list = enemy_list
    
    @classmethod
    def GetEnemyList(self):
        return EnemyManager.enemy_list

    def Update(self):
        for skeleton in self.enemy_list:
            skeleton.Update()
            if skeleton.IsRemoved:
                self.enemy_list.remove(skeleton)

    def Draw(self):
        for skeleton in self.enemy_list:
            skeleton.Draw()
        