from shared import *
from interactible import Interactible
import math
import logging

#
#   General Interface class for all Graphical elements for display and interaction with the player

class Interface( pg.sprite.Sprite ):
    def __init__(self, name, shown=True ):
        """Interface class

        Args:
            name (string): identifiable name for shared.py
            shown (bool): to immediately render interface or to wait for interface.show() to be called 
        """
        self.name = name
        self.shown = shown
        self.attrs = INTERFACE_ATTRS[ self.name ]
        self.group = clientApp().draw_manager.layer_masks["hud_layer"]
        super().__init__( self.group )
        self.pos = vec2( self.attrs[ 'pos' ] )
        self.size = vec2( self.attrs[ 'size' ] )
        self.interactable = False
        if self.shown:
            self.create_interactions()
        
        self.sprite = pg.image.load( self.attrs[ 'path' ] ).convert_alpha()
        if self.shown:
            self.image = pg.image.load( self.attrs[ 'path' ] ).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
        else:
            self.image = pg.Surface( (0, 0) )
            self.rect = self.image.get_rect()
        self.group.change_layer( self, self.attrs[ 'z' ] )
    
    def __del__( self ):
        self.remove_interactions()

    def update( self ):
        self.get_image()
    
    def get_image( self ):
        if self.shown:
            self.image = pg.image.load( self.attrs[ 'path' ] ).convert_alpha()
            clientApp().screen.blit(self.image, self.rect)
        else:
            self.image = None
    
    def show( self ):
        """Displays interface, recreating interactibles
        """
        if not self.shown:
            self.create_interactions()
        self.shown = True
        self.image = pg.image.load( self.attrs[ 'path' ] ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def hide( self ):
        """Hides interface, removing interactibles
        """
        if self.shown:
            self.remove_interactions()
        self.shown = False
        self.image = pg.Surface( (0, 0) )
        self.rect = self.image.get_rect()

    def create_interactions ( self ):
        if 'interactibles' in self.attrs:
            self.interactable = True
            self.interactibles = INTERFACE_ATTRS[ self.name ][ 'interactibles' ]
            for interaction in self.interactibles:
                Interactible(self.name, interaction, self.attrs[ 'z' ])
    
    def remove_interactions ( self ):
        if 'interactibles' in self.attrs:
            self.interactable = False
            for interaction in clientApp().clickable_group:
                if interaction.name == self.name:
                    interaction.drop()
                    del interaction


class BarInterface( Interface ):
    def __init__(self, name, shown=True):
        """Bar Interface class
        Used for UI elements that track information in the style of a "bar"
        To track information REQUIRES for the information to be added to clientApp().trackables

        Args:
            name (string): identifiable name for shared.py
            shown (bool): to immediately render interface or to wait for interface.show() to be called 
        """
        super().__init__(name, shown)
        self.frames = self.attrs[ 'frames' ]
        self.tracking = self.attrs[ 'tracking' ]
        self.frame_index = 0
        self.sheet = self.get_sheet()

    def update( self ):
        super().update()
        self.updateFrameIndex()
        self.get_image()

    def updateFrameIndex( self ):
        trackable = clientApp().trackables[self.tracking]
        tracked_stat = getattr(trackable['object'], trackable['attr'])
        self.frame_index = (self.frames - 1) - math.floor(tracked_stat / trackable[ 'max' ] * (self.frames - 1))
    
    def get_sheet( self ):
        sheet_width = self.sprite.get_width()
        sheet_height = self.sprite.get_height()
        sprite_width = sheet_width // self.frames
        sprite_sheet = []
        for x in range( 0, sheet_width, sprite_width):
            sprite = self.sprite.subsurface( ( x, 0, sprite_width, sheet_height ))
            sprite_sheet.append( sprite )
        return sprite_sheet

    
    def get_image( self ):
        self.image = self.sheet[ self.frame_index ]