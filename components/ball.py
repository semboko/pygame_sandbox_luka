import pygame
from pygame.surface import Surface
import pymunk
from utils import convert
from typing import Tuple
from math import sin, cos, radians


class Ball:
    def __init__(self, coord: Tuple[int, int], r: int, s: pymunk.Space) -> None:
        self.body = pymunk.Body()
        self.body.position = coord
        # self.body.velocity_func = self.limit_velocity

        self.radius = r
        self.shape = pymunk.Circle(self.body, r)
        self.shape.density = 1
        self.shape.friction = 1
        self.shape.elasticity = .5
        self.lifetime = 255
        s.add(self.body, self.shape)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 500
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale

    def render(self, display: Surface) -> None:
        h = display.get_height()
        pygame.draw.circle(display, (255, 0, 0), convert(self.body.position, h), self.radius)

        alpha = radians(self.body.angle)
        start_pos = convert(self.body.position, h)
        end_pos = convert(
            self.body.local_to_world(
                (
                    self.radius * sin(alpha), 
                    self.radius * cos(alpha),
                )
            ), 
            h
        )
        
        pygame.draw.line(display, (0, 0, 0), start_pos, end_pos, 1)