from shared import *
import math


class StackedSprite( pg.sprite.Sprite ):
    def __init__( self, name="", pos=vec2(0,0), rot=0, collision=True ):
        self.name = name
        self.pos = vec2( pos ) * TILE_SIZE
        self.player = clientApp().player
        self.group = clientApp().draw_manager.layer_masks["main_layer"]
        super().__init__( self.group )

        if collision:
            clientApp().collision_group.add( self )

        self.attrs = STACKED_SPRITE_ATTRS[ name ]
        self.y_offset = vec2( 0, self.attrs[ 'y_offset' ] )
        self.cache = clientApp().cache.stacked_sprite_layer_cache
        self.viewing_angle = clientApp().cache.viewing_angle
        self.rotated_sprites = self.cache[ name ][ 'rotated_sprites' ]
        self.collision_masks = self.cache[ name ][ 'collision_masks' ]

        self.angle = 0
        self.screen_pos = vec2( 0 )
        self.rot = ( rot % 360 ) // self.viewing_angle

        self.image = self.rotated_sprites[ self.angle ]
        self.mask = self.collision_masks[ self.angle ]
        self.rect = self.image.get_rect()

        
        try:
            self.message = self.attrs[ 'message' ]
        except:
            self.message = ''
    
    def set_pos( self, pos ):
        self.pos = vec2( pos )

    def change_layer( self ):
        self.group.change_layer( self, self.screen_pos.y )

    def transform( self ):
        pos = self.pos - self.player.offset
        pos = pos.rotate_rad( self.player.angle )
        self.screen_pos = pos + CENTER

    def get_angle( self ):
        self.angle = -math.degrees( self.player.angle ) // self.viewing_angle + self.rot
        self.angle = int( self.angle % NUM_ANGLES )

    def update( self ):
        self.transform()
        self.get_angle()
        self.get_image()
        self.change_layer()

    def get_image( self ):
        self.image = self.rotated_sprites[ self.angle ]
        self.mask = self.collision_masks[ self.angle ]
        self.rect = self.image.get_rect( center=self.screen_pos + self.y_offset )


class TrnspStackedSprite( StackedSprite ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        clientApp().transparent_objects.append( self )

        self.alpha_trigger = False
        self.alpha_objects = self.cache[ self.name ][ 'alpha_sprites' ]
        self.dist_to_player = 0.0

    def get_dist_to_player( self ):
        self.dist_to_player = self.pos.distance_to( self.player.pos )

    def update( self ):
        super().update()
        self.get_dist_to_player()

    def get_image( self ):
        super().get_image()
        self.get_alpha_image()

    def get_alpha_image( self ):
        if( self.player.sprite == None ):
            return

        if self.alpha_trigger:
            if self.rect.centery > self.player.sprite.rect.top:
                if self.rect.contains( self.player.sprite.rect ):
                    self.image = self.alpha_objects[ self.angle ]
                    self.alpha_trigger = False