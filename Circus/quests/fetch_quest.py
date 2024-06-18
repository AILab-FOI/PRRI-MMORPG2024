from inventory import Inventory
from shared import *
import player
import quest
import entity

class FetchQuest(quest.Quest):
    def __init__( self, id, required_items=[], reward = None, owner=None, text="", title="" ):
        super().__init__( id=id, reward=reward, owner=owner, text=text, title=title )
        self.progress['items'] = {}
        self.required_items = required_items
        for item in required_items:
            self.progress['items'][item.id] = 0
    
    def check_quest_finished( self ):
        has_quest_finished = bool(True)
        # send to server?
        #return bool

        inventory: Inventory = clientApp().player.inventory

        for item in self.required_items:
            count = inventory.count_item_of_id(item.id)
            self.progress['items'][item.id] = count
            # If we're missing an item, BLEH
            if( count == 0 ):
                has_quest_finished = False
        
        distance = abs(self.owner.pos.distance_to(clientApp().player.pos))
        required_distance = 200

        # We also need to return to the npc
        if distance > required_distance:
            has_quest_finished = False

        self.update_info()
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

        ids = []
        for item in self.required_items:
            ids.append(item.id)

        inventory: Inventory = clientApp().player.inventory
        inventory.delete_items_by_id(ids)

        clientApp().player.questDialogue.set_message("Thank you greatly traveler, here you've earned your reward")
        clientApp().player.questDialogue.display()

