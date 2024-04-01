from shared import *
from random import random
from itertools import cycle

class BaseEntity( pg.sprite.Sprite ):
    def __init__( self, name ):
        self.name = name
        if name == 'player' or name == 'bullet' or name == 'explosion':
            
            self.group = g.client_app.draw_manager.layer_masks["main_layer"]
        else:
            self.group = g.client_app.draw_manager.layer_masks["entity_layer"]
        super().__init__( self.group )

        self.attrs = ENTITY_SPRITE_ATTRS[ name ]
        entity_cache = g.client_app.cache.entity_sprite_cache
        self.images = entity_cache[ name ][ 'images' ]
        self.image = self.images[ 0 ]
        self.mask = entity_cache[ name ][ 'mask' ]
        self.rect = self.image.get_rect()
        self.frame_index = 0

    def animate( self ):
        if g.client_app.anim_trigger:
            self.frame_index = ( self.frame_index + 1 ) % len( self.images )
            self.image = self.images[ self.frame_index ]

    def update( self ):
        self.animate()


class Entity( BaseEntity ):
    def __init__( self, name, pos ):
        super().__init__( name )
        self.pos = vec2( pos ) * TILE_SIZE
        self.player = g.client_app.player
        self.y_offset = vec2( 0, self.attrs[ 'y_offset' ] )
        self.screen_pos = vec2( 0 )

        try:
            self.message = self.attrs[ 'message' ]
        except:
            self.message = ''

    def update( self ):
        super().update()
        self.transform()
        self.set_rect()
        self.change_layer()

    def transform( self ):
        pos = self.pos - self.player.offset
        pos = pos.rotate_rad( self.player.angle )
        self.screen_pos = pos + CENTER

    def change_layer( self ):
        self.group.change_layer( self, self.screen_pos.y )

    # Rect is the actual thing used in the draw call to determine the position
    def set_rect( self ):
        self.rect.center = self.screen_pos + self.y_offset



class RemotePlayer( Entity ):
    def __init__( self, name, pos, username ):
        super().__init__( name, pos )
        self.username = username

        self.down_ind = [ 3, 7, 11 ]
        self.down_list = cycle( self.down_ind )
        self.up_ind = [ 0, 4, 8 ]
        self.up_list = cycle( self.up_ind )
        self.left_ind = [ 2, 6, 10 ]
        self.left_list = cycle( self.left_ind )
        self.right_ind = [ 1, 5, 9 ]
        self.right_list = cycle( self.right_ind )

        self.direction = 'DOWN'
        self.moving = False  
          
    def animate( self ):
        if g.client_app.anim_trigger or True: # TODO: ovo podesiti ako se pomakne remote igrač
            if self.direction == 'DOWN':
                if self.moving:
                    self.frame_index = next( self.down_list )
                else:
                    self.frame_index = self.down_ind[ 1 ]
            elif self.direction == 'UP':
                if self.moving:
                    self.frame_index = next( self.up_list )
                else:
                    self.frame_index = self.up_ind[ 1 ]
            elif self.direction == 'LEFT':
                if self.moving:
                    self.frame_index = next( self.left_list )
                else:
                    self.frame_index = self.left_ind[ 1 ]
            else:
                if self.moving:
                    self.frame_index = next( self.right_list )
                else:
                    self.frame_index = self.right_ind[ 1 ]

            self.image = self.images[ self.frame_index ]


    def control( self ):
        return        
        self.moving = False
        self.inc = vec2( 0 )
        speed = PLAYER_SPEED * g.client_app.delta_time
        rot_speed = PLAYER_ROT_SPEED * g.client_app.delta_time

        key_state = pg.key.get_pressed()

        if key_state[ pg.K_LEFT ]:
            self.angle += rot_speed
        if key_state[ pg.K_RIGHT ]:
            self.angle -= rot_speed

        if key_state[ pg.K_w ]:
            self.inc += vec2( 0, -speed ).rotate_rad( -self.angle )
            self.direction = 'UP'
            self.moving = True
        if key_state[ pg.K_s ]:
            self.inc += vec2( 0, speed ).rotate_rad( -self.angle )
            self.direction = 'DOWN'
            self.moving = True
        if key_state[ pg.K_a ]:
            self.inc += vec2( -speed, 0 ).rotate_rad( -self.angle )
            self.direction = 'LEFT'
            self.moving = True
        if key_state[ pg.K_d ]:
            self.inc += vec2( speed, 0 ).rotate_rad( -self.angle )
            self.direction = 'RIGHT'
            self.moving = True

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr

    
    def move( self ): # TODO: Ovdje bi trebalo staviti promjenu pozicije temeljem poruke
        self.pos = g.client_app.players_pos[ self.username ]

    def update( self ):
        super().update()
        self.transform()
        self.set_rect()
        #self.change_layer()
        self.move()