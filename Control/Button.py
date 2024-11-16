import pygame, sys
sys.path.append('..')
import Renderder, Globals

class Button:
    def __init__(self, f_path, rect: pygame.Rect):
        self.btn = pygame.image.load(f_path).convert_alpha()
        self.btn_rect = rect
        self.btn_rect_scale = pygame.rect.Rect(rect.x * Renderder.scale, 
                                         rect.y * Renderder.scale, rect.width * Renderder.scale, 
                                         rect.height * Renderder.scale)
        self.color = 'white'
        self.isHovering = False
        self.currentMouse = False
        self.previousMouse = False
        self.isClick = False

    def changColor(self, image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)

        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage
    
    def Update(self):
        self.previousMouse = self.currentMouse
        self.currentMouse = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

        if mouse_rect.colliderect(self.btn_rect_scale):
            self.isHovering = True
        else:
            self.isHovering = False

        if self.isHovering and not self.currentMouse and self.previousMouse:
            self.isClick = True

    def Draw(self):
        self.color = "white"
        if self.isHovering:
            self.color = "green"

        Globals.Surface.blit(pygame.transform.scale(self.changColor(self.btn, self.color), 
                                                    (self.btn_rect.width, self.btn_rect.height)), 
                                                    (self.btn_rect.x, self.btn_rect.y))
