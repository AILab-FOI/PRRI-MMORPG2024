from shared import *
import player


class Quest ( object ):
    """Quest base class

    """    
    def __init__( self ):
        super().__init__( )
        self.id = -1
        self.title = ""
        self.text = ""

    def check_quest_finished( self ):
        has_quest_finished = bool(False)
        # has the player been to x tile

        return has_quest_finished
    
    def check_quest_conditions( self ):
        has_quest_condition = bool(False)
        # lista boolova?
        # return bool
        return has_quest_condition
    
    def accept_quest( self, player : player.Player):
        return












