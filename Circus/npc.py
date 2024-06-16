from shared import *
import entity
from quest import Quest
from typing import List

class NPCBase( entity.Entity ):
    def __init__( self, name, pos = vec2(0), quests = None ):
        self.npc_name = name
        super().__init__( "kitty", pos )
        self.quests : List[Quest] = []

        if( quests == None ):
            return
        
        if( isinstance(quests, list) ):
            for id, quest in quests:
                self.add_quest(quest)
        else:
            self.add_quest(quests)

    def add_quest( self, quest ):
        clientApp().quest_list[id] = quest
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
                    