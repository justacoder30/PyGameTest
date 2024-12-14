import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

text_font = pygame.font.SysFont("Helvetica", 30)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))
print("Hello\n World")

run = True
while run:

  screen.fill((255, 255, 255))

  draw_text("Hello World", text_font, (0, 0, 0), 220, 150)

  for event in pygame.event.get():
   if event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

pygame.quit()