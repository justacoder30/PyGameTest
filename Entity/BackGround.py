import pygame, Globals, sys
sys.path.append('..')

class BackGround:
    def __init__(self):

        bg1 = pygame.transform.scale(pygame.image.load('resource/Background/layers/sky.png').convert_alpha(), Globals.Surface.get_size())
        bg2 = pygame.transform.scale(pygame.image.load('resource/Background/layers/clouds_1.png').convert_alpha(), Globals.Surface.get_size())
        bg3 = pygame.transform.scale(pygame.image.load('resource/Background/layers/rocks.png').convert_alpha(), Globals.Surface.get_size())
        bg4 = pygame.transform.scale(pygame.image.load('resource/Background/layers/clouds_2.png').convert_alpha(), Globals.Surface.get_size())
        bg5 = pygame.transform.scale(pygame.image.load('resource/Background/layers/ground_1.png').convert_alpha(), Globals.Surface.get_size())
        bg6 = pygame.transform.scale(pygame.image.load('resource/Background/layers/ground_2.png').convert_alpha(), Globals.Surface.get_size())
        bg7 = pygame.transform.scale(pygame.image.load('resource/Background/layers/plant.png').convert_alpha(), Globals.Surface.get_size())

        self.bg_list = [ bg1, bg2, bg3, bg4, bg5, bg6, bg7]
        self.bg = pygame.image.load('resource/Background/Background2.png').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, Globals.Surface.get_size())

        self.bg_width = Globals.CameraSize_X
        self.scroll = 0
        self.speed = 0.6
    def Update(self):
        self.speed = 0.6
        self.scroll = abs(Globals.camera.x * self.speed) % self.bg_width * -1

    def Draw(self):
        pass
        # for i in range(2):
        #     Globals.Surface.blit(self.bg, (i * self.bg_width + int(self.scroll), 0))
                
        for i in range(2):
            for n in range(len(self.bg_list)):
                Globals.Surface.blit(self.bg_list[n], (i * self.bg_width + int(self.scroll), 0))