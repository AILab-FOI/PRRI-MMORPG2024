from settings import *
import math
import logging

class Interactible:
    def __init__(self, app, name, interaction):
        self.app = app
        self.attrs = INTERFACE_ATTRS[ name ][ 'interactibles' ][ interaction ]
        self.x = self.attrs['x']
        self.y = self.attrs['y']
        self.width = self.attrs['width']
        self.height = self.attrs['height']
        self.interaction = self.attrs['interaction']

        self.app.clickable_group.append( self )

        def try_interact( self ):
            mx, my = pg.mouse.get_pos()
            x = self.x - mx
            y = self.y - my
            if x < self.width and y < self.height:
                return self.interaction
            else:
                return ''
