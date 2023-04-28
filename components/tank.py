from pymunk import Vec2d, Body, Poly, Space, PivotJoint, ShapeFilter, SimpleMotor
from pygame import Surface, draw, image, transform
from components.ball import Ball
from utils import convert
from typing import List, Tuple
from math import degrees



class TankBase:
    def __init__(self, origin: Vec2d, space: Space) -> None:
        self.origin = origin
        
        self.body = Body()
        self.center = Vec2d(104, -22)
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
            convert(Vec2d(*p) - self.center, 44)
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
        dest = rotated_img.get_rect(center=convert(self.body.position, h))
        display.blit(rotated_img, dest)
        draw.polygon(display, (255, 0, 150), points, 1)


class Wheel(Ball):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.image = image.load("./assets/wheel.png", "png")
        
    def render(self, display: Surface) -> None:
        h = display.get_height()
        rotated_img = transform.rotate(self.image, degrees(self.body.angle))
        display.blit(
            rotated_img, 
            convert(self.body.position - Vec2d(self.radius, -self.radius), h)
        )
        

class RearWheel(Wheel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        tb: TankBase = kwargs["tb"]
        space: Space = self.body.space
        
        self.image = image.load("./assets/rear_wheel.png")
        self.motor = SimpleMotor(self.body, tb.body, 1)
        space.add(self.motor)


class Tank:
    def __init__(self, origin: Vec2d, space: Space) -> None:
        self.origin = origin
        self.cf = ShapeFilter(group=1)
        
        self.tb = TankBase(origin + Vec2d(0, -30), space)
        self.tb.shape.filter = self.cf
        
        self.wheels = self.create_wheels(space)
        
        self.rw = self.create_rear_wheel(space)
        
    
    def create_rear_wheel(self, space: Space) -> RearWheel:
        r = 9
        coord = self.origin + Vec2d(14, -42) + Vec2d(r, -r)
        wheel = RearWheel(coord, r, space, tb=self.tb)
        wheel.shape.filter = self.cf
        
        return wheel

    def create_wheels(self, space: Space) -> List[Wheel]:
        r = 9
        
        wheel_coords = [
            Vec2d(38, -54),
            Vec2d(57, -54),
            Vec2d(76, -54),
            Vec2d(96, -54),
            Vec2d(116, -54),
            Vec2d(136, -54),
            Vec2d(160, -54),
            Vec2d(184, -42),
        ]
        
        result = []
        
        for coord in wheel_coords:
            wheel = Wheel(self.origin + coord + Vec2d(r, -r), r, space)
            wheel.shape.filter = self.cf
            tb_local = self.tb.body.world_to_local(wheel.body.position)
            space.add(PivotJoint(wheel.body, self.tb.body, (0, 0), tb_local))
            result.append(wheel)
        
        return result
        
    def render(self, display: Surface) -> None:
        for wheel in self.wheels:
            wheel.render(display)
        self.rw.render(display)
        self.tb.render(display)