from shared import *
from stacked_sprite import *
from random import uniform
from entity import Entity, RemotePlayer
from cache import Cache
from player import Player
import threading
from tilemap import Material, Tile

P = 'player'
K = 'kitty'  # entity
CR = 'circus'

F1, F2, F3, F4, F5, F6, F7 = 'flower1', 'flower2', 'flower3','flower4', 'flower5', 'flower6','flower7'

T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12 = 'tree7', 'tree6', 'tree5', 'tree4', 'tree4', 'tree5', 'tree6', 'tree7', 'tree7', 'tree6', 'tree5', 'tree4'

#C1, C2 = 'car1', 'car2'

B = 'bike'

M = 'movement'

R = 'resource'

C = 'combat'

T = 'tetris'

G = 'globe'

U = 'upgrades'

UI = 'ui'

CH = 'chicken'

CR = 'circus'




MAP = [ 
    [ T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3 ],
    [ T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6 ],
    [ T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9 ],
    [ T1, T6, T7, F1,  0,  0,  0,  0,  0, F2,  0,  0, F1,  0,  0,  0, F7,  0,  0,  0,  0,  0, F6, CH,T11,T10,T12 ],
    [ T2, T8, T3,  0,  0,  0,  0, F7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, F4,  0,  0,  0,  0, F5,T12, T6, T5 ],
    [ T3, T9,T12,  0,  0,  0,  0,  0,  0,  0,  0,  0, T4,  0, F3,  0,  0, F1,  0, F3,  0, F7,  0,  0, T7, T9, T1 ],
    [ T1, T8, T9,T10,  0,  0, T5,  0,  0, F4, T3,  0,  0,  0,  0,  0,  0,  0,  0, T1,  0,  0,  0,  0, T6, T7, T8 ],
    [ T6, T6, T7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, F2,  0, F3,  0,  0,  0, F6,  0, F3,  0,  0,T11,T12, T1 ],
    [ T7, T6, T7, T8,  0,  0,  0, F3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T3, T4, T5, T6 ],
    [ T8, T1, T2, T3, T4,  0,  0,  0,  0,  0, F3,  0, T2,  0,  0,  0,  0, F2,  0,  0,  0,  0,  0,  0,T12, T1, T2 ],
    [ T3, T6, T7, T8,  0,  0, T6,  0,  0,  0,  0,  0,  0,  0, CR,  0,  0,  0,  0,  0,  0,  0,  0, T1, T2, T3, T4 ],
    [ T9, T9,T10,  0,  0,  0,  0, F6,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T8, T9,T10 ],
    [ T10,  0,  0,  0,  0, F5,  0,  0,  0,  0, F4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T2, T3, T4 ],
    [ T4 ,T6, T7,  0,  0,  0, F3,  0,  0,  0,  0, F1, T4,  0, T3,  0,  0,  0,  U,  0,  0, UI,  0,  0, T6, T7, T8 ],
    [ T11,T12, T1, T2,  0,  0,  0,  0,  B,  0,  0,  0,  0,  M,  0,  0, F2,  0,  0,  0,  0,  0,  0,  0,T11,T12, T1 ],
    [ T5, T6, T9,  0, F2,  0,  0,  0,  0,  0,  R,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T6, T7, T8 ],
    [ T1, T9, T2,  0, T7,  0, F1,  0,  0,  0,  0, F6,  0,  P, T1, T2,  0,  0, F3,  0, F7,  0,  0,  0, T9,T10,T11 ],
    [ T6, T9,T10,  0,  0,  0,  0,  0,  0,  0,  0,  K,  K,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T1, T2, T3, T4 ],
    [ T9, T4, T7,  0,  0, F3,  0, F3,  0,  0,  0,  0,  0,  0,  0,  T,  0,  0,  G,  0,  0,  0,  0,  0, T8, T9,T10 ],
    [ T5, T9,T12,  0,  0,  0,  0,  0,  0,  0, F5,  0,  0,  C, F4,  0,  0,  0,  0, F5,  0,  0,  0,  0, T6, T2,T11 ],
    [ T10, T6, T7, T8,  0, F6,  0,  0, F7,  0,  0,  0,  0, F1,  0,  0, F3,  0,  0,  0,  0, F4,  0,  0, T2, T3, T4 ],
    [ T2, T6, T7,  0,  0,  0,  0, F5,  0,  0,  0,T10,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T3, T4, T5, T6 ],
    [ T8,T11,T12, T1,  0, T8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,T12,  0,  0,  0,  0, F4, T6, T7, T8 ],
    [ T9, T9,T10, F2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,T11,  0,  0,  0,  0, F3, T3,T11,T12, T1 ],
    [ T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3 ],
    [ T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6 ],
    [ T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9 ],
 ]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2( len( MAP ), len( MAP[ 0 ] ))
MAP_CENTER = MAP_SIZE / 2


