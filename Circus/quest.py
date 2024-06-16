from shared import *
import player

class Quest ( object ):
    """Quest base class

    """    
    def __init__( self ):
        super().__init__( )
        self.id = None
        self.title = ""
        self.text = ""
        self.accepted = False
        self.finished = False

    def is_accepted(self):
        return self.accepted
    
    def is_finished(self):
        return self.finished

    def is_in_progress(self):
        return self.accepted and not self.finished

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
        self.accepted = True

    def finish_quest( self ):
        self.finished = True










