from scenes.abstract import BaseScene
from pymunk import Space
from components.catapult import Catapult
from components.floor import Floor
from pygame.surface import Surface
from pygame.event import Event
import pygame
from typing import Sequence


class CatapultScene(BaseScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = (0, -1000)
        self.catapult = Catapult(250, 155, 75, self.space)
        self.floor = Floor(self.space)
        
        self.bullets = []
        
    def update(self) -> None:
        self.space.step(1/60)
        self.catapult.update_motor_rate()
        ammo = self.catapult.detach_ammo()
        if ammo:
            self.bullets.append(ammo)
        
    def hadnle_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.catapult.reload()
                
            if event.key == pygame.K_SPACE:
                self.catapult.shot()
                
    def handle_pressed_keys(self, keys: Sequence[bool]) -> None:
        if keys[pygame.K_LEFT]:
            self.catapult.move_arm()
    
        if keys[pygame.K_a]:
            self.catapult.move(-1)
        
        if keys[pygame.K_d]:
            self.catapult.move(1)

    def render(self, display: Surface) -> None:
        display.fill((255, 255, 255))
        self.catapult.render(display)
        self.floor.render(display)
        for b in self.bullets:
            b.render(display)