from shared import *

class LayerMask( pg.sprite.LayeredUpdates ):
    def __init__( self, order, *sprites, **kwargs ):
        super().__init__( sprites, kwargs )
        self.order = order

    def set_order( self, order ):
        self.order = order
        clientApp().draw_manager.sort_layers_by_order()

class DrawManager:
    def __init__( self ):
        self.layer_masks: dict = {}
        self.drawables = []
        self.dirty = True

        # Default masks
        self.layer_masks["tile_layer"] = LayerMask(-1)
        self.layer_masks["main_layer"] = LayerMask(0)
        self.layer_masks["entity_layer"] = LayerMask(1)

        self.layer_masks["hud_layer"] = LayerMask(999)

    def update( self ):
        if( self.dirty ):
            print(self.dirty)
            self.screenpos_update()
            self.dirty = False

        for layer in self.layer_masks.values():
            layer.update()

    def draw( self ):
        for drawable in list(self.drawables):
            drawable._draw_update()

        for layer in self.layer_masks.values():
            layer.draw( clientApp().screen )

    def screenpos_update( self ):
        for drawable in self.drawables:
            drawable._screenpos_update()

    def sort_layers_by_order( self ):
        self.layer_masks = dict(sorted(self.layer_masks.items(), key=lambda item: item[1].order))

    def add_layer( self, name, order ):
        self.layer_masks[name] = LayerMask( order )
        self.sort_layers_by_order()

    def add_drawable( self, drawable ):
        self.drawables.append(drawable)
        self.dirty = True

    def remove_drawable( self, drawable ):
        self.drawables.remove(drawable)