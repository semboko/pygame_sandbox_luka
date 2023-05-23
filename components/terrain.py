import pygame
from pygame.surface import Surface
from pymunk import Space, Body, Segment, Vec2d
from random import randint
from utils import convert
from typing import List, Tuple

class Terrain:
    def __init__(self, display_width: int, min_y: int, max_y: int, step: int, space: Space) -> None:
        
        self.segments: List[Tuple[Body, Segment]] = []
        
        for xa in range(0, display_width, step):
            if not self.segments:
                ya = randint(min_y, max_y)
            else:
                last_body, last_segment = self.segments[-1]
                local_b = last_segment.b
                world_b = last_body.local_to_world(local_b)
                ya = world_b.y
                
            xb = xa + step
            yb = randint(min_y, max_y)
            
            body = Body(body_type=Body.STATIC)
            body.position = Vec2d(xa, ya)
            
            shape = Segment(body, Vec2d(0, 0), Vec2d(xb, yb) - Vec2d(xa, ya), 5)
            shape.density = 1
            shape.friction = 1
            space.add(body, shape)
            self.segments.append((body, shape))
    
    def render(self, display: Surface) -> None:
        h = display.get_height()
        for body, shape in self.segments:
            start_pos = convert(body.local_to_world(shape.a), h)
            end_pos = convert(body.local_to_world(shape.b), h)
            pygame.draw.line(display, (255, 0, 0), start_pos, end_pos, 5)