from pymunk import Vec2d, Body, Poly, Space, PivotJoint, ShapeFilter
from pygame import Surface, draw, image, transform
from components.ball import Ball
from utils import convert
from typing import List
from math import degrees



class TankBase:
    def __init__(self, origin: Vec2d, space: Space) -> None:
        self.origin = origin
        
        self.body = Body()
        self.center = Vec2d(85, -15)
        self.body.position = origin + self.center
        
        points = (
            (0, 0),
            (48, 0),
            (73, 6),
            (204, 10),
            (200, 28),
            (172, 34),
            (38, 33),
            (10, 20),
            (0, 20)
        )
        
        self.shape = Poly(self.body, [
            convert(Vec2d(*p) - self.center, 32)
            for p in points
        ])
        self.shape.density = 1
        space.add(self.body, self.shape)
        
        self.image = image.load("./assets/tank_base.png", "png")
        
    
    def render(self, display: Surface) -> None:
        h = display.get_height()
        
        points = [
            convert(self.body.local_to_world(v), h)
            for v in self.shape.get_vertices()
        ]
        
        rotated_img = transform.rotate(self.image, degrees(self.body.angle))
        display.blit(rotated_img, convert(self.body.position - self.center, h))
        draw.polygon(display, (255, 0, 150), points, 1)


class Wheel(Ball):
    pass


class Tank:
    def __init__(self, origin: Vec2d, space: Space) -> None:
        self.origin = origin
        self.cf = ShapeFilter(group=1)
        
        self.tb = TankBase(origin + Vec2d(0, -30), space)
        self.tb.shape.filter = self.cf
        
        self.wheels = self.create_wheels(space)

    def create_wheels(self, space: Space) -> List[Wheel]:
        r = 9
        
        wheel = Wheel(self.origin + Vec2d(38, -56) + Vec2d(r, -r), r, space)
        wheel.shape.filter = self.cf
        tb_local = self.tb.body.world_to_local(wheel.body.position)
        space.add(PivotJoint(wheel.body, self.tb.body, (0, 0), tb_local))
        
        return [wheel, ]
        
    def render(self, display: Surface) -> None:
        for wheel in self.wheels:
            wheel.render(display)
        self.tb.render(display)