from inventory_item import InventoryItem
from shared import *
import entity
from quest import Quest, ItemReward
from quests.fetch_quest import FetchQuest
from quests.test_quest import PositionQuest
from typing import List

NPCS = {
    'test_npc': {
        'name': 'Guggy',
        'entity': 'empty',
        'dialog': 'Hey, could you fetch some apples for me?\nAn apple tree is to the east of here!',
        'quests': [
            FetchQuest(
                id="QUEST_FETCH_APPLE", 
                required_items=[
                    InventoryItem( id=2, name="Apple",description="+40% Doctor resistance", type="Armor", stat=40 )
                ],
                reward=ItemReward(
                    InventoryItem( id=1, name="Gold",description="Feels oddly chocholatey", type="Currency", stat=1 ),
                ),
                title = "The Testiest Quest",
                text = "Move to the lower right tree." ),
            PositionQuest(
                id="QUEST_APPLE_GAIN",
                position=vec2( 13.90625 * TILE_SIZE, 14.125 * TILE_SIZE ),
                reward=ItemReward(
                    InventoryItem( id=2, name="Apple",description="+40% Doctor resistance", type="Armor", stat=40 ),
                )
                )
                ],
    },
}

class NPCBase( entity.Entity ):
    def __init__( self, name, pos = vec2(0), template=None ):
        super().__init__( name, pos )

        self.npc_name = name
        self.quests : List[Quest] = []
        self.spoke_to = False
        self.dialog = ''

        if( template != None ):
            self.load_npc_template(template)

    def load_npc_template(self, name):
        template = NPCS[name]
        # Load default entity stuff
        self.load_attrs_from_name(template['entity'])

        self.npc_name = template['name']

        self.dialog = template['dialog']

        self.quests : List[Quest] = []

        quests = template['quests']

        if( quests == None ):
            return
        
        if( isinstance(quests, list) ):
            for quest in quests:
                self.add_quest(quest)
        else:
            self.add_quest(quests)

    def load_attribute(self, name, value):
        match name:
            case "template":
                self.load_npc_template(value)
            case _:
                super().load_attribute(name, value)

    def add_quest( self, quest ):
        quest.set_owner(self)
        self.quests.append(quest)

    def should_think(self) -> bool:
        return True
    
    def speak(self):
        if( self.spoke_to ):
            return
        
        # Cant speak if we already did their stuff
        for quest in self.quests:
            if( quest.is_in_progress() or quest.is_finished() ):
                return
        
        message = f"{self.npc_name}\n{self.dialog}"

        clientApp().player.questDialogue.set_message(message)
        clientApp().player.questDialogue.display()
        clientApp().player.questDialogue.listener = self

    def end_speak(self):
        self.spoke_to = True

    def think(self):
        if( abs( self.pos.distance_to(clientApp().player.pos) ) < 200 ):
            self.speak()

        for quest in self.quests:
            if( quest.is_in_progress() ):
                if( quest.check_quest_finished() ):
                    quest.finish_quest()
            elif( not quest.is_finished() ):
                if( quest.check_quest_conditions() ):
                    quest.accept_quest(clientApp().player)
                    