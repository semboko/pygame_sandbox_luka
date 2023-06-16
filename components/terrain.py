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
        self.min_y = min_y
        self.max_y = max_y
        self.space = space
        
        self.blocks: List[TerrainBlock] = []
        
        self.noise = SimplexNoise()
        
        for x in range(0, display_width, TerrainBlock.size.x):
            block = self.get_block(x)
            self.blocks.append(block)
            
    def get_block(self, x: float) -> TerrainBlock:
        noise_value = self.noise.noise2(x/700, 0)
        y = self.min_y + (self.max_y - self.min_y) * (noise_value + 1) / 2
        return TerrainBlock(Vec2d(x, y), self.space)
            
    def update(self, shift_x: float) -> None:
        rx = self.blocks[-1].body.position.x
        lx = self.blocks[0].body.position.x
        
        if rx < shift_x + 1600:
            new_rx = shift_x + 1600
            for x in range(int(rx), int(new_rx), int(TerrainBlock.size.x)):
                block = self.get_block(x)
                self.blocks.append(block)
        
        if lx > shift_x - 190:
            new_lx = shift_x - 190
            for x in range(int(new_lx), int(lx), int(TerrainBlock.size.x)):
                block = self.get_block(x)
                self.blocks.insert(0, block)

    def render(self, display: Surface, shift_x: float) -> None:
        for block in self.blocks:
            block.render(display, shift_x)