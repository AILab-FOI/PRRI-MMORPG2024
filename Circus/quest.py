from shared import *
import math
from entity import BaseSpriteEntity
from bullet import Bullet
from itertools import cycle
import json
import player

from viewpoint import Viewpoint


class Quest ( object ):
    """Quest base class

    """    
    def __init__( self ):
        super().__init__( )
        self.id = -1
        self.title = ""

    def check_quest_finished( self ):
        has_quest_finished = bool(False)
        # send to server?
        #return bool
        return has_quest_finished
    
    def check_quest_conditions( self ):
        has_quest_condition = bool(False)
        # lista boolova?
        # return bool
        return has_quest_condition
    
    def accept_quest( self, player : player.Player):
        return












