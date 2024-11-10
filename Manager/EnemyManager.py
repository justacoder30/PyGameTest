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
        # self.skeleton_list[0].Update(player)

        # if self.skeleton_list[0].IsRemoved:
        #     self.skeleton_list.remove(self.skeleton_list[0])
        # print(self.skeleton_list[0].ObjectDistance(player))

    def Draw(self):
        for skeleton in self.skeleton_list:
            skeleton.Draw()
        # self.skeleton_list[0].Draw()
        