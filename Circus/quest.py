from shared import *
import player
from shared import _globals
from inventory_item import InventoryItem

class Reward( object ):
    def __init__(self) -> None:
        pass

    def give_reward(self):
        pass

    def reward_string(self) -> str:
        return "Nothing"

class ItemReward( Reward ):
    def __init__(self, *items) -> None:
        super().__init__()

        self.items = []
        for item in items:
            self.items.append(item)
        
    def give_reward(self):
        clientApp().player.inventory.add_items([
            InventoryItem( id=1, name="Apple",description="+40% Doctor resistance", type="Armor", stat=40 ),
            InventoryItem( id=2, name="Gold",description="Common Currency", type="Currency", stat=1 ),
        ])
    
    def reward_string(self) -> str:
        return str(self.items)

class Quest ( object ):
    """Quest base class

    """    
    def __init__( self, id = None, owner = None, reward=None, text="", title="" ):
        super().__init__( )
        self.id = id
        self.title = title
        self.text = text
        self.accepted = False
        self.finished = False
        self.progress = {}
        # Who handles the quest, not which player does it!!
        self.owner = owner
        self.reward : Reward = reward

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

        self.on_quest_accepted()

        self.update_info()

    def finish_quest( self ):
        self.finished = True

        self.on_quest_finished()
        if( self.reward ):
            self.reward.give_reward()

        self.update_info()
    
    # Called before info is sent to server
    def on_quest_accepted( self ):
        pass

    # Called before info is sent to server
    def on_quest_finished( self ):
        pass

    def update_info(self):
        message = {"command": "update_quest_info"}
        message['quest'] = self.id
        message['player'] = clientApp().username
        message['accepted'] = self.accepted
        message['finished'] = self.finished
        message['progress'] = self.progress

        clientApp().push_websocket_message(message, False)








