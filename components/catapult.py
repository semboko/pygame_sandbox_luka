from pygame import Surface
from pymunk import Space, Poly, Body, PivotJoint, ShapeFilter, PinJoint, RotaryLimitJoint, SimpleMotor
import pygame
from utils import convert, draw_joint
from components.ball import Ball
from components.rect import Rect
from typing import Tuple, Optional
from math import radians, degrees


class Catapult:
    
    ammo: Optional[Ball] = None
    ammo_joint: Optional[PinJoint] = None
    
    def __init__(self, x: int, y: int, r: int, space: Space):
        self.space = space
        self.is_making_shot = False
        self.collision_group = ShapeFilter(group=8)
        self.frame_body = Body()
        self.frame_body.position = x, y
        self.frame_shape = Poly(self.frame_body, (
            (0, r),
            (-r, -r),
            (r, -r),
        ))
        self.frame_shape.density = 1
        self.frame_shape.filter = self.collision_group
        space.add(self.frame_body, self.frame_shape)
        
        self.front_wheel = self.get_wheel((x + r, y - r), space)
        self.rear_wheel = self.get_wheel((x - r, y - r), space)
        
        arm_length = 200
        self.arm = self.get_arm((x, y + r), space, arm_length)
        self.counterweight, self.cw_joint = self.get_counterweight(
            (x + arm_length/4, y + 0.5 * r), 
            (x + arm_length/4, y + r), 
            space,
        )
        
        hook_coord = (x - arm_length * 3/4, y + r)
        self.hook = Ball(hook_coord, 2, space)
        self.hook.shape.filter = self.collision_group
        space.add(PivotJoint(
            self.arm.body,
            self.hook.body,
            self.arm.body.world_to_local(hook_coord),
            self.hook.body.world_to_local(hook_coord)
        ))
        
        self.arm_limit = RotaryLimitJoint(
            self.arm.body,
            self.frame_body,
            0, 
            radians(225)
        )
        space.add(self.arm_limit)
        
        self.motor = SimpleMotor(self.rear_wheel.body, self.frame_body, 0)
        space.add(self.motor)
    
    def get_wheel(self, coords: Tuple[int, int], space: Space) -> Ball:
        wheel = Ball(coords, 20, space)
        wheel.shape.filter = self.collision_group
        space.add(
            PivotJoint(
                self.frame_body, 
                wheel.body, 
                self.frame_body.world_to_local(coords), 
                (0, 0)
            )
        )
        return wheel

    def get_arm(self, attachment: Tuple[int, int], space: Space, arm_length: int = 200) -> Rect:
        arm = Rect(attachment[0] - arm_length/4, attachment[1], arm_length, 5, space)
        arm.shape.filter = self.collision_group
        space.add(PivotJoint(
            self.frame_body,
            arm.body,
            self.frame_body.world_to_local(attachment),
            arm.body.world_to_local(attachment),
        ))
        return arm

    def reload(self):
        self.is_making_shot = False
        ammo_coord = (self.hook.body.position.x, self.hook.body.position.y - 20)
        self.ammo = Ball(ammo_coord, 10, self.space)
        self.ammo.shape.filter = self.collision_group
        self.ammo_joint = PinJoint(self.hook.body, self.ammo.body, (0, 0), (0, 0))
        self.space.add(self.ammo_joint)
    
    def shot(self):
        if not self.ammo:
            return
        self.is_making_shot = True
        self.arm_limit.min = 0
        self.arm_limit.max = radians(360)
    
    def move_arm(self):
        self.is_making_shot = False
        if degrees(self.arm_limit.max) < -55:
            return
        self.arm_limit.min = self.arm_limit.min - 0.05
        self.arm_limit.max = self.arm_limit.max - 0.05

    def ready_to_detach_ammo(self):
        return degrees(self.arm.body.angle - self.frame_body.angle) > 55 and self.is_making_shot

    def detach_ammo(self):
        if not self.ammo_joint:
            return
        if degrees(self.arm.body.angle - self.frame_body.angle) > -80:
            return
        self.space.remove(self.ammo_joint)
        self.ammo_joint = None
        
        ammo = self.ammo
        self.ammo = None
        return ammo

    def move(self, direction: int):
        self.motor.rate += direction * -1 * 0.3
    
    def update_motor_rate(self):
        self.motor.rate *= .9

    def get_counterweight(self, coord: Tuple[int, int], attachment: Tuple[int, int], space: Space) -> Tuple[Ball, PinJoint]:
        cw = Ball(coord, 20, space)
        cw.body.mass = 30000
        cw.shape.filter = self.collision_group
        
        cw_joint = PinJoint(
            self.arm.body,
            cw.body,
            self.arm.body.world_to_local(attachment),
            cw.body.world_to_local(coord)
        )
        space.add(cw_joint)
        return cw, cw_joint

    def render(self, display: Surface):
        h = display.get_height()
        points = [
            convert(
                self.frame_body.local_to_world(p), 
                h,
            ) 
            for p in self.frame_shape.get_vertices()
        ]
        pygame.draw.polygon(display, (0, 0, 0), points, 5)
        
        self.front_wheel.render(display)
        self.rear_wheel.render(display)

        self.arm.render(display)
        self.counterweight.render(display)
        draw_joint(display, self.cw_joint)
        self.hook.render(display)
        
        if self.ammo and self.ammo_joint:
            self.ammo.render(display)
            draw_joint(display, self.ammo_joint)