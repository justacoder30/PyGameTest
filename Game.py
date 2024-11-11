import pygame, Renderder, Globals, Renderder
import Entity.Map as Map
import Manager.InputManager as InputManager
from Camera import *
from Manager.AnimationManager import *
from Animation import *
from Entity.Player import *
from Manager.EnemyManager import *

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        Globals.CameraSize(480, 270)
        Globals.Init()
        Renderder.SetResolution(1920, 1080)

        self.running = True
        self.map = Map()
        self.player = Player()
        self.enemy = EnemyManager()
        self.camera = Camera()
        self.bg = pygame.image.load('resource/Background/Background1.png')
        self.btn = pygame.image.load('resource/Button/Play Button.png')
        self.playgame = False
        self.color: None

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage

    def Updated(self):
        
        self.camera.Update(self.player)
        Globals.Updated()
        InputManager.Update()
        self.enemy.Update(self.player)
        self.player.Update()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
        btn_rect = pygame.rect.Rect(176.00 * Renderder.scale, 96.00 * Renderder.scale, 120.00 * Renderder.scale, 40.00 * Renderder.scale)
        if mouse_rect.colliderect(btn_rect):
            self.color = "green"
        else:
            self.color = "white"

        if mouse_rect.colliderect(btn_rect) and mouse_clicked:
            self.playgame = True

    def Draw(self):
        # fill the Surface with a color to wipe away anything from last frame
        Globals.Surface.fill("blue")

        # RENDER YOUR GAME HERE
        self.map.Draw()
        self.enemy.Draw()
        self.player.Draw()
        if not self.playgame:
            Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
            Globals.Surface.blit(pygame.transform.scale(self.changColor(self.btn, self.color), (120.00, 40.00)), (176.00, 96.00))
        
        # flip() the display to put your work on Surface
        Renderder.render()
        pygame.display.update()
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
        pygame.quit()