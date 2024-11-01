import Renderder, pygame

CurrentKey = None
PreviousKey = None

def Update():
    global CurrentKey, PreviousKey

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    CurrentKey = pygame.key.get_pressed()

    if(CurrentKey[pygame.K_F11] and PreviousKey[pygame.K_F11] == False):
        Renderder.FullScreenToggle()

    PreviousKey = CurrentKey