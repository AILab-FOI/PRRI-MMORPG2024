from interface import Interface
from shared import *
import textwrap
from itertools import chain

class Dialogue( Interface ):
    def __init__( self, pos, type = 'dialogue-box', font_size = 15, max_lines = 3):
        super().__init__(type, False)
        self.font = pg.font.Font( "assets/PressStart2P-Regular.ttf", font_size )
        self.max_lines = max_lines
        self.pos = pos
        self.text_pos = self.attrs[ 'text-pos' ]
        self.text_area = self.attrs[ 'text-area' ]
        self.line_height = self.font.get_height()
        self.text_index = 0
        self.inner_surface = pg.Surface((self.text_area['width'], self.text_area['height']))

    def set_message( self, msg ):
        t = [ textwrap.wrap( m, width=39 ) for m in msg.split( '\n' ) ]
        self.wrapped_text = list( chain( *t ) )

    def display( self, msg ):
        self.show()
        self.set_message( msg )
        self.show_text = self.wrapped_text[ self.text_index:self.text_index + self.max_lines ]

        for i, line in enumerate( self.show_text ):
            text = self.font.render( line, False, ( 29, 29, 29 ))
            text_rect = text.get_rect()
            text_rect.top = i * self.line_height
            self.inner_surface.blit( text, text_rect )
            self.inner_surface.set_colorkey((0,0,0))
        self.image.blit( self.inner_surface, self.text_pos)

    def close( self ):
        self.hide()
    
    def handle_input( self ):
        if self.text_index < len( self.wrapped_text ):
            self.text_index += self.max_lines
        else:
            self.text_index = 0
            self.close()
    
    def update( self ):
        return