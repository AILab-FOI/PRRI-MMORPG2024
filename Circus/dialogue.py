from interface import Interface
from shared import *
import textwrap
from itertools import chain
import math
class Dialogue( Interface ):

    def __init__( self, name = 'dialogue-box', font_size = 13, max_lines = 6, color = ( 29, 29, 29 ), source = None, shown=False):
        """Dialogue class

        Args:
            name (string): identifiable name for shared.py, defaults to dialogue-box
            font_size (int): size of the font to display
            max_lines (int): maximum number of lines to display
            color (vec3): RGB color for the text
            source (WorldObject): object that is "sending" the dialogue, used for checking distance to cancel dialogue when getting too far away
        """
        super().__init__(name, shown)
        self.font = pg.font.Font( "assets/PressStart2P-Regular.ttf", font_size )
        if "max_lines" in self.attrs:
            self.max_lines = self.attrs[ 'max_lines' ]
        else:
            self.max_lines = max_lines

        if "color" in self.attrs:
            self.color = self.attrs[ 'color' ]
        else:
            self.color = color
        self.text_pos = self.attrs[ 'text-pos' ]
        self.text_area = self.attrs[ 'text-area' ]
        self.line_height = self.font.get_height()
        self.text_index = 0
        self.inner_surface = pg.Surface((self.text_area['width'], self.text_area['height']))
        self.source = source
        self.msg = ''

    def set_message( self, msg, width=25 ):
        """Sets message up for displaying within the inner_surface, automatically wraps it

        Args:
            msg (string): text to place into the dialogue
            width (int): number of characters before wrapping, defaults to 25
        """
        t = [ textwrap.wrap( m, width=width ) for m in msg.split( '\n' ) ]
        self.wrapped_text = list( chain( *t ) )

    def display( self, offset=0 ):
        """Displays dialogue

        Args:
            offset (int): offset used for moving text up or down, defaults to no offset
        """
        self.show()
        self.show_text = self.wrapped_text[ self.text_index:self.text_index + self.max_lines ]
        self.clear_text( self.inner_surface )

        height = len(self.show_text) * self.line_height * 1.1
        if height > self.text_area['height']:
            y = self.text_area['height'] - height
        else:
            y = 0

        for i, line in enumerate( self.show_text ):
            aligning = y + i * self.line_height * 1.1 - offset
            self.render_text( line, self.inner_surface, align=aligning  )
        self.image.blit( self.inner_surface, self.text_pos)

    def close( self ):
        """Hides the dialogue
        """
        self.hide()
    
    def handle_input( self ):
        """Input handling for the default 'dialogue-box', moves index to next set of max_lines of the message
        """
        if self.text_index < len( self.wrapped_text ):
            self.text_index += self.max_lines
            self.display()
        else:
            self.text_index = 0
            self.close()
            if( hasattr(self, "listener") ):
                self.listener.end_speak()
    
    def dist_to_source( self ):
        """Distance from player to dialogues' source object

        Returns:
            int: returns the distance to source
        """
        if not self.source:
            return 0
        dist_x = clientApp().player.pos.x - self.source.pos.x
        dist_y = clientApp().player.pos.y - self.source.pos.y
        dist = math.sqrt((dist_x ** 2) * (dist_y ** 2))
        return dist

    def update( self ):
        if not self.shown:
            self.hide()
    
    def clear_text( self, surface):
        """Clears surface to prepare for new text rendering

        Args:
            surface (pygame.Surface): surface to clear
        """
        surface.fill((0,0,0))
        surface.set_colorkey((0,0,0))

    def render_text( self, msg, surface, align=0, alignmode = 'top' , color=None):
        """Renders text onto an inner surface, preparing for it to get .blit onto an image

        Args:
            msg (string): text to render
            surface (pygame.Surface): text surface to render onto
            align (int): offset for moving the text usually to show latest text inputted
            alignmode (string): 'left' or 'top' for offsetting from the left or top
            color (vec3): font color used for overriding dialogues preset color, if None will default to the preset color
        """
        font_color = self.color
        if color:
            font_color = color
        text = self.font.render( msg, False, font_color)
        text_rect = text.get_rect()

        match alignmode:
            case 'top':
                text_rect.top = align
            case 'left':
                text_rect.left = align
            case 'bottom':
                text_rect.left = align
            case 'right':
                text_rect.left = align

        surface.blit( text, text_rect )
        surface.set_colorkey((0,0,0))