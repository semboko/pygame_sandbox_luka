import pygame
import pymunk
from components.floor import Floor
from components.catapult import Catapult

pygame.init()
display = pygame.display.set_mode((500, 500))
h = display.get_height()
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, -1000)

floor = Floor(space)
catapult = Catapult(250, 300, 75, space)
bullets = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                catapult.reload()
            
            if event.key == pygame.K_SPACE:
                catapult.shot()
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        catapult.move_arm()
    
    if pressed_keys[pygame.K_a]:
        catapult.move(-1)
    
    if pressed_keys[pygame.K_d]:
        catapult.move(1)
        
    ammo = catapult.detach_ammo()
    if ammo:
        bullets.append(ammo)

    catapult.update_motor_rate()
    
    display.fill((255, 255, 255))

    floor.render(display)
    catapult.render(display)
    for b in bullets:
        b.render(display)
    
    pygame.display.update()
    space.step(1/60)
    clock.tick(60)
