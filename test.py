import pygame

def changColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

pygame.init()
window = pygame.display.set_mode((1280, 720))

image = pygame.image.load('resource/img/Run.png').convert_alpha()
hue = 0

clock = pygame.time.Clock()
nextColorTime = 0
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    color_image = changColor(image, "red")

    window.fill("blue")
    window.blit(color_image, color_image.get_rect(center = window.get_rect().center))
    pygame.display.flip()

pygame.quit()
exit()