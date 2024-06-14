from settings import *
from interactible import Interactible

#
#   General Interface class for all Graphical elements for display and interaction with the player

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
    
    def __del__( self ):
        for interaction in self.interactibles:
            del interaction

    def update( self ):
        self.get_image()
    
    def get_image( self ):
        a = 3
        # need to make health and mana updates here