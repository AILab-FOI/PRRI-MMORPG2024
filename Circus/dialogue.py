from interface import Interface
from shared import *
import textwrap
from itertools import chain
import math
class Dialogue( Interface ):
    def __init__( self, name = 'dialogue-box', font_size = 15, max_lines = 5, color = ( 29, 29, 29 ), source = None):
        """Dialogue class

        Args:
            name (string): identifiable name for shared.py, defaults to dialogue-box
            font_size (int): size of the font to display
            max_lines (int): maximum number of lines to display
            color (vec3): RGB color for the text
            source (WorldObject): object that is "sending" the dialogue, used for checking distance to cancel dialogue when getting too far away
        """
        super().__init__(name, False)
        self.font = pg.font.Font( "assets/PressStart2P-Regular.ttf", font_size )
        self.max_lines = max_lines
        self.color = color
        self.text_pos = self.attrs[ 'text-pos' ]
        self.text_area = self.attrs[ 'text-area' ]
        self.line_height = self.font.get_height()
        self.text_index = 0
        self.inner_surface = pg.Surface((self.text_area['width'], self.text_area['height']))
        self.source = source
        self.msg = ''

    def set_message( self, msg, width=39 ):
        t = [ textwrap.wrap( m, width=width ) for m in msg.split( '\n' ) ]
        self.wrapped_text = list( chain( *t ) )

    def display( self, offset=0 ):
        self.show()
        self.show_text = self.wrapped_text[ self.text_index:self.text_index + self.max_lines ]
        self.inner_surface.fill((0,0,0))
        self.inner_surface.set_colorkey((0,0,0))

        height = len(self.show_text) * self.line_height * 1.1
        if height > self.text_area['height']:
            y = self.text_area['height'] - height
        else:
            y = 0

        for i, line in enumerate( self.show_text ):
            text = self.font.render( line, False, self.color)
            text_rect = text.get_rect()
            text_rect.top = y + i * self.line_height * 1.1 - offset
            self.inner_surface.blit( text, text_rect )
            self.inner_surface.set_colorkey((0,0,0))
        self.image.blit( self.inner_surface, self.text_pos)

    def close( self ):
        self.hide()
    
    def handle_input( self ):
        if self.text_index < len( self.wrapped_text ):
            self.text_index += self.max_lines
            self.display( self.msg )
        else:
            self.text_index = 0
            self.close()
    
    def dist_to_source( self ):
        if not self.source:
            return 0
        dist_x = clientApp().player.pos.x - self.source.pos.x
        dist_y = clientApp().player.pos.y - self.source.pos.y
        dist = math.sqrt((dist_x ** 2) * (dist_y ** 2))
        return dist

    def update( self ):
        if not self.shown:
            self.hide()
            