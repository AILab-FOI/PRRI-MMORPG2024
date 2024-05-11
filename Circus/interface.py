from settings import *
from interactible import Interactible
import math

class Interface( pg.sprite.Sprite ):
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.group = app.main_group
        super().__init__( self.group )
        self.attrs = INTERFACE_ATTRS[ name ]
        self.pos = vec2( self.attrs['pos'] )
        self.size = vec2( self.attrs['size'] )
        self.interactibles = INTERFACE_ATTRS[ name ][ 'interactibles' ]
        for interaction in self.interactibles:
            Interactible(self.app, self.name, interaction)
        
        self.image = pg.image.load( self.attrs[ 'path' ] ).convert_alpha()
        self.rect = self.image.get_rect()

        self.group.change_layer( self, 900)