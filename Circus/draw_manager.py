from shared import *

class LayerMask( pg.sprite.LayeredUpdates ):
    def __init__( self, order, *sprites, **kwargs ):
        super().__init__( sprites, kwargs )
        self.order = order

    def set_order( self, order ):
        self.order = order
        g.client_app.draw_manager.sort_layers_by_order()

class DrawManager:
    def __init__( self ):
        self.layer_masks: dict = {}

        # Default masks
        self.layer_masks["tile_layer"] = LayerMask(-1)
        self.layer_masks["main_layer"] = LayerMask(0)
        self.layer_masks["entity_layer"] = LayerMask(1)

        self.layer_masks["hud_layer"] = LayerMask(999)

    def update( self ):
        for layer in self.layer_masks.values():
            layer.update()
    
    def draw( self ):
        for layer in self.layer_masks.values():
            layer.draw( g.client_app.screen )

    def sort_layers_by_order( self ):
        self.layer_masks = dict(sorted(self.layer_masks.items(), key=lambda item: item[1].order))

    def add_layer( self, name, order ):
        self.layer_masks[name] = LayerMask( order )
        self.sort_layers_by_order()