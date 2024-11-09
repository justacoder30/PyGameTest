import pygame

a, b = 108.8, 110
i = 0 

while(i <= 10):
    a = pygame.math.lerp(a, b, 0.04)
    a = round(a, 1)
    print(a, b)
    i+=1