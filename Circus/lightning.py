from ability import Ability
from shared import *
import math
class Lightning ( Ability ):
    def __init__( self ):
        super().__init__(name='ability_lightning')

        screen_center = vec2(WIDTH // 2, HEIGHT // 2)
        position = screen_center - pg.mouse.get_pos()
        position = position.rotate_rad(-self.player.angle)

        self.set_pos(self.player.pos - position + 155 * self.player.forward())

    def think ( self ):
        super().think()

    def run ( self ):
        self.hit_enemy()

    def hit_enemy( self ):
        # collides = self.check_collision( enemy list )

        # for collision in collides
        # if not collision in self.collided
        # code to damage whoever it collides with goes here
        # when damaged:
        # self.collided.add( damaged enemy )
        
        
        return
        
