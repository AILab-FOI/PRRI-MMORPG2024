from shared import *
import player
from shared import _globals
import inventory_item


class Inventory ( object ):
    """Inventory base class

    """    
    def __init__( self, id = None, owner = None, *items ):
        super().__init__( )
        self.id = id
        self.items_list = []
        for item in items:
            self.items_list.append(item)
    
        # reference to the inventory's owner, fix if wrong
        self.owner = owner


    def set_owner(self, owner):
        self.owner = owner

    def delete_items(self, items):
        if len(self.items_list) <= 0:
            raise Exception("inventory cannot contain negative items")
        else:
            for item in items:
                if len(self.items_list) > 0:
                    self.items_list.remove(item)
                else:
                    raise Exception("cannot remove any more items")

        self.on_inventory_updated()
        self.update_info()

    def add_items(self, items):
        # if len(self.items_list) >= 3:
        #     raise Exception("inventory cannot go over 3 items")
        # else:
        
        # removed limit on items for now

        for item in items:
             self.items_list.append(item)

        self.on_inventory_updated()
        self.update_info()
    
    def items_string(self) -> str:
        return str(self.items_list)
    
    # Called before info is sent to server
    def on_inventory_updated( self ):
        pass

    def update_info(self):
        message = {"command": "update_inventory_info"}
        message['inventory'] = self.id
        message['player'] = clientApp().username
        message['inventory_items'] = self.items_list

        clientApp().push_websocket_message(message, False)








