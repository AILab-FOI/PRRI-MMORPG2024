from shared import *


class Cache:
    """Cache base class
    """    
    def __init__( self ):
        clientApp().done_counter = 0

        # This dictionary contains all the raw layers of each stacked sprite
        self.stacked_sprite_layer_cache = {}
        # This dictionary contains the data for our sprites
        self.entity_sprite_cache = {}
        
        # Used in calculations, NUM_ANGLES defines how many possible angles a precompiled stacked sprite can have
        self.viewing_angle = 360 // NUM_ANGLES
        self.outline_thickness = 5
        self.alpha_value = 70  #

        #self.get_stacked_sprite_cache()
        #self.get_entity_sprite_cache()

    # This method should be called when a scene loads
    # It takes all our sprite data and saves it into the cache
    def cache_entity_sprite_data( self ):
        """Called when a scene loads.
        Takes all the sprite data and saves it into the cache.
        """        
        # Go through each sprite entity
        for sprite_name in ENTITY_SPRITE_ATTRS:
            # Create entry in our cache
            self.entity_sprite_cache[ sprite_name ] = {
                'images': None
            }

            # Get our entities attributes
            attrs = ENTITY_SPRITE_ATTRS[ sprite_name ]

            images = self.create_stack_layer_array( attrs )
            
            self.entity_sprite_cache[ sprite_name ][ 'images' ] = images

            mask = self.create_entity_mask( attrs, images )
            self.entity_sprite_cache[ sprite_name ][ 'mask' ] = mask

    def create_entity_mask( self, attrs: dict, images: list ) -> pg.Mask:
        """Creates an entity mask

        Args:
            attrs ( dict ): Dictionary of attributes
            images ( list ): Array of images

        Returns:
            Mask: Entity mask
        """        
        path = attrs.get( 'mask_path', False )
        if not path:
            return pg.mask.from_surface( images[ 0 ] )
        else:
            scale = attrs[ 'scale' ]
            mask_image = pg.image.load( path ).convert_alpha()
            mask_image = pg.transform.scale( mask_image, vec2( mask_image.get_size() ) * scale )
            return pg.mask.from_surface( mask_image )

    def cache_stacked_sprite_data( self ):
        """Caches stacked sprite data

        Yields:
            status: whether it was done or not
        """        
        for obj_name in STACKED_SPRITE_ATTRS:
            self.stacked_sprite_layer_cache[ obj_name ] = {
                'rotated_sprites': {},
                'alpha_sprites': {},
                'collision_masks': {}
            }
            attrs = STACKED_SPRITE_ATTRS[ obj_name ]
            layer_array = self.create_stack_layer_array( attrs )
            self.compile_stacked_sprite_angles( obj_name, layer_array, attrs )
            clientApp().done_counter += 1
            yield 1
        yield 'done'

    def compile_stacked_sprite_angles( self, obj_name: str, layer_array: list, attrs: dict ):
        """Compiles the stacked sprite angles of a given stacked sprite

        Args:
            obj_name (str): object's name
            layer_array (list): array of the slices
            attrs (dict): sprite attributes
        """        
        outline = attrs.get( 'outline', 0 )
        transparency = attrs.get( 'transparency', False )
        mask_layer = attrs.get( 'mask_layer', attrs[ 'num_layers' ] // 2 )

        for angle in range( NUM_ANGLES ):
            layer_size = layer_array[ 0 ].get_size()
            surf = pg.Surface( layer_size )
            surf = pg.transform.rotate( surf, angle * self.viewing_angle )
            sprite_surf = pg.Surface( [ surf.get_width(), surf.get_height()
                                      + attrs[ 'num_layers' ] * attrs[ 'scale' ]] )
            sprite_surf.fill( 'khaki' )
            sprite_surf.set_colorkey( 'khaki' )

            for layer_index, layer in enumerate( layer_array ):
                layer = pg.transform.rotate( layer, angle * self.viewing_angle )
                sprite_surf.blit( layer, ( 0, layer_index * attrs[ 'scale' ] ))

                # get collision mask
                if layer_index == mask_layer:
                    surf = pg.transform.flip( sprite_surf, True, True )
                    mask = pg.mask.from_surface( surf )
                    self.stacked_sprite_layer_cache[ obj_name ][ 'collision_masks' ][ angle ] = mask

            # get outline
            if outline:
                outline_coords = pg.mask.from_surface( sprite_surf ).outline()
                pg.draw.polygon( sprite_surf, 'black', outline_coords, outline )

            # get alpha sprites
            if transparency:  #
                alpha_sprite = sprite_surf.copy()
                alpha_sprite.set_alpha( self.alpha_value )
                alpha_sprite = pg.transform.flip( alpha_sprite, True, True )
                self.stacked_sprite_layer_cache[ obj_name ][ 'alpha_sprites' ][ angle ] = alpha_sprite

            image = pg.transform.flip( sprite_surf, True, True )
            self.stacked_sprite_layer_cache[ obj_name ][ 'rotated_sprites' ][ angle ] = image



    def create_stack_layer_array( self, attrs: dict ) -> list:
        """Creates a stack sprite layer array, returns the layer array in reverse order

        Args:
            attrs ( dict ): dictionary of attributes

        Returns:
            list: layer array list in reverse
        """        
        # load sprite sheet
        sprite_sheet = pg.image.load( attrs[ 'path' ] ).convert_alpha()
        # scaling
        sprite_sheet = pg.transform.scale( sprite_sheet,
                                          vec2( sprite_sheet.get_size() ) * attrs[ 'scale' ] )
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        sprite_height = sheet_height // attrs[ 'num_layers' ]
        # new height to prevent error
        sheet_height = sprite_height * attrs[ 'num_layers' ]
        # get sprites
        layer_array = []
        for y in range( 0, sheet_height, sprite_height ):
            sprite = sprite_sheet.subsurface( (0, y, sheet_width, sprite_height ))
            layer_array.append( sprite )
        return layer_array[ ::-1 ]