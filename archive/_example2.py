import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List
from random import randint

pygame.init()
display = pygame.display.set_mode((500, 500))
h = display.get_height()
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, -1000)


class Ball:
    def __init__(self, coord: Tuple[int, int], r: int, s: pymunk.Space) -> None:
        self.body = pymunk.Body()
        self.body.position = coord
        self.body.velocity_func = self.limit_velocity

        self.radius = r
        self.shape = pymunk.Circle(self.body, r)
        self.shape.density = 1
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


class Floor:
    def __init__(self) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (0, 20), (h, 40), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def render(self, display: Surface) -> None:
        pygame.draw.line(
            display,
            (255, 0, 0),
            convert(self.shape.a, h),
            convert(self.shape.b, h),
            5,
        )


def convert(coord: Tuple[int, int], height: int) -> Tuple[int, int]:
    return int(coord[0]), int(height - coord[1])


def clean_up(balls: List[Ball]) -> List[Ball]:
    new_balls = []
    for b in balls:
        if b.body.position.y >= 0:
            new_balls.append(b)
            continue
        space.remove(b.body, b.shape)
        print("Ball is removed")
    return new_balls


def clean_dead(balls: List[Ball]) -> List[Ball]:
    new_balls = []
    for b in balls:
        b.lifetime -= 1
        if b.lifetime >= 0:
            new_balls.append(b)
            continue
        space.remove(b.body, b.shape)
    return new_balls


balls = []
floor = Floor()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            b = Ball(convert(event.pos, h), 3, space)
            b.body.apply_force_at_local_point((randint(0, 5000), 500000), (0, 0))
            balls.append(b)

    # b = Ball((250, 450), 3, space)
    # b.body.apply_force_at_local_point((randint(0, 5000), 500000), (0, 0))
    # balls.append(b)

    balls = clean_up(balls)
    balls = clean_dead(balls)
    display.fill((255, 255, 255))

    for ball in balls:
        ball.render(display)
        # print(ball.body.velocity)

    floor.render(display)
    pygame.display.update()
    space.step(1/60)
    clock.tick(60)
