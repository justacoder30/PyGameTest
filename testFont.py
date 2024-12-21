import pygame

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

text_font = pygame.font.SysFont("Helvetica", 70)

#function for outputting text onto the screen
def draw_text(text, font, color, x, y):
  img = font.render(text, True, color)
  screen.blit(img, (x, y))
print("Hello\n World")

run = True
while run:

  screen.fill((0, 0, 0))

  img = text_font.render("Hello World", True, (255, 255, 255))
  posx = (screen.get_width() - img.get_width())/2
  posy = (screen.get_height() - img.get_height())/2
  draw_text("Hello World", text_font, (255, 255, 255), posx, posy)
  print(img.get_width())

  for event in pygame.event.get():
   if event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

pygame.quit()