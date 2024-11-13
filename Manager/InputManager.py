import Renderder, pygame, Globals

CurrentKey = None
PreviousKey = None
PreviousMouse = None
CurrentMouse = None

def Update():
    global CurrentKey, PreviousKey

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    PreviousKey = CurrentKey
    CurrentKey = pygame.key.get_pressed()

    if(CurrentKey[pygame.K_F11] and PreviousKey[pygame.K_F11] == False):
        Renderder.FullScreenToggle()

    