import pygame

class Sound():
    def __init__(self, f_path, volume):
        self.sound = pygame.mixer.Sound(f_path)
        self.sound.set_volume(volume)

    def play(self):
        self.sound.play()