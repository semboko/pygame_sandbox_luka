from scenes.abstract import BaseScene
from pymunk import Space, Vec2d
from components.floor import Floor
from components.tank import Tank
from pygame.surface import Surface



class TankScene(BaseScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = (0, -1000)
        
        self.terrain = Floor(self.space)
        self.tank = Tank(Vec2d(100, 190), self.space)
        
    def update(self) -> None:
        self.space.step(1/60)
    
    def render(self, display: Surface) -> None:
        display.fill((255, 255, 255))
        self.terrain.render(display)
        self.tank.render(display)