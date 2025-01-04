import pygame, Globals

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.top = y
        self.bottom = y + h
        self.left = x
        self.right = x + w
        
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
        topleft = Rectangle(x + w/2, y, w/2, h/2)
        self.topleft = Quadtree(topleft, self.capacity)
        topright = Rectangle(x, y, w/2, h/2)
        self.topright = Quadtree(topright, self.capacity)
        bottomleft = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.bottomleft = Quadtree(bottomleft, self.capacity)
        bottomright = Rectangle(x, y + h/2, w/2, h/2)
        self.bottomright = Quadtree(bottomright, self.capacity)
        self.divided = True
    
    def checkcollide(self, rect1, rect2): 
        return ( rect1.top < rect2.bottom and 
                rect1.bottom > rect2.top and 
                rect1.left < rect2.right and 
                rect1.right > rect2.left) 

    def insert(self, sprite):
        if not self.checkcollide(self.boundary, sprite.rect):
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

    def query(self, range, found=None):
        if found is None:
            found = []
        if not self.checkcollide(self.boundary, range):
            return
        else:
            for sprite in self.sprites:
                if self.checkcollide(range, sprite.rect):
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
