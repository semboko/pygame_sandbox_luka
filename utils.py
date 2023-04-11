from typing import Tuple
from pygame.surface import Surface
import pymunk
import pygame


def convert(coord: Tuple[int, int], height: int) -> Tuple[int, int]:
    return int(coord[0]), int(height - coord[1])


def draw_joint(display: Surface, joint: pymunk.PinJoint) -> None:
    a, b = joint.anchor_a, joint.anchor_b
    world_a = joint.a.local_to_world(a)
    world_b = joint.b.local_to_world(b)
    h = display.get_height()
    pygame.draw.line(
        display,
        (255, 255, 0),
        convert(world_a, h),
        convert(world_b, h),
        5,
    )
