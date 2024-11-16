import sys
sys.path.append('..')

from Entity.Skeleton import *
from Entity.Map import *

class EnemyManager:
    skeleton_list = []
    def __init__(self):
        for pos in Map.GetListPosition("SkeletonPosition"):
            skeleton = Skeleton(pos)
            self.skeleton_list.append(skeleton)
    
    @classmethod
    def GetEnemyList(self):
        return self.skeleton_list

    def Update(self, player):
        for skeleton in self.skeleton_list:
            skeleton.Update(player)
            if skeleton.IsRemoved:
                self.skeleton_list.remove(skeleton)

    def Draw(self):
        for skeleton in self.skeleton_list:
            skeleton.Draw()
        