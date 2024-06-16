import pygame as pg
import sys
import re

vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = vec2( 800, 450 ) #vec2( 1600, 900 )
CENTER = H_WIDTH, H_HEIGHT = RES // 2
TILE_SIZE = 250  #

PLAYER_SPEED = 0.4
PLAYER_ROT_SPEED = 0.0015

BG_COLOR = ( 9, 20, 38 ) #'white'  # olivedrab
NUM_ANGLES = 8  # multiple of 360 -> 24, 30, 36, 40, 45, 60, 72, 90, 120, 180

pg.mixer.init()
pg.mixer.music.load( "assets/bgm/bgm.ogg" )
pg.mixer.music.play( loops=-1 )


CREDITS = """
CREDITS

Author: 
Markus Schatten
ChatGPT

Art:
Karen Arnold - https://www.publicdomainpictures.net/en/view-image.php?image=282526&picture=circus-tent
Studios SoulAres - https://soulares.itch.io/
deadpixl - https://itch.io/jam/gameshell/rate/378133
neogeodev - https://wiki.neogeodev.org/index.php?title=File:Wh2earth.gif
anokolisa - https://anokolisa.itch.io/dungeon-crawler-pixel-art-asset-pack
BlueWillow
Markus Schatten
StanislavPetrovV
Mo Enen Voxel Collection

Engine and programming:
StanislavPetrovV - https://github.com/StanislavPetrovV/SpriteStacking
Markus Schatten
ChatGPT

Music:
Julius Fucik - https://opengameart.org/content/entry-of-the-gladiators-march-of-triumph

Copyright: 
Artificial Intelligence Laboratory
Faculty of Organization and Informatics
University of Zagreb
2023.



"""




# entity settings
ENTITY_SPRITE_ATTRS = {
    'player': {
        'path': 'assets/entities/player/ringmaster.png',
        'mask_path': 'assets/entities/player/mask.png',
        'num_layers': 16,
        'scale': 1,
        'y_offset': 0,
    },
    'remote_player': {
        'path': 'assets/entities/player/ringmaster.png',
        'mask_path': 'assets/entities/player/mask.png',
        'num_layers': 16,
        'scale': 1,
        'y_offset': 0,
    },
    'kitty': {
        'path': 'assets/entities/cats/kitty.png',
        'num_layers': 8,
        'scale': 0.8,
        'y_offset': -20,
    },
    'circus': {
        'path': 'assets/entities/circus/circus_tent.png',
        'num_layers': 1,
        'scale': 6.0,
        'y_offset': -20,
    },
    'explosion': {
        'num_layers': 7,
        'scale': 1.0,
        'path': 'assets/entities/explosion/explosion.png',
        'y_offset': 50,
    },
    'bullet': {
        'num_layers': 1,
        'scale': 0.4,
        'path': 'assets/entities/bullet/bullet.png',
        'y_offset': 50,
    },
    'movement': {
        'path': 'assets/entities/movement/movement.png',
        'num_layers': 74,
        'scale': 1,
        'y_offset': 20,
    },
    'resource': {
        'path': 'assets/entities/resource/resource-crafting.png',
        'num_layers': 16,
        'scale': 1,
        'y_offset': 20,
    },
    'combat': {
        'path': 'assets/entities/combat/combat.png',
        'num_layers': 69,
        'scale': 1,
        'y_offset': 20,
    },
    'tetris': {
        'path': 'assets/entities/tetris/tetris.png',
        'num_layers': 239,
        'scale': 1,
        'y_offset': 20,
    },
    'globe': {
        'path': 'assets/entities/globe/globe.png',
        'num_layers': 86,
        'scale': 2,
        'y_offset': 20,
    },
    'upgrades': {
        'path': 'assets/entities/upgrades/upgrades.png',
        'num_layers': 24,
        'scale': 1,
        'y_offset': 20,
    },
    'ui': {
        'path': 'assets/entities/ui/ui.png',
        'num_layers': 7,
        'scale': 1,
        'y_offset': 20,
    },
}

# stacked sprites settings
'''mask_layer - index of the layer from which we get the mask for collisions 
and is also cached for all angles of the object, set manually or by default 
equal to num_layer // 2'''