class Scene:
    def __init__( self ):
        self.transform_objects = []
        self.load_scene()
        g.client_app.message.set_message( g.client_app.player.message )
        g.client_app.message.active = True

    def load_scene( self ):
        rand_rot = lambda: uniform( 0, 360 )
        rand_pos = lambda pos: pos + vec2( uniform( -0.25, 0.25 ))

        player_pos = vec2(0)

        for j, row in enumerate( MAP ):
            for i, name in enumerate( row ):
                pos = vec2( i, j ) + vec2( 0.5 )
                print( name, pos )
                if name == 'player':
                    g.client_app.player.offset = pos * TILE_SIZE
                    player_pos = g.client_app.player.offset
                elif name == 'kitty' or name == 'circus' or name == 'movement' or name == 'resource' or name == 'combat' or name == 'tetris' or name == 'globe' or name == 'upgrades' or name == 'ui':
                    Entity( name=name, pos=pos )
                elif str( name ).startswith( 'tree' ) or name == 'bush':
                    TrnspStackedSprite( name=name, pos=rand_pos( pos ), rot=rand_rot() )
                elif name == 'grass' or str( name ).startswith( 'flower' ):
                    StackedSprite( name=name, pos=rand_pos( pos ), rot=rand_rot(),
                                  collision=False )
                elif name == 'sphere':
                    obj = StackedSprite( name=name, pos=rand_pos( pos ), rot=rand_rot() )
                    self.transform_objects.append( obj )
                elif name:
                    StackedSprite( name=name, pos=rand_pos( pos ), rot=rand_rot() )

        print(player_pos)
        material1 = Material("assets/materials/tiles/test_tile.png")
        Tile( material1, player_pos, g.client_app.draw_manager.layer_masks["tile_layer"] )
        Tile( material1, player_pos + vec2( TILE_SIZE, 0 ), g.client_app.draw_manager.layer_masks["tile_layer"] )
        Tile( material1, player_pos + vec2( TILE_SIZE * 2, 0 ), g.client_app.draw_manager.layer_masks["tile_layer"] )
        Tile( material1, player_pos + vec2( TILE_SIZE * 3, 0 ), g.client_app.draw_manager.layer_masks["tile_layer"] )

        for pl in g.client_app.players_pos: 
            RemotePlayer( 'remote_player', g.client_app.players_pos[ pl ], pl )

    def get_closest_object_to_player( self ):
        closest = sorted( g.client_app.transparent_objects, key=lambda e: e.dist_to_player )
        closest[ 0 ].alpha_trigger = True
        closest[ 1 ].alpha_trigger = True

    def transform( self ):
        for obj in self.transform_objects:
            obj.rot = 30 * g.client_app.time

    def update( self ):
        self.get_closest_object_to_player()
        self.transform()




def run_in_thread( func, args=None, kwargs=None, callback=None ):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    def wrapped_func():
        result = func( *args, **kwargs )
        if callback:
            callback()

    thread = threading.Thread( target=wrapped_func )
    thread.start()
    return thread
        
        

class LoadingScene:
    def __init__( self ):
        self.font = pg.font.Font( "assets/PressStart2P-Regular.ttf", 16 )
        self.progress = 0
        self.messages = [ 
            'Loading assets...',
            'Setting up player...',
            'Initializing game...',
            'Checking the weather...',
            'Thinking about the meaning of life...',
            'Resting...',
            'Contemplating life decisions...',
            'Talking to myself...',
            'Drinking coffee...',
            "Starring at my mobile...",
            "Doing nothing...",
            "A little bit more nothing...",
            'Almost done...',
            'Or not...',
            'Maybe...',
            "I have no idea what I'm doing...",
            
        ]
        self.bar_width = int( WIDTH / 3.0 )
        self.bar_height = int( HEIGHT / 56.33 )
        self.MAX = len( STACKED_SPRITE_ATTRS )
        self.done = False
        g.client_app.cache = Cache()
        g.client_app.cache.cache_entity_sprite_data()
        self.stacked_sprite_iterator = g.client_app.cache.cache_stacked_sprite_data()

    def done_cache( self ):
        self.done = True
        

    def update( self ):
        counter = next( self.stacked_sprite_iterator, 'done' )
        if counter == 'done':
            self.done_cache()
        
        if self.done:
            # Switch to the game scene after loading is complete
            g.client_app.player = Player()
            g.client_app.scene = Scene()
        else:
            # Simulate loading progress
            self.progress = g.client_app.done_counter / self.MAX * len( self.messages )

        print(self.progress)


    def draw( self ):
        #client_app.screen.fill( BG_COLOR )
        self.bg_img = pg.image.load( 'assets/images/png' )
        self.bg_img = pg.transform.smoothscale( self.bg_img, g.client_app.screen.get_size() )
        g.client_app.screen.blit( self.bg_img, self.bg_img.get_rect() )
        screen_center_x = g.client_app.screen.get_width() // 2
        screen_center_y = g.client_app.screen.get_height() // 100 * 85

        # Display the current message based on progress
        current_message_index = min( int( self.progress ), len( self.messages ) - 1 )
        msg = self.messages[ current_message_index ]
        text = self.font.render( msg, True, ( 0, 0, 0 ))
        text_rect = text.get_rect( center=( screen_center_x, screen_center_y + 80 ))
        g.client_app.screen.blit( text, text_rect )

        # Draw the progress bar background
        bar_bg_rect = pg.Rect( 0, 0, self.bar_width, self.bar_height )
        bar_bg_rect.center = ( screen_center_x, screen_center_y + 40 )
        pg.draw.rect( g.client_app.screen, ( 204, 239, 253 ), bar_bg_rect )

        # Draw the progress bar
        progress_width = int( self.progress / len( self.messages ) * self.bar_width )
        bar_rect = pg.Rect( 0, 0, progress_width, self.bar_height )
        bar_rect.midleft = bar_bg_rect.midleft
        pg.draw.rect( g.client_app.screen, ( 221, 220, 79 ), bar_rect )










