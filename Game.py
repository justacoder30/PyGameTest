import pygame, Renderder
import Manager.InputManager as InputManager
import pygame._sdl2 as sdl2
import Globals

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        Globals.CameraSize(256, 128)
        Globals.Init()
        Renderder.Init()
        Renderder.SetResolution(1280, 720)

        self.running = True

        self.player_pos = pygame.Vector2(Globals.Screen.get_width() / 2, Globals.Screen.get_height() / 2)
        self.speed = 100

        self.img = pygame.image.load('img/hearts.png')

        # pygame.display.toggle_fullscreen()

    def LoadContent():
        pass

    def Updated(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        Globals.Updated()
        InputManager.Update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
         
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= self.speed * Globals.DeltaTime
        if keys[pygame.K_s]:
            self.player_pos.y += self.speed * Globals.DeltaTime
        if keys[pygame.K_a]:
            self.player_pos.x -= self.speed * Globals.DeltaTime
        if keys[pygame.K_d]:
            self.player_pos.x += self.speed * Globals.DeltaTime
            

    def Draw(self):
        # fill the screen with a color to wipe away anything from last frame
        Globals.Screen.fill("blue")

        # RENDER YOUR GAME HERE
        Globals.Screen.blit(self.img, (self.player_pos.x, self.player_pos.y))

        # flip() the display to put your work on screen
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
            pygame.display.update()
        pygame.quit()