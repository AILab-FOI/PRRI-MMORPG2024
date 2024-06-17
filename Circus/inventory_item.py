import json
from shared import *

class InventoryItem(object):
    def __init__(self, id = 0, name = "test item", description = "this is a test item", type = "armor", stat = 1):
        super().__init__()
        self.id = id
        self.name = name
        self.description = description
        # type moze biti weapon, armour, ili none
        # zamisao je da se uspoređuje string?
        self.type = type
        self.stat = stat

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True)