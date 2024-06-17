
from ability import Ability
from shared import *
import math

class Slash ( Ability ):
    def __init__( self ):
        super().__init__(name='ability_slash')


        # positioning slash
        screen_center = vec2(WIDTH // 2, HEIGHT // 2)
        position = screen_center - pg.mouse.get_pos()

        self.angle = math.atan2(position.y, position.x)

        # WHY THE FUCK JE LIJEVI VECTOR ZA NAPRIJED ????????????
        self.direction = (-self.player.right()).rotate_rad(self.angle)
        self.direction.normalize()
        self.direction *= 100
        self.update_position

        self.collided = []

    def think ( self ):
        super().think()

    def run ( self ):
        self.update_position()
        self.update_rotation()
    
    def update_position( self ):
        newpos = self.player.pos + self.direction
        self.set_pos(newpos)
    
    def update_rotation( self ):
        return #doesnt work
        if self.is_drawing:
            self.sprite.image = pg.transform.rotate(self.sprite.image, angle)

        
    def hit_enemy( self ):
        # collides = self.check_collision( enemy list )

        # for collision in collides
        # if not collision in self.collided
        # code to damage whoever it collides with goes here
        # when damaged:
        # self.collided.add( damaged enemy )
        
        
        return