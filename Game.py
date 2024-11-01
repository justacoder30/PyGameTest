import pygame
import pygame._sdl2 as sdl2
import Globals

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        WIDTH, HEIGHT = (256, 128)
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)


        # # choose the initial scale factor for the window
        initial_scale_factor = 3  # <-- adjustable
        window = sdl2.Window.from_display_module()
        window.size = (WIDTH * initial_scale_factor, HEIGHT * initial_scale_factor)
        window.position = sdl2.WINDOWPOS_CENTERED
        window.show()   

        # # bonus: specify the color of the out-of-bounds area in RESIZABLE mode (it's black by default)
        # OUTER_FILL_COLOR = "plum4"
        # renderer = sdl2.Renderer.from_window(window)
        # renderer.draw_color = pygame.Color(OUTER_FILL_COLOR)

        Globals.Clock = pygame.time.Clock()
        Globals.Clock.tick(60) # limits FPS to 60
        self.running = True
        self.FullScreen = False

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.speed = 300

        self.img = pygame.image.load('img/hearts.png')

        # pygame.display.toggle_fullscreen()

    def LoadContent():
        pass

    def Updated(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        Globals.Updated()
        # pygame.draw.rect()

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
        if keys[pygame.K_F11]:
            if self.FullScreen:
                pygame.display.toggle_fullscreen()
                self.FullScreen = False
            else:
                pygame.display.toggle_fullscreen()
                self.FullScreen = True

    def Draw(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("blue")

        # RENDER YOUR GAME HERE
        # pygame.draw.circle(self.screen, "red", self.player_pos, 100)
        # pygame.draw.rect(self.screen, "red", [0, 0, 100, 100])
        self.screen.blit(self.img, (self.player_pos.x, self.player_pos.y))

        # flip() the display to put your work on screen
        pygame.display.flip()
        

    def Run(self):
        while self.running:
            self.Updated()
            self.Draw()
        pygame.quit()