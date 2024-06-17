
from ability import Ability
from shared import *
class Lightning ( Ability ):
    def __init__( self ):
        super().__init__(name='ability_lightning')
        
        self.set_pos(self.player.pos)
        
