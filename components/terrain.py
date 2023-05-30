import pygame
from pygame.surface import Surface
from pymunk import Space, Body, Segment, Vec2d, Poly
from random import randint
from utils import convert
from typing import List, Tuple
from noise.perlin import SimplexNoise


class TerrainBlock:
    size = Vec2d(10, 10)
    
    def __init__(self, pos: Vec2d, space: Space) -> None:
        self.body = Body(body_type=Body.STATIC)
        self.body.position = pos
        
        self.shape = Poly(self.body, vertices=(
            (-self.size.x / 2, self.size.y / 2),
            (self.size.x / 2, self.size.y / 2),
            (self.size.x / 2, -self.size.y / 2),
            (-self.size.x / 2, -self.size.y / 2),
        ))
        self.shape.density = 1
        self.shape.friction = 1
        
        self.image = Surface(self.size)
        self.image.fill((30, 30, 30))
        
        space.add(self.body, self.shape)
    
    def render(self, display: Surface, shift_x: float) -> None:
        h = display.get_height()
        pos = pygame.Vector2(*convert(self.body.position, h))
        pos.x -= shift_x
        dest = self.image.get_rect(center=pos)
        display.blit(self.image, dest)


class Terrain:
    def __init__(self, display_width: int, min_y: int, max_y: int, step: int, space: Space) -> None:
        self.blocks: List[TerrainBlock] = []
        
        self.noise = SimplexNoise()
        
        for x in range(0, display_width, TerrainBlock.size.x):
            noise_value = self.noise.noise2(x/700, 0)
            y = min_y + (max_y - min_y) * abs(noise_value)
            block = TerrainBlock(Vec2d(x, y), space)
            self.blocks.append(block)
            
    def update(self, shift_x: float) -> None:
        pass
    
    def render(self, display: Surface, shift_x: float) -> None:
        for block in self.blocks:
            block.render(display, shift_x)