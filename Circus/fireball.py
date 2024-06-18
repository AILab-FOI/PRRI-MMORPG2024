import math
from ability import Ability
from shared import *
class Fireball ( Ability ):
    def __init__( self ):
        super().__init__(name='ability_fireball')

        screen_center = vec2(WIDTH // 2, HEIGHT // 2)
        position = screen_center - pg.mouse.get_pos()
        self.angle = math.atan2(position.y, position.x)
        
        self.direction = (-self.player.right()).rotate_rad(self.angle)
        self.direction.normalize()
        self.direction *= 4

        self.set_pos(self.player.pos + 50 * self.player.forward())
        self.set_ang(math.degrees(-self.angle) - 90)

    def think ( self ):
        super().think()

    def run ( self ):
        self.update_position()
        self.update_rotation()
        self.hit_enemy()

    def update_position( self ):
        newpos = self.pos + self.direction
        self.set_pos(newpos)

    def update_rotation( self ):
        angle = math.atan2(self.direction.y, self.direction.x)
        self.set_ang(math.degrees(-angle - self.player.angle) )

    def hit_enemy( self ):
        # collides = self.check_collision( enemy list )

        # for collision in collides
        # if not collision in self.collided
        # code to damage whoever it collides with goes here
        # when damaged:
        # self.collided.add( damaged enemy )
        
        
        return
        