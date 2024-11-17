import pygame, sys, time
# StaticObstacle((800,600),(100,200),[all_sprites,collision_sprites])
# StaticObstacle((900,200),(200,10),[all_sprites,collision_sprites])
# MovingVerticalObstacle((200,300),(200,60),[all_sprites,collision_sprites])
# MovingHorizontalObstacle((850,350),(100,100),[all_sprites,collision_sprites])
# player = Player(all_sprites,collision_sprites)



# loop

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
colliders = []

class StaticObstacle:
	def __init__(self, x, y, w, h):
		self.rect = pygame.Rect(x, y, w, h)
		self.pos = pygame.Vector2(x, y)

	def Update():
		pass

	def Draw(self):
		pygame.draw.rect(screen, "yellow", self.rect)
		
class Player:
	def __init__(self, x, y, w, h):
		self.rect = pygame.Rect(x, y, w, h)
		self.pos = pygame.Vector2(x, y)

	def Update(self):
		pass

	def Draw(self):
		pygame.draw.rect(screen, "red", pygame.Rect(self.pos.x, self.pos.y,50,50))

# sprite setup
obj = StaticObstacle(800,600,100,200)
player = Player(player_pos.x, player_pos.y,50,50)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_w]:
        player.pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player.pos.y += 300 * dt
    if keys[pygame.K_a]:
        player.pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player.pos.x += 300 * dt

    print(player.pos)

    obj.Draw()
    player.Draw()


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()


