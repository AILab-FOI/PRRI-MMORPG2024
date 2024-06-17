from ability import Ability
from shared import *
from datetime import datetime, timedelta

class Heal ( Ability ):
    def __init__( self ):
        super().__init__(name='ability_heal')
        self.set_pos(self.player.pos)

        self.tick_time = self.instance_start_time

    def think( self ):
        super().think()
    
    def run ( self ):
        self.heal_tick()
        self.update_position()

    def update_position( self ):
        self.set_pos(self.player.pos + 50 * self.player.forward())

    def heal_tick( self ):
        elapsed = datetime.now() - self.tick_time
        if elapsed.seconds >= 0.5:
            self.player.heal(2)
            self.tick_time = datetime.now()