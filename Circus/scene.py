from importlib import import_module
from quests.test_quest import PositionQuest
from quest import Quest
from npc import NPCBase
from shared import *
from stacked_sprite import *
from random import uniform
from entity import Entity, RemotePlayer
from cache import Cache
from player import Player
import threading
from tilemap import Tile, MapData
from materialsystem import Material
import json
from interface import Interface
from interface import BarInterface
from dialogue import Dialogue
from chat import Chat

vartypes = {
    "vec2": vec2
}

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

AN = 'animacija'

DR = 'deer'

WALL = 'wall'

DOG = 'dog'

MAP_OLD = [
    [ T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3 ],
    [ T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6 ],
    [ T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9 ],
    [ T1, T6, T7, F1,  0,  0,  0,  0,  0, F2,  0,  0, F1,  0,  0,  0, F7,  0,  0,  0,  0,  0, F6, CH,T11,T10,T12 ],
    [ T2, T8, T3,  0,  0,  0,  0, F7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, F4,  0,  0,  0,  0, F5,T12, T6, T5 ],
    [ T3, T9,T12,  0,  0,  0,  0,  0,  0,  0,  0,  0, T4,  0, F3,  0,  0, F1,  0, F3,  0, F7,  0,  0, T7, T9, T1 ],
    [ T1, T8, T9,T10,  0,  0, T5,  0,  0, F4, T3,  0,  0,  0,  0,  0,  0,  0,  0, T1,  0,  0,  0,  0, T6, T7, T8 ],
    [ T6, T6, T7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, F2,  0, F3,  0,  0,  0, F6,  0, F3,  0,  0,T11,T12, T1 ],
    [ T7, T6, T7, T8,  0,  0,  0, F3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T3, T4, T5, T6 ],
    [ T8, T1, T2, T3, T4,  0,  0,  0,  0,  0, 0,  0, T2,  0,  0,  0,  0, F2,  0,  0,  0,  0,  0,  0,T12, T1, T2 ],
    [ T3, T6, T7, T8,  0,  0, T6,  0,  0,  0,  0,  0,  0,  0, CR,  0,  0,  0,  0,  0,  0,  0,  0, T1, T2, T3, T4 ],
    [ T9, T9,T10,  0,  0,  0,  0, F6,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T8, T9,T10 ],
    [ T10,  0,  0,  0,  0, F5,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T2, T3, T4 ],
    [ T4 ,T6, T7,  0,  0,  0, F3,  0,  0,  0,  0, F1, T4,  0, T3,  0,  0,  0,  U,  0,  0, UI,  0,  0, T6, T7, T8 ],
    [ T11,T12, T1, T2,  0,  0,  0,  0,  B,  0,  0,  0,  0,  M,  0,  0, F2,  0,  0,  0,  0,  0,  0,  0,T11,T12, T1 ],
    [ T5, T6, T9,  0, F2,  0,  0,  0,  0,  0,  R,  DOG,  0,  DR,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T6, T7, T8 ],
    [ T1, T9, T2,  0, T7,  0, 0,  0,  0,  0,  0, F6,  AN,  P, T1, T2,  0,  0, F3,  0, F7,  0,  0,  0, T9,T10,T11 ],
    [ T6, T9,T10,  0,  0,  0,  0,  0,  0,  0,  0,  K,  K,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T1, T2, T3, T4 ],
    [ T9, T4, T7,  0,  0, 0,  0, F3,  0,  0,  0,  0,  0,  0,  0,  T,  0,  0,  G,  0,  0,  0,  0,  0, T8, T9,T10 ],
    [ T5, T9,T12,  0,  0,  0,  0,  0,  0,  0, F5,  0,  0,  C, F4,  0,  0,  0,  0, F5,  0,  0,  0,  0, T6, T2,T11 ],
    [ T10, T6, T7, T8,  0, 0,  0,  0, F7,  0,  0,  0,  0, F1,  0,  0, F3,  0,  0,  0,  0, F4,  0,  0, T2, T3, T4 ],
    [ T2, T6, T7,  0,  0,  0,  0, 0,  0,  0,  0,T10,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, T3, T4, T5, T6 ],
    [ T8,T11,T12, T1,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,T12,  0,  0,  0,  0, F4, T6, T7, T8 ],
    [ T9, T9,T10, F2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,T11,  0,  0,  0,  0, F3, T3,T11,T12, T1 ],
    [ T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3 ],
    [ T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6 ],
    [ T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9,T10,T11,T12, T1, T2, T3, T4, T5, T6, T7, T8, T9 ],
]

