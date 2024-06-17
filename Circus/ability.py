from entity import Entity
import pygame as pg
from shared import *
from datetime import datetime, timedelta

class Ability( Entity ):
    def __init__( self, name, pos=vec2(0,0)):
        """Ability class

        Args:
            name (string): name of ability to identify through shared.py
            pos (vec2): spawn position, defaults to (0,0)
        """
        super().__init__( name, pos )
        self.pos /= TILE_SIZE
        self.lifetime = self.attrs[ 'lifetime' ]
        self.cycles = 0
        self.cooldown = self.attrs[ 'cooldown' ]
        self.instance_start_time = datetime.now()

    def check_life_time( self ):
        if clientApp().anim_trigger:
            self.cycles += 1
            if self.cycles > self.lifetime:
                self.kill()

    def check_collision( self ):
        """Checks if ability collides with collision group

        Returns:
            List: collided objects
        """
        if( not self.sprite ):
            return

        hits = pg.sprite.spritecollide( self.sprite, clientApp().collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask )
        return hits

    def think( self ):
        self.run()
        self.check_life_time()

    def check_cooldown( self ):
        """Checks if cooldown has passed

        Returns:
            bool: has cooldown passed
        """
        elapsed = datetime.now() - self.instance_start_time
        if elapsed.total_seconds() > self.cooldown:
            return True
        else:
            return False

    def run( self ):
        """Function to override, updates ability, most often position
        """
        return