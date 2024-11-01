import Renderder, pygame

CurrentKey = None
PreviousKey = None

def Update():
    global CurrentKey, PreviousKey
    CurrentKey = pygame.key.get_pressed()

    if(CurrentKey[pygame.K_F11] == True and PreviousKey[pygame.K_F11] == False):
        Renderder.FullScreenToggle()

    PreviousKey = CurrentKey