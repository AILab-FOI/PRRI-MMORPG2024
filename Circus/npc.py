from shared import *
import entity
from quest import Quest
from quests.test_quest import PositionQuest
from typing import List

NPCS = {
    'test_npc': {
        'name': 'Guggy',
        'entity': 'kitty',
        'quests': PositionQuest("TEST_QUEST_2", 
                vec2( 16 * TILE_SIZE, 20 * TILE_SIZE ) ),
    },
}

class NPCBase( entity.Entity ):
    def __init__( self, name, pos = vec2(0) ):
        template = NPCS[name]
        self.npc_name = template['name']

        super().__init__( template['entity'], pos )
        self.quests : List[Quest] = []

        quests = template['quests']

        if( quests == None ):
            return
        
        if( isinstance(quests, list) ):
            for id, quest in quests:
                self.add_quest(quest)
        else:
            self.add_quest(quests)

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
                    