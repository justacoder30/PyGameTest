import pygame

class Animation:
    def __init__(self, file_path, framecount, frameSpeed = 0.08, isAnimationRunning = False):
        self.texture = pygame.image.load(file_path)
        self.texture_flip = pygame.transform.flip(self.texture, True, False)
        self.FrameCount = framecount
        self.FrameSpeed = frameSpeed
        self.IsAnimationRunning = isAnimationRunning
        self.CurrentFrame = 0
        self.FrameWidth = self.texture.get_width() / self.FrameCount
        self.FrameHeight = self.texture.get_height