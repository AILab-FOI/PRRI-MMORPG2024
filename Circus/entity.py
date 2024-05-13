from shared import *
from random import random
from itertools import cycle
import math

# Base class for anything that is within the world
# Handles displaying the object on the screen based on a given viewpoint
class WorldObject(object):
    """World Object base class for anything that is within the world
    Handles displaying the object on the screen based on a given viewpoint

    Args:
        object ( object ): world object
    """    
    def __init__( self, pos=( 0, 0 ) ):
        self.pos: vec2 = vec2( pos )
        self.screen_pos: vec2 = vec2( 0 )
        self.screen_ang = 0
        self.visible: bool = True
        self.always_update: bool = False
        self.is_drawing = False
        clientApp().draw_manager.add_drawable(self)
    
    def __del__(self):
        clientApp().draw_manager.remove_drawable(self)

    def set_pos( self, newPos ):
        if( newPos == self.pos ):
            return

        self.pos = newPos

        if( self.sprite ):
            self.update_screenpos()

    def calculate_viewpoint_position( self ):
        viewpoint = clientApp().active_viewpoint

        if( viewpoint == None ):
            return

        view_pos = self.pos - viewpoint.offset
        view_pos = view_pos.rotate_rad( viewpoint.angle )
        self.screen_pos = view_pos + CENTER

        self.screen_ang = -math.degrees( viewpoint.angle )

    # Called by Sprite layers - Primarily used for visuals
    def _draw_update( self ):
        """Called by Sprite layers - Primarily used for visuals
        """        
        if( not self.is_visible() ):

            return

        self.calculate_viewpoint_position()

        if( self.is_drawing != self.should_draw() ):
            self.is_drawing = self.should_draw()

            if( self.is_drawing ):
                self.on_start_drawing()
            else:
                self.on_stop_drawing()

        if( not self.is_drawing ):
            return
        
        if( not self._should_update_visuals() ):
            return
        
        self.update_visuals()
    
    # If this object is supposed to be visible
    def is_visible(self) -> bool:
        """If you can, at any point, see the object

        Returns:
            bool: Returns the object's visibility
        """        
        return self.visible
    
    # If we should CURRENTLY draw the object
    def should_draw(self) -> bool:
        if( not self.is_visible() ):
            return False
        
        if( not self._should_update_visuals() ):
            return False
        
        return True
    
    # Check if we should call the visual update
    def _should_update_visuals(self) -> bool:
        """Check if visuals should be updated

        Returns:
            bool: Returns true if the object is set to "always_update" or if self.is_in_pov()
        """        
        return self.always_update or self.is_in_pov()

    # Is the object in our line of sight
    def is_in_pov(self) -> bool:

        """Checks if the object is in our line of sight

        Returns:
            bool: Returns true if the object is in the line of sight
        """        
        # TODO: Implement
        viewpoint = clientApp().active_viewpoint

        buffer = TILE_SIZE

        screen_start = 0
        screen_start -= buffer

        screen_end = max(viewpoint.size.x,viewpoint.size.y)
        screen_end += buffer

        if( self.screen_pos.x > screen_end ):
            return False
        
        if( self.screen_pos.y > screen_end ):
            return False
        
        if( self.screen_pos.x < screen_start ):
            return False
        
        if( self.screen_pos.y < screen_start ):
            return False
        
        return True

    
    # Called every frame when in view
    # Replace for classes with visuals
    def update_visuals(self):
        """Called for every frame when in view
        """        
        pass

    # When the viewpoint changes, this triggers
    def _screenpos_update(self):
        """This is triggered when the viewpoint changes
        """        
        if( not self.is_drawing ):
            return
        
        self.update_screenpos()

    # Called whenever the viewpoint changes and we're in view
    # Replace for classes with visuals
    def update_screenpos(self):
        pass

    def should_think(self) -> bool:
        return False
    
    def on_stop_drawing(self):
        pass

    def on_start_drawing(self):
        pass

class BaseSpriteEntity( WorldObject ):
    """BaseSpriteEntity class 

    Args:
        WorldObject ( WorldObject ): _description_
    """    
    def __init__( self, name, pos=( 0, 0 ) ):
        super().__init__( pos )
        self.name = name
        self.ent_index = -1 # -1 means unassigned entindex

        self.group = None
        import player
        import bullet
        if isinstance( self, player.Player ) or isinstance( self, bullet.Bullet) or isinstance( self, bullet.Explosion ):
            self.group = clientApp().draw_manager.layer_masks["main_layer"]
        else:
            self.group = clientApp().draw_manager.layer_masks["entity_layer"]

        clientApp().entity_system.add_entity(self)

        self.sprite = None

        self.attrs = ENTITY_SPRITE_ATTRS[ self.name ]
        entity_cache = clientApp().cache.entity_sprite_cache
        self.images = entity_cache[ self.name ][ 'images' ]
        self.mask = entity_cache[ self.name ][ 'mask' ]
        self.frame_index = 0
    
    def on_start_drawing(self):
        super().on_start_drawing()
        self.sprite = pg.sprite.Sprite( self.group )
        self.sprite.entity = self

        self.sprite.image = self.images[ 0 ]
        self.sprite.rect = self.sprite.image.get_rect()

        self.update_screenpos()
    
    def on_stop_drawing(self):
        super().on_stop_drawing()
        self.sprite.kill()
        self.sprite = None

    def __del__(self):
        pass

    def kill(self):
        clientApp().entity_system.delete(self)
        del self

    def animate( self ):
        
        if clientApp().anim_trigger:
            self.frame_index = ( self.frame_index + 1 ) % len( self.images )
            self.sprite.image = self.images[ self.frame_index ]

    def update_visuals( self ):
        self.animate()


class Entity( BaseSpriteEntity ):
    """Base Entity class

    Args:
        BaseSpriteEntity ( BaseSpriteEntity ): _description_
    """    
    def __init__( self, name, pos=( 0, 0 ) ):
        super().__init__( name )
        self.set_pos( vec2( pos ) * TILE_SIZE )
        self.player = clientApp().player
        self.y_offset = vec2( 0, self.attrs[ 'y_offset' ] )

        try:
            self.message = self.attrs[ 'message' ]
        except:
            self.message = ''

    def update( self ):
        super().update()
        self.change_layer()

    def change_layer( self ):
        if( self.sprite == None ):
            return
        
        self.sprite.groups()[0].change_layer( self.sprite, self.screen_pos.y )

    # Rect is the actual thing used in the draw call to determine the position
    def update_screenpos( self ):
        super().update_screenpos()

        self.sprite.rect.center = self.screen_pos + self.y_offset

        self.change_layer()

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
        if clientApp().anim_trigger or True: # TODO: ovo podesiti ako se pomakne remote igrač
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
        return        
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

    
    def move( self ): # TODO: Ovdje bi trebalo staviti promjenu pozicije temeljem poruke
        self.pos = clientApp().players_pos[ self.username ]

    def should_think(self) -> bool:
        """Checks whether the entity has behaviour to be called every frame

        Returns:
            bool: Returns true if the entity has defined behaviour in the think function
        """        
        return True

    def think(self):
        self.move()

    def update_visuals( self ):
        super().update_visuals()