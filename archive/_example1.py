import pygame
from typing import Tuple

from math import atan, cos, sin, sqrt, radians, degrees, asin, acos, atan2
from pygame.math import Vector2

pygame.init()

display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

white = pygame.color.Color("white")
red = pygame.color.Color("red")

Coord = Tuple[int, int]

class Triangle:
    def __init__(self, a: Coord, b: Coord, c: Coord) -> None:
        self.coords = (a, b, c)
        xs, ys = [x for x, _ in self.coords], [y for _, y in self.coords]
        self.xO, self.yO = sum(xs)/3, sum(ys)/3
    
    def rotate(self, alpha: float) -> None:
        shift = Vector2(self.xO, self.yO)
        new_coords = []
        for xV, yV in self.coords:
            v = Vector2(xV, yV) - shift
            newX, newY = v.rotate_rad(radians(alpha)) + shift
            new_coords.append((newX, newY))
            
        self.coords = (*new_coords, )
        
    
    def render(self, display: pygame.Surface) -> None:
        pygame.draw.polygon(display, (255, 0, 0), (*self.coords, ), width=2)
        pygame.draw.circle(display, (255, 0, 0), (self.xO, self.yO), 5, 1)


t = Triangle((300, 100), (250, 400), (100, 300))

def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            t.rotate(-1)
        if keys[pygame.K_RIGHT]:
            t.rotate(1)
        
        # Render state
        display.fill(white)
        t.render(display)
        pygame.display.update()
        clock.tick(60)

mainloop()
pygame.quit()