import pygame, sys
from pygame.locals import *

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)

pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('P.Earth')

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('Text', False, "red")
screen.blit(text_surface, (size[0] / 2, size[1] / 2))
while 1: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:           
            pygame.display.update() 

import time

direction = ''
print('Welcome to Earth')
pygame.draw.rect(screen, RED, [55,500,10,5], 0)
time.sleep(1)