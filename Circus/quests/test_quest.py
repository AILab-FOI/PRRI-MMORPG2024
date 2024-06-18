from shared import *
import player
import quest
import entity

class PositionQuest(quest.Quest):
    def __init__( self, id, position, reward = None, owner=None, text="", title="" ):
        super().__init__( id=id, reward=reward, owner=owner, text=text, title=title )
        self.position : vec2 = position
        self.progress['distance'] = -1
    
    def check_quest_finished( self ):
        has_quest_finished = bool(False)
        # send to server?
        #return bool

        self.progress['distance'] = abs(self.position.distance_to(clientApp().player.pos))
        required_distance = 200
        self.update_info()

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
        if distance <= required_distance and self.owner.spoke_to == True:
            has_quest_condition = True

        return has_quest_condition
    
    def on_quest_accepted( self):
        super().on_quest_accepted()
        print("Accepted Quest!")
    
    def on_quest_finished(self):
        super().on_quest_finished()
        self.progress['distance'] = -1
        print("Quest finished!")

