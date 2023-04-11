import pygame
from pygame.surface import Surface
import pymunk
from utils import convert


class Floor:
    def __init__(self, space: pymunk.Space) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (0, 60), (500, 60), 5)
        self.shape.elasticity = 1
        self.shape.friction = 1
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        h = display.get_height()
        pygame.draw.line(
            display,
            (255, 0, 0),
            convert(self.shape.a, h),
            convert(self.shape.b, h),
            5,
        )
