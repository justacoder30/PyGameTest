
import Entity.Entity as enity
import pygame, Globals, sys, Entity
sys.path.append('..')
# from Entity.Block import *

class BackGround(enity.Entity):
    def __init__(self, groups):
        super().__init__(groups)
        bg1 = self.GetImg('resource/img/Background/layers/sky.png')
        bg2 = self.GetImg('resource/img/Background/layers/clouds_1.png')
        bg3 = self.GetImg('resource/img/Background/layers/rocks.png')
        bg4 = self.GetImg('resource/img/Background/layers/clouds_2.png')
        bg5 = self.GetImg('resource/img/Background/layers/ground_1.png')
        bg6 = self.GetImg('resource/img/Background/layers/ground_2.png')
        bg7 = self.GetImg('resource/img/Background/layers/plant.png')
        self.bg = self.GetImg('resource/img/Background/Background2.png')

        self.bg_list = [ bg1, bg2, bg3, bg4, bg5, bg6, bg7]

        self.bg_width = Globals.CameraSize_X
        self.scroll = 0
        self.speed = 0.6
        self.cloud_speed = [10, 20]
        self.pos_cloud = [0, 0]
        

    def GetImg(self, f_path):
        return pygame.transform.scale(pygame.image.load(f_path).convert_alpha(), Globals.Surface.get_size())

    def Update(self):
        return
        for i in range(2):
            self.pos_cloud[i] -= self.cloud_speed[i] * Globals.DeltaTime
            if self.pos_cloud[i] <= -self.bg_width:
                self.pos_cloud[i] = 0

    def Draw(self):
        # for i in range(5):
        #     speed = 0.1
        #     for layer in range(len(self.bg_list)):
        #         pos_x = i * self.bg_width + Globals.camera.x * speed
        #         if layer == 1:
        #             pos_x += self.pos_cloud[0]
        #         elif layer == 3:
        #             pos_x += self.pos_cloud[1]
        #         rect = Globals.Surface.get_rect(left = pos_x)
        #         super().DrawOnly(self.bg_list[layer], (pos_x, 0), rect)
        #         speed+=0.1
        self.DrawOnly(self.bg, (0, 0), self.bg.get_rect())