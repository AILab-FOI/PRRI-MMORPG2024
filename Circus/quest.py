from shared import *
import player
from shared import _globals

class Quest ( object ):
    """Quest base class

    """    
    def __init__( self, owner = None ):
        super().__init__( )
        if( not hasattr(self, 'id') ):
            self.id = None
        
        self.title = ""
        self.text = ""
        self.accepted = False
        self.finished = False
        self.progress = {}
        # Who handles the quest, not which player does it!!
        self.owner = owner

        if( clientApp() != None ):
            clientApp().add_quest( self.id, self )
        else:
            _globals.tmp_quest_list[self.id] = self

    def is_accepted(self):
        return self.accepted
    
    def is_finished(self):
        return self.finished

    def is_in_progress(self):
        return self.accepted and not self.finished
    
    def set_owner(self, owner):
        self.owner = owner

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
        self.update_info()

    def finish_quest( self ):
        self.finished = True
        self.update_info()

    def update_info(self):
        message = {"command": "update_quest_info"}
        message['quest'] = self.id
        message['player'] = clientApp().username
        message['accepted'] = self.accepted
        message['finished'] = self.finished
        message['progress'] = self.progress

        clientApp().push_websocket_message(message)








