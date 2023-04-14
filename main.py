import pygame
import pymunk
from typing import Type
from scenes.abstract import BaseScene
from scenes.catapult_scene import CatapultScene


space = pymunk.Space()
space.gravity = (0, -1000)

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.scene = None
    
    def load_scene(self, Scene: Type[BaseScene]):
        self.scene = Scene()
    
    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.scene.hadnle_event(event)
            
            pk = pygame.key.get_pressed()
            self.scene.handle_pressed_keys(pk)
            
            self.scene.update()
            
            self.scene.render(self.display)
            
            pygame.display.update()
            self.clock.tick(60)
    

g = Game()
g.load_scene(CatapultScene)  # !!! Change to the concrete scene
g.run()