from pygame.event import Event
from typing import Sequence
from pygame.surface import Surface


class BaseScene:
    def __init__(self) -> None:
        pass
    
    def hadnle_event(self, event: Event) -> None:
        pass
    
    def handle_pressed_keys(self, keys: Sequence[bool]) -> None:
        pass
    
    def update(self, display: Surface) -> None:
        pass
    
    def render(self, display: Surface) -> None:
        pass