import pygame, Globals

class Quadtree:
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.sprites = []
        self.topleft = None
        self.topright = None
        self.bottomleft = None
        self.bottomright = None
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        topleft = pygame.Rect(x + w/2, y, w/2, h/2)
        self.topleft = Quadtree(topleft, self.capacity)
        topright = pygame.Rect(x, y, w/2, h/2)
        self.topright = Quadtree(topright, self.capacity)
        bottomleft = pygame.Rect(x + w/2, y + h/2, w/2, h/2)
        self.bottomleft = Quadtree(bottomleft, self.capacity)
        bottomright = pygame.Rect(x, y + h/2, w/2, h/2)
        self.bottomright = Quadtree(bottomright, self.capacity)
        self.divided = True

    def insert(self, sprite):
        if not self.boundary.colliderect(sprite.rect):
            return

        if not self.divided:
            if len(self.sprites) < self.capacity:
                self.sprites.append(sprite)
            else:
                self.subdivide()
                self.sprites.append(sprite)
                for sprite in self.sprites:
                    self.topleft.insert(sprite)
                    self.topright.insert(sprite)
                    self.bottomleft.insert(sprite)
                    self.bottomright.insert(sprite)
                self.sprites = []
        else:
            self.topleft.insert(sprite)
            self.topright.insert(sprite)
            self.bottomleft.insert(sprite)
            self.bottomright.insert(sprite)

    def query(self, range: pygame.Rect, found=None):
        if found is None:
            found = []
        if not self.boundary.colliderect(range):
            return
        else:
            for sprite in self.sprites:
                if range.colliderect(sprite.rect):
                    found.append(sprite)
        if self.divided:
            self.topleft.query(range, found)
            self.topright.query(range, found)
            self.bottomleft.query(range, found)
            self.bottomright.query(range, found)
            return found

    def draw(self):
        pygame.draw.rect(Globals.Surface, (0, 0, 255), (self.boundary.x + Globals.camera.x, self.boundary.y + Globals.camera.y, self.boundary.w, self.boundary.h), 1)

        if self.divided:
            self.topleft.draw()
            self.topright.draw()
            self.bottomleft.draw()
            self.bottomright.draw()

    def draw_sprites(self, screen):
        if self.divided:
            self.topleft.draw_sprites(screen)
            self.topright.draw_sprites(screen)
            self.bottomleft.draw_sprites(screen)
            self.bottomright.draw_sprites(screen)
        else:
            for sprite in self.sprites:
                pygame.draw.rect(screen, (255, 0, 0), (sprite.x, sprite.y, sprite.w, sprite.h), 3)
