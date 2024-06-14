from shared import *
import player
import quest
import entity

class TestQuest (quest.Quest):
    def __init__(self, quest_giver : entity.Entity):
        super().__init__()
        self.title = "The Testiest Quest"
        self.id = 0
        self.text = "This is the testiest quest."
        self.entity : entity.Entity = quest_giver
    
    def check_quest_finished( self ):
        has_quest_finished = bool(False)
        # send to server?
        #return bool
        if self.entity.pos.distance_to(clientApp().player.pos) <= 100:
            has_quest_finished = True
        return has_quest_finished
    
    def check_quest_conditions( self ):
        has_quest_condition = bool(False)
        # lista boolova?
        has_quest_condition = True
        return has_quest_condition
    
    def accept_quest( self, player : player.Player):
        return
