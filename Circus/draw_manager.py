import math
from shared import *

class LayerMask( pg.sprite.LayeredUpdates ):
    """Layermask class

    Args:
        pg (pygame): pygame macro
    """
    
    def __init__( self, order, *sprites, **kwargs ):
        super().__init__( sprites, kwargs )
        self.order = order

    def set_order( self, order ):
        self.order = order
        clientApp().draw_manager.sort_layers_by_order()

class DrawManager:
    """Draw Manager class
    """
    
    def __init__( self ):
        self.layer_masks: dict = {}
        self.drawables = []
        self.dirty = True
        self.angle = True

        # Default masks
        self.layer_masks["tile_layer"] = LayerMask(-1)
        self.layer_masks["main_layer"] = LayerMask(0)
        self.layer_masks["entity_layer"] = LayerMask(1)

        self.layer_masks["hud_layer"] = LayerMask(999)
    
    def set_dirty( self, angle = False ):
        """force a draw call update

        Args:
            repeats (int, optional): number of times to redraw. Defaults to 2.
        """
        self.dirty = True
        self.angle = self.angle or angle

    def update( self ):
        if( self.dirty ):
            self.screenpos_update()

        for layer in self.layer_masks.values():
            layer.update()

    def draw( self ):
        for drawable in list(self.drawables):
            drawable._draw_update()

        for layer in self.layer_masks.values():
            layer.draw( clientApp().screen )

    def screenpos_update( self ):
        if( self.angle ):
            clientApp().material_system.recalculate_tile_rotation()
            try:
                clientApp().scene.redraw_tile_rotation()
            except:
                pass

        for drawable in self.drawables:
            drawable._screenpos_update()
        
        self.dirty = False
        self.angle = False

    def sort_layers_by_order( self ):
        self.layer_masks = dict(sorted(self.layer_masks.items(), key=lambda item: item[1].order))

    def add_layer( self, name: str, order: int ):
        """adds a draw layer by name defined by the order

        Args:
            name (string): layer name
            order (int): number of layer in order
        """
        self.layer_masks[name] = LayerMask( order )
        self.sort_layers_by_order()

    def add_drawable( self, drawable ):
        """adds a drawable object

        Args:
            drawable ( object ): the object to add
        """
        self.drawables.append(drawable)

    def remove_drawable( self, drawable ):
        """removes a drawable object

        Args:
            drawable ( object ): the object to remove
        """
        self.drawables.remove(drawable)