MAP_EMPTY = [ 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, P, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
]

ESSAY = """

Dummy text: Its function as a filler or as a tool for comparing the visual impression of different typefaces

Dummy text is text that is used in the publishing industry or by web designers to occupy the space which will later be filled with 'real' content. This is required when, for example, the final text is not yet available. Dummy text is also known as 'fill text'. It is said that song composers of the past used dummy texts as lyrics when writing melodies in order to have a 'ready-made' text to sing with the melody. Dummy texts have been in use by typesetters since the 16th century.
The usefulness of nonsensical content

Dummy text is also used to demonstrate the appearance of different typefaces and layouts, and in general the content of dummy text is nonsensical. Due to its widespread use as filler text for layouts, non-readability is of great importance: human perception is tuned to recognize certain patterns and repetitions in texts. If the distribution of letters and 'words' is random, the reader will not be distracted from making a neutral judgement on the visual impact and readability of the typefaces (typography), or the distribution of text on the page (layout or type area). For this reason, dummy text usually consists of a more or less random series of words or syllables. This prevents repetitive patterns from impairing the overall visual impression and facilitates the comparison of different typefaces. Furthermore, it is advantageous when the dummy text is relatively realistic so that the layout impression of the final publication is not compromised.
Incomprehensibility or readability? That is the question.

"""


# Koju map datoteku da ucita
# koristite SCENE_MAPNAME = "" ako ne zelite da se ista ucita
SCENE_MAPNAME = "new" # new.map

# Koji map array da se ucita ( gledaj gore )
# MAP_EMPTY samo pozicionira igraca
MAP = MAP_EMPTY 

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2( len( MAP ), len( MAP[ 0 ] ))
MAP_CENTER = MAP_SIZE / 2

