from pymunk import Vec2d, Body, Poly, Space
from pygame import Surface, draw, image
from utils import convert



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
        
        display.blit(self.image, convert(self.body.position - self.center, h))
        draw.polygon(display, (255, 0, 150), points, 1)


class Tank:
    def __init__(self, origin: Vec2d, space: Space) -> None:
        self.origin = origin
        self.tb = TankBase(origin + Vec2d(5, -30), space)
        
    def render(self, display: Surface) -> None:
        self.tb.render(display)