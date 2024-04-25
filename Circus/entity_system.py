from shared import *


class EntitySystem(object):
    """This is the Entity System base class.

    Args:
        object (object): python base class
    """
    
    def __init__( self ):
        self.entity_list: dict = {}
        self.delete_list: list = []
        self.index = 0
    
    def add_entity( self, entity ):
        """Adds an entity

        Args:
            entity ( entity_type ): entity to add
        """        
        self.entity_list[self.index] = entity
        entity.ent_index = self.index
        self.index += 1

    def remove_entity( self, index: int ):
        """Removes an entity

        Args:
            index (int): index/id of the entity in the dictionary to remove
        """        
        self.entity_list.pop(index)

    def think( self ):
        """Entity function that executes every frame
        If no behaviour, skips it
        """        
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
        """Deletes an entity

        Args:
            entity (entity_type): Entity to delete
        """        
        self.delete_list.append(entity)