STACKED_SPRITE_ATTRS = {
    'tree4': {
        'path': 'assets/stacked_sprites/tree4.png',
        'num_layers': 46,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
        'outline': 10,
    },
    'tree5': {
        'path': 'assets/stacked_sprites/tree5.png',
        'num_layers': 60,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
        'outline': 10,
    },
    'tree6': {
        'path': 'assets/stacked_sprites/tree6.png',
        'num_layers': 46,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
        'outline': 10,
    },
    'tree7': {
        'path': 'assets/stacked_sprites/tree7.png',
        'num_layers': 48,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
        'outline': 10,
    },
    'flower1': {
        'path': 'assets/stacked_sprites/flower1.png',
        'num_layers': 9,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower2': {
        'path': 'assets/stacked_sprites/flower2.png',
        'num_layers': 8,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower3': {
        'path': 'assets/stacked_sprites/flower3.png',
        'num_layers': 10,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower4': {
        'path': 'assets/stacked_sprites/flower4.png',
        'num_layers': 9,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower5': {
        'path': 'assets/stacked_sprites/flower5.png',
        'num_layers': 8,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower6': {
        'path': 'assets/stacked_sprites/flower6.png',
        'num_layers': 9,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower7': {
        'path': 'assets/stacked_sprites/flower7.png',
        'num_layers': 9,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'animacija': {
        'path': 'assets/stacked_sprites/animacija.png',
        'num_layers': 4,
        'animation': {
            'num_frames': 4,
            'animation_speed': 2,
            'sequence': {
                'idle': {
                    'seq': [ 0, 1, 2, 3 ],
                    'looping': True,
                },
            },
        },
        'scale': 8,
        'y_offset': -8,
        'mask_layer': 1,
        'outline': False,
    },
    'wall': {
        'path': 'assets/stacked_sprites/wall.png',
        'num_layers': 8,
        'scale': 16,
        'y_offset': -30,
        'mask_layer': 4,
        'outline': True,
    },
    'deer': {
        'path': 'assets/stacked_sprites/deer.png',
        'num_layers': 27,
        'animation': {
            'num_frames': 4,
            'animation_speed': 10,
            'sequence': {
                'idle': {
                    'seq': [ 0, 1, 2, 3 ],
                    'looping': True,
                },
            },
        },
        'scale': 8,
        'y_offset': -100,
        'mask_layer': 1,
        'outline': False,
    },
    'dog': {
        'path': 'assets/stacked_sprites/dog.png',
        'num_layers': 27,
        'animation': {
            'num_frames': 19,
            'animation_speed': 6,
            'sequence': {
                'idle': {
                    'seq': [ 0, 1, 2, 3, 4, 5, 6, 7 ],
                    'looping': True,
                },
                'walk': {
                    'seq': [ 8, 9, 10, 11 ],
                    'looping': True,
                },
                'run': {
                    'seq': [ 12, 13, 14, 15, 16, 17, 18 ],
                    'looping': True,
                },
            },
        },
        'scale': 8,
        'y_offset': -100,
        'mask_layer': 8,
        'outline': False,
    },
    'chicken': {
        'path': 'assets/stacked_sprites/chicken.png',
        'num_layers': 15,
        'scale': 10,
        'y_offset': 10,
        'message': CREDITS,
    },
    'bike': {
        'path': 'assets/stacked_sprites/bike.png',
        'num_layers': 14,
        'num_frames': 1,
        'scale': 10,
        'y_offset': 10,
    },
}



# UI settings

INTERFACE_ATTRS = {
    'hud': {
        'path': 'assets/images/hud.png',
        'pos': (0, 0),
        'size': (800, 450),
        'z': 0,
        'interactibles': {
            'Ability1': {
                'x': 240,
                'y': 352,
                'width': 24,
                'height': 24,
                'interaction': 'a'
                }
        }
    }
}

# NOTE NOTE: Only use this with strings that *we* made, not something the user can edit
#            and ESPECIALLY not something an user can send to others
#            This can cause unwanted code execution

def getVarFromString( string: str ):
    match = re.search("^(.+)\((.*)\)$", string)

    type = match.group(1)
    args = match.group(2)
    
    try:
        val = eval(type + "(" + args + ")" )
    except:
        val = string
    
    return val

class _globals:
    app = None

def clientApp():
    return _globals.app

def setClientApp( app ):
    _globals.app = app

def strToVec(string: str) -> vec2:
    ret = string
    ret = ret.replace("Vector2", "")
    ret = ret.replace("vec2", "")
    ret = ret.replace("(","")
    ret = ret.replace(")","")
    ret = ret.replace(" ","")
    strVals: list = ret.split(",")
    return vec2(float(strVals[0]),float(strVals[1]))