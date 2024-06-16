from shared import *
import player
import quest
import entity

class PositionQuest(quest.Quest):
    def __init__( self, id, position ):
        self.id = id
        super().__init__()
        self.title = "The Testiest Quest"
        self.text = "This is the testiest quest."
        self.position : vec2 = position
        self.progress['distance'] = -1
    
    def check_quest_finished( self ):
        has_quest_finished = bool(False)
        # send to server?
        #return bool

        self.progress['distance'] = abs(self.position.distance_to(clientApp().player.pos))
        required_distance = 200
        self.update_info()

        print(self.progress['distance'])

        # Got to pos, finished!
        if self.progress['distance'] <= required_distance:
            has_quest_finished = True
        return has_quest_finished
    
    def check_quest_conditions( self ):
        has_quest_condition = bool(False)

        if( self.owner == None ):
            return has_quest_condition
        
        distance = abs(self.owner.pos.distance_to(clientApp().player.pos))
        required_distance = 200

        # Close to NPC, accept
        if distance <= required_distance:
            has_quest_condition = True

        return has_quest_condition
    
    def accept_quest( self, player : player.Player):
        super().accept_quest(player)
        print("Accepted Quest!")
    
    def finish_quest(self):
        super().finish_quest()
        self.progress['distance'] = -1
        print("Quest finished!")

