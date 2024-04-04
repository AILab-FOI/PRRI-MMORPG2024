from shared import *

class EntitySystem(object):
    def __init__( self ):
        self.entity_list: dict = {}
        self.delete_list: list = []
        self.index = 0
    
    def add_entity( self, entity ):
        self.entity_list[self.index] = entity
        entity.ent_index = self.index
        self.index += 1

    def remove_entity( self, index ):
        self.entity_list.pop(index)

    def think( self ):
        for entity in list(self.delete_list):
            self.delete_list.remove(entity)
            self.remove_entity(entity.ent_index)

            clientApp().draw_manager.remove_drawable(entity)

            if( entity.sprite ):
                entity.sprite.kill()
                entity.sprite = None
            del entity

        for entity in list(self.entity_list.values()):
            if not entity.should_think():
                continue

            entity.think()
    
    def delete( self, entity ):
        self.delete_list.append(entity)