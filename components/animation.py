from pygame.image import load
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from typing import Optional


class Animation:
    def __init__(self, filename: str, frames: int, frame_size: Vector2) -> None:
        self.tiles = load(filename)
        self.frames = frames
        self.frame_size = frame_size
        self.running: bool = False
        self.active_frame = 0
        self.pos: Optional[Vector2] = None
        
    def get_coords(self, frame_n: int) -> Vector2:
        cols_n = self.tiles.get_width() // self.frame_size.x
        rows_n = self.tiles.get_height() // self.frame_size.y
        
        x = (frame_n % cols_n) * self.frame_size.x
        y = (frame_n // rows_n) * self.frame_size.y
        
        return Vector2(x, y)
    
    def start(self, pos: Vector2) -> None:
        self.running = True
        self.active_frame = 0
        self.pos = pos
    
    def update(self):
        if self.active_frame == self.frames - 1:
            self.running = False
            self.active_frame = 0
            self.pos = None
            return
        
        self.active_frame += 1
    
    def render(self, display: Surface, shift_x: int):
        if not self.running or self.pos is None:
            return
        coords = self.get_coords(self.active_frame)
        rect = Rect(coords, self.frame_size)
        tile = self.tiles.subsurface(rect)
        display.blit(tile, self.pos - Vector2(shift_x, 0))
        

class ExplosionAnimation(Animation):
    pass