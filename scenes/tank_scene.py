from pygame import K_a, K_d, K_UP, K_DOWN, KEYDOWN, K_SPACE, Vector2
from typing import Sequence, List

from pygame.event import Event
from scenes.abstract import BaseScene
from pymunk import Space, Vec2d
from components.floor import Floor
from components.tank import Tank, Ammo
from components.terrain import Terrain, TerrainBlock
from pygame.surface import Surface
from utils import convert
from components.animation import Animation




class TankScene(BaseScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = (0, -1000)
        
        
        self.terrain = Terrain(1500, 5, 100, 300, self.space)
        self.tank = Tank(Vec2d(100, 190), self.space)
        self.init_pos = self.tank.tb.body.position
        
        self.explosion = Animation("./assets/Tile.png", 64, Vector2(256, 256))
        
        self.bullets: List[Ammo] = []
        
    def hadnle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not self.explosion.running:
                ammo = self.tank.fire()
                exp_pos = convert(ammo.body.position, 750)
                self.explosion.start(Vector2(exp_pos) + Vector2(0, -150))
                self.bullets.append(ammo)
            
        
    def handle_pressed_keys(self, keys: Sequence[bool]) -> None:
        if keys[K_a]:
            self.tank.move(-1)
        
        if keys[K_d]:
            self.tank.move(1)
            
        if keys[K_UP]:
            self.tank.update_gun_angle(-0.01)
        
        if keys[K_DOWN]:
            self.tank.update_gun_angle(0.01)
    
    def get_camera_shift(self, display: Surface) -> Vec2d:
        h = display.get_height()
        return (self.init_pos - convert(self.tank.tb.body.position, h)) * -1
        
    def update(self, display: Surface) -> None:
        self.space.step(1/60)
        self.tank.rw.motor.rate *= 0.98
        camera_shift = self.get_camera_shift(display)
        self.terrain.update(camera_shift.x)
        self.explosion.update()
    
    def render(self, display: Surface) -> None:
        display.fill((255, 255, 255))
        h = display.get_height()
        camera_shift = self.get_camera_shift(display)
        self.terrain.render(display, camera_shift.x)
        self.tank.render(display, camera_shift.x)
        for bullet in self.bullets:
            bullet.render2(display, camera_shift.x)
        self.explosion.render(display, camera_shift.x)