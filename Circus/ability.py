from entity import *
import pygame as pg
from datetime import datetime, timedelta

class Ability( Entity ):
    def __init__( self, name, pos=(0,0)):
        """Ability class

        Args:
            name (string): name of ability to identify through shared.py
            pos (vec2): spawn position, defaults to (0,0)
        """
        super().__init__( name, pos )
        self.pos /= TILE_SIZE
        self.lifetime = self.attrs[ 'lifetime' ]
        self.cycles = 0
        self.instance_start_time = datetime.now()

        self.always_update = True

    def should_think(self) -> bool:
        return True    

    def check_life_time( self ):
        if clientApp().anim_trigger:
            self.cycles += 1
            if self.cycles > self.lifetime:
                self.kill()

    def check_collision( self, hitList ):
        """Checks if ability collides with collision group
        
        Args:
            hitList (list): list of enemies to check through

        Returns:
            List: collided objects
        """
        if( not self.sprite ):
            return

        hits = pg.sprite.spritecollide( self.sprite, hitList,
                                      dokill=False, collided=pg.sprite.collide_mask )
        return hits

    def think( self ):
        clientApp().collision_group.remove( self )
        self.run()
        self.check_life_time()

    def run( self ):
        """Function to override, updates ability, most often position
        """
        return