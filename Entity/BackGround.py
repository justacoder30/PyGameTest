import pygame, Globals, sys
sys.path.append('..')
# from Entity.Block import *

class BackGround:
    def __init__(self):

        bg1 = self.GetImg('resource/Background/layers/sky.png')
        bg2 = self.GetImg('resource/Background/layers/clouds_1.png')
        bg3 = self.GetImg('resource/Background/layers/rocks.png')
        bg4 = self.GetImg('resource/Background/layers/clouds_2.png')
        bg5 = self.GetImg('resource/Background/layers/ground_1.png')
        bg6 = self.GetImg('resource/Background/layers/ground_2.png')
        bg7 = self.GetImg('resource/Background/layers/plant.png')

        self.bg_list = [ bg1, bg2, bg3, bg4, bg5, bg6, bg7]

        self.bg_width = Globals.CameraSize_X
        self.scroll = 0
        self.speed = 0.6
        self.cloud_speed = [10, 20]
        self.pos_cloud = [0, 0]
        # Block.Obj.append(self)
        

    def GetImg(self, f_path):
        return pygame.transform.scale(pygame.image.load(f_path).convert_alpha(), Globals.Surface.get_size())

    def Update(self):
        # self.speed = 0.6
        # self.scroll = abs(Globals.camera.x * self.speed) % self.bg_width * -1
        for i in range(2):
            self.pos_cloud[i] -= self.cloud_speed[i] * Globals.DeltaTime
            if self.pos_cloud[i] <= -self.bg_width:
                self.pos_cloud[i] = 0
        pass

    def Draw(self):
        # for i in range(7):
        #     self.speed = 0.1
        #     for n in range(len(self.bg_list)):
        #         Globals.Surface.blit(self.bg_list[n], (i * self.bg_width + Globals.camera.x * self.speed, 0))
        #         self.speed+=0.1

        for i in range(7):
            self.speed = 0.1
            # self.scroll = abs(Globals.camera.x * self.speed) % self.bg_width * -1
            for layer in range(len(self.bg_list)):
                pos_x = 0
                if layer == 1:
                    pos_x = self.pos_cloud[0] + i * self.bg_width + Globals.camera.x * self.speed
                elif layer == 3:
                    pos_x = self.pos_cloud[1] + i * self.bg_width + Globals.camera.x * self.speed
                else:
                    pos_x = i * self.bg_width + Globals.camera.x * self.speed
                Globals.Surface.blit(self.bg_list[layer], (pos_x, 0))
                self.speed+=0.1