from shared import *
import math
import logging

#
#   General class for mouse interactive elements, assumes the interactive element is a square, currently only attachable to Interface items

class Interactible:
    def __init__(self, name, interaction='default'):
        self.app = clientApp()
        self.attrs = INTERFACE_ATTRS[ name ][ 'interactibles' ][ interaction ]
        self.x = self.attrs['x']
        self.y = self.attrs['y']
        self.width = self.attrs['width']
        self.height = self.attrs['height']
        self.interaction = self.attrs['interaction'] 

        #
        #   Group that collects all Interactible areas, used for sifting through all of them when checking on click
        self.app.clickable_group.append( self )


    def __del__( self ):
        self.app.clickable_group.remove( self )


        #
        #   Method to attempt interacting with an interactible area, if succesful it will return the interaction
        #   else returns empty string, on mouse clicking event before doing anything else check if its interacting

    def try_interact( self ):
        mx, my = pg.mouse.get_pos()
        x = self.x - mx
        y = self.y - my
        if x < self.width and y < self.height:
            return self.interaction
        else:
            return ''