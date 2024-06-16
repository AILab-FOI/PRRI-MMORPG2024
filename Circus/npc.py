from shared import *
import entity
from quest import Quest, ItemReward
from quests.test_quest import PositionQuest
from typing import List

NPCS = {
    'test_npc': {
        'name': 'Guggy',
        'entity': 'kitty',
        'quests': PositionQuest(id="TEST_QUEST_POSITION", 
                position=vec2( 16 * TILE_SIZE, 20 * TILE_SIZE ),
                reward=ItemReward("Apple(+doctor resistance)","Outdated Magazine"),
                title = "The Testiest Quest",
                text = "Move to the lower right tree." ),
    },
}

class NPCBase( entity.Entity ):
    def __init__( self, name, pos = vec2(0), template=None ):
        super().__init__( name, pos )

        self.npc_name = name
        self.quests : List[Quest] = []

        if( template != None ):
            self.load_npc_template(template)

    def load_npc_template(self, name):
        template = NPCS[name]
        # Load default entity stuff
        self.load_attrs_from_name(template['entity'])

        self.npc_name = template['name']
        self.quests : List[Quest] = []

        quests = template['quests']

        if( quests == None ):
            return
        
        if( isinstance(quests, list) ):
            for id, quest in quests:
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
    
    def think(self):
        for quest in self.quests:
            if( quest.is_in_progress() ):
                if( quest.check_quest_finished() ):
                    quest.finish_quest()
            elif( not quest.is_finished() ):
                if( quest.check_quest_conditions() ):
                    quest.accept_quest(clientApp().player)
                    