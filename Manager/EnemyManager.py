import sys
sys.path.append('..')

from Entity.Skeleton import *
from Entity.Map import *

class EnemyManager:
    skeleton_list = []
    def __init__(self, player):
        skeleton_list = []
        self.player = player
        for pos in Map.GetListPosition("SkeletonPosition"):
            skeleton = Skeleton(pos, self.player)
            skeleton_list.append(skeleton)

        EnemyManager.skeleton_list = skeleton_list
    
    @classmethod
    def GetEnemyList(self):
        return EnemyManager.skeleton_list

    def Update(self):
        for skeleton in self.skeleton_list:
            skeleton.Update()
            if skeleton.IsRemoved:
                self.skeleton_list.remove(skeleton)

    def Draw(self):
        for skeleton in self.skeleton_list:
            skeleton.Draw()
        