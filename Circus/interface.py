from settings import *
import math

class Interface:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.group = app.main_group
        self.attrs = INTERFACE_ATTRS[ name ]
        self.pos = vec2( self.attrs['pos'] )
        self.size = vec2( self.attrs['size'] )
        self.interactibles = {}
        self.rect = pg.Surface(self.size)

        def draw(self):
            self.image = pg.image.load( self.attrs[ 'path' ] ).convert_alpha()
            gui_sprite = pg.Surface(self.size)
            gui_sprite.blit(self.image)

        def update( self ):
            self.draw()