class Scene:
    def __init__( self ):
        self.transform_objects = []
        self.done = False
        self.load_scene(SCENE_MAPNAME)

    def load_scene( self, mapname: str ):
        self.load_map_file( mapname )

        #clientApp().player.questDialogue.set_message(ESSAY)
        #clientApp().player.questDialogue.show()
        Interface('hud')
        BarInterface('health-bar')
        BarInterface('mana-bar')

        rand_rot = lambda: uniform( 0, 360 )
        rand_pos = lambda pos: pos + vec2( uniform( -0.25, 0.25 ))

        player_pos = vec2(0)
        

        clientApp().chat.show()

        for j, row in enumerate( MAP ):
            for i, name in enumerate( row ):
                pos = vec2( i, j ) + vec2( 0.5 )
                if name == 'player':
                    player_pos = pos * TILE_SIZE
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

        for pl in clientApp().players_pos: 
            if( pl != clientApp().username ):
                RemotePlayer( 'remote_player', clientApp().players_pos[ pl ]['position'], pl )
            # U edge case-u da je vec 0 nekako, ovo nece raditi
            # But it will do for now
            elif( clientApp().players_pos[ pl ]['position'] != vec2(0) ):
                player_pos = clientApp().players_pos[ pl ]['position']
        
        clientApp().player.offset = player_pos

        self.done = True
            

    def load_map_file( self, mapname ):
        if( len(mapname) <= 0 ):
            return

        if( mapname.endswith(".map") ):
            mapname = mapname.replace(".map", "")

        mapObj = MapData("assets/maps/" + mapname + ".map")

        for layerName in mapObj.layers.keys():
            layer = mapObj.layers[layerName]
            if layerName.startswith("tiles_"):
                layerData = layer["data"]
                for posStr in layerData:
                    pos = strToVec(posStr)
                    material: Material = clientApp().material_system.register_material( "assets/" + layerData[posStr] )
                    Tile( material, pos * TILE_SIZE, clientApp().draw_manager.layer_masks["tile_layer"] )
            elif layerName.startswith("entities_"):
                layerData = layer["data"]
                for key in layerData:
                    attr:dict = layerData[key]

                    startIndex = max(0, key.find("_")+1)
                    entType = key[startIndex::]
                    classStr: str = entType

                    entClass = None
                    try:
                        module_path, class_name = classStr.rsplit('.', 1)
                        module = import_module(module_path)
                        entClass = getattr(module, class_name)
                    except (ImportError, AttributeError) as e:
                        raise ImportError(classStr)
                    
                    name = "kitty"

                    if( "name" in attr ):
                        name = attr["name"]
                    
                    newEnt = entClass(name)
                    if( "pos" in attr ):
                        newEnt.set_pos( strToVec(attr["pos"]) * TILE_SIZE )
                    
                    try:
                        newEnt.load_info_from_map(attr)
                    except Exception as e:
                        pass

                    print(newEnt)

    def get_closest_object_to_player( self ):
        closest = sorted( clientApp().transparent_objects, key=lambda e: e.dist_to_player )
        if( len(closest) > 0 ):
            closest[ 0 ].alpha_trigger = True
            closest[ 1 ].alpha_trigger = True

    def transform( self ):
        for obj in self.transform_objects:
            obj.rot = 30 * clientApp().time

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
        clientApp().cache = Cache()
        clientApp().cache.cache_entity_sprite_data()
        self.stacked_sprite_iterator = clientApp().cache.cache_stacked_sprite_data()

    def done_cache( self ):
        self.done = True
        
    def update( self ):
        counter = next( self.stacked_sprite_iterator, 'done' )
        if counter == 'done':
            self.done_cache()
        
        if self.done:
            # Switch to the game scene after loading is complete
            clientApp().set_local_player( Player() )
            clientApp().set_chat( Chat() )
            clientApp().set_active_scene( Scene() )
            
        else:
            # Simulate loading progress
            self.progress = clientApp().done_counter / self.MAX * len( self.messages )

        print(self.progress)


    def draw( self ):
        #client_app.screen.fill( BG_COLOR )
        self.bg_img = pg.image.load( 'assets/images/splash.png' )
        self.bg_img = pg.transform.smoothscale( self.bg_img, clientApp().screen.get_size() )
        clientApp().screen.blit( self.bg_img, self.bg_img.get_rect() )
        screen_center_x = clientApp().screen.get_width() // 2
        screen_center_y = clientApp().screen.get_height() // 100 * 85

        # Display the current message based on progress
        current_message_index = min( int( self.progress ), len( self.messages ) - 1 )
        msg = self.messages[ current_message_index ]
        text = self.font.render( msg, True, ( 0, 0, 0 ))
        text_rect = text.get_rect( center=( screen_center_x, screen_center_y + 80 ))
        clientApp().screen.blit( text, text_rect )

        # Draw the progress bar background
        bar_bg_rect = pg.Rect( 0, 0, self.bar_width, self.bar_height )
        bar_bg_rect.center = ( screen_center_x, screen_center_y + 40 )
        pg.draw.rect( clientApp().screen, ( 204, 239, 253 ), bar_bg_rect )

        # Draw the progress bar
        progress_width = int( self.progress / len( self.messages ) * self.bar_width )
        bar_rect = pg.Rect( 0, 0, progress_width, self.bar_height )
        bar_rect.midleft = bar_bg_rect.midleft
        pg.draw.rect( clientApp().screen, ( 221, 220, 79 ), bar_rect )










