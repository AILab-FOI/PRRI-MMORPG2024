from shared import *
import math
from entity import BaseSpriteEntity
from bullet import Bullet
from itertools import cycle
import json

from viewpoint import Viewpoint


class Player( BaseSpriteEntity ):
    """Player base class

    Args:
        BaseSpriteEntity ( BaseSpriteEntity ): Sprite entity to create the player from
    """    
    def __init__( self, name='player' ):
        super().__init__( name )

        self.offset = vec2( 0 )
        self.last_offset = vec2( 0 )
        
        self.inc = vec2( 0 )
        self.prev_inc = vec2( 0 )
        self.last_inc = vec2( 0 )
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt( 2 )

        self.viewpoint = Viewpoint()

        self.down_ind = [ 3, 7, 11, 15 ]
        self.down_list = cycle( self.down_ind )
        self.up_ind = [ 2, 6, 10, 14 ]
        self.up_list = cycle( self.up_ind )
        self.left_ind = [ 1, 5, 9, 13 ]
        self.left_list = cycle( self.left_ind )
        self.right_ind = [ 0, 4, 8, 12 ]
        self.right_list = cycle( self.right_ind )

        self.direction = 'DOWN'
        self.moving = False

        self.message = """Welcome to the Circus of Game Mechanics! Where everything is important, but nothing realy matters.

What are game mechanics, you ask? Well, let me show you!

Game Mechanics are the rules and systems that govern player interactions within a game.

They are important because they provide structure, challenge, and variety in games.

As a first, I am the ring master, the narrator of this game. This is our first mechanic related to story and narrative. 

It can include branching storylines, dialogue choices, moral and ethical choices, and quest systems which provide narrative depth and immersion.

Let us walk through the circus and I show you some of our performers!

"""
    def on_start_drawing(self):
        super().on_start_drawing()
        self.sprite.groups()[0].change_layer( self.sprite, CENTER.y )

        self.sprite.rect = self.sprite.image.get_rect( center=CENTER )

    def forward( self ):
        ret = vec2()
        ret.x = math.cos(-self.angle-(math.pi/2))
        ret.y = math.sin(-self.angle-(math.pi/2))
        return ret
    
    def right( self ):
        ret = vec2()
        ret.x = math.cos(-self.angle)
        ret.y = math.sin(-self.angle)
        return ret

    def animate( self ):
        if clientApp().anim_trigger:
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

            self.sprite.image = self.images[ self.frame_index ]


    def control( self ):
        self.moving = False
        self.inc = vec2( 0 )
        speed = PLAYER_SPEED * clientApp().delta_time
        rot_speed = PLAYER_ROT_SPEED * clientApp().delta_time

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

    def single_fire( self, event ):
        if event.key == pg.K_UP:
            Bullet( "bullet", self.pos )
        if event.key == pg.K_SPACE:
            clientApp().message.handle_input()

    def check_collision( self ):
        if( self.sprite == None ):
            return

        hitobst = pg.sprite.spritecollide( self.sprite, clientApp().collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask )
        hit = pg.sprite.spritecollide( self.sprite, clientApp().draw_manager.layer_masks['entity_layer'],
                                      dokill=False, collided=pg.sprite.collide_mask )
        if not hitobst and not hit:
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            self.inc = -self.prev_inc
            if hit:
                clientApp().message.set_message( hit[ 0 ].entity.message )
                clientApp().message.active = True
            if hitobst and hitobst[ 0 ].message != '':
                clientApp().message.set_message( hitobst[ 0 ].entity.message )
                clientApp().message.active = True


    def move( self ):
        self.offset += self.inc
        x = self.offset[ 0 ]
        y = self.offset[ 1 ]
        x1 = self.last_offset[ 0 ]
        y1 = self.last_offset[ 1 ]
        if x != x1 or y != y1:
            message = { "command":"update", "id": clientApp().username, "position": { "x": x, "y": y } }
            clientApp().push_websocket_message( message )

            self.last_offset[ 0 ] = self.offset[ 0 ]
            self.last_offset[ 1 ] = self.offset[ 1 ]

    def should_think(self) -> bool:
        return True
    
    def update_visuals(self):
        self.animate()
        self.pos = self.offset
        self.viewpoint.set_ang( self.angle )
        self.viewpoint.set_pos( self.offset )

    def think( self ):
        self.control()
        self.check_collision()
        self.move()
















