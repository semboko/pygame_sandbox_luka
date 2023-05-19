from pygame import K_a, K_d, K_UP, K_DOWN, KEYDOWN, K_SPACE
from typing import Sequence

from pygame.event import Event
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
        
    def hadnle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.tank.fire()
            
        
    def handle_pressed_keys(self, keys: Sequence[bool]) -> None:
        if keys[K_a]:
            self.tank.move(-1)
        
        if keys[K_d]:
            self.tank.move(1)
            
        if keys[K_UP]:
            self.tank.update_gun_angle(-0.01)
        
        if keys[K_DOWN]:
            self.tank.update_gun_angle(0.01)
        
    def update(self) -> None:
        self.space.step(1/60)
        self.tank.rw.motor.rate *= 0.98
    
    def render(self, display: Surface) -> None:
        display.fill((255, 255, 255))
        self.terrain.render(display)
        self.tank.render(display)