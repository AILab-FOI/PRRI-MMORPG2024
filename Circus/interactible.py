from shared import *
import math
import logging

#
#   General class for mouse interactive elements, assumes the interactive element is a square, currently only attachable to Interface items

class Interactible:
    def __init__(self, name, interaction='default', z=0):
        self.name = name
        self.attrs = INTERFACE_ATTRS[ name ][ 'interactibles' ][ interaction ]
        self.x = self.attrs['x']
        self.y = self.attrs['y']
        self.width = self.attrs['width']
        self.height = self.attrs['height']
        self.interaction = self.attrs['interaction'] 
        self.interact_with = self.attrs['interact-with']
        
        self.z = z

        #
        #   Group that collects all Interactible areas, used for sifting through all of them when checking on click
        clientApp().clickable_group.append( self )

        #
        # Debug print
        print("Creating interaction for: " + self.name)
        print(self.interact_with)


    def drop( self ):
        clientApp().clickable_group.remove( self )

        #
        #   Method to attempt interacting with an interactible area, if succesful it will return the interaction
        #   else returns empty string, on mouse clicking event before doing anything else check if its interacting

    def try_interact( self, event ):
        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = pg.mouse.get_pos()
            if mx > self.x and my > self.y and mx < self.x + self.width and my < self.y + self.height:
                return {'z':self.z, 'interaction':self.interaction}
        elif event.type == pg.KEYDOWN:
            if event.key in self.interact_with:
                return {'z':self.z, 'interaction':self.interaction}
        return ''