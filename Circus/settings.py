import pygame as pg
import sys

vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = vec2( 800, 450 ) #vec2( 1600, 900 )
CENTER = H_WIDTH, H_HEIGHT = RES // 2
TILE_SIZE = 250  #

PLAYER_SPEED = 0.4
PLAYER_ROT_SPEED = 0.0015

BG_COLOR = ( 9, 20, 38 ) #'white'  # olivedrab
NUM_ANGLES = 72  # multiple of 360 -> 24, 30, 36, 40, 45, 60, 72, 90, 120, 180

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
        'message':"""A lot of players are in there for the community. 

Social and multiplayer game mechanics include cooperative and competitive gameplay, MMO systems, communication tools, trading between players, and guilds which foster social interaction within the game.""",
    },
    'circus': {
        'path': 'assets/entities/circus/circus_tent.png',
        'num_layers': 1,
        'scale': 6.0,
        'y_offset': -20,
        'message':"""Let me tell you about the relationship between mechanics and game genres.

Different combinations of game mechanics create distinct gameplay experiences, leading to various genres.
For example: Role-playing games typically feature character progression, branching narratives, and resource management mechanics.

Or another example: First-person shooters focus on movement, ranged combat, and often include multiplayer mechanics.

Mechanics as the foundation of game experiences. The choice and implementation of game mechanics directly impact the overall feel and enjoyment of a game.

Designers often mix and match mechanics from different genres to create unique experiences or to innovate within a genre.

Game mechanics are different on different platforms.

On Consoles, game mechanics often designed with console-specific controllers in mind; can leverage unique features of consoles ( e.g., motion controls ).

PCs offer more control options ( e.g., mouse and keyboard ) and enable more complex mechanics, such as in strategy or simulation games.

Mobile devices feature a touchscreen interface which leads to simplified mechanics and controls, focus on shorter, more casual experiences.

VR/AR systems provide immersive experiences that utilize motion controls and spatial awareness as well as new mechanics unique to these platforms ( e.g., hand-tracking ).

If you want to implement cross-platform games you need to consider design choices. Designers need to balance and adapt mechanics to ensure a consistent experience across different platforms.
    
    
Some of the basic elements of game mechanics design include:

- Balancing gameplay: Ensuring that no single mechanic or strategy is overpowered, creating a fair and engaging experience for players.
- Player agency: Designing mechanics that allow players to make meaningful choices and have an impact on the game world.
- Feedback loops: Positive and negative feedback loops help maintain game balance, reinforce player actions, and provide dynamic gameplay experiences.
- Reward systems: Encouraging player engagement and motivation through rewards, such as new abilities, in-game items, or story progression.
- Design principles: Keeping mechanics clear, consistent, and easy to learn; ensuring they provide depth and variety for players.
- Iterative design: Continuously refining and improving mechanics based on playtesting and player feedback.

2D games are special in terms of algorithms and used game mechanics.

2D games are games that take place in a two-dimensional plane, often featuring sprite-based graphics and side-scrolling or top-down views.

Algorithms govern the behavior of game elements, enabling complex interactions and dynamic gameplay.
    
Most important algorithms that influence 2D game mechanics include:
- Collision detection: Algorithm used to determine when game objects collide, essential for various mechanics like movement, combat, and physics.

- Pathfinding: Algorithms that help non-player characters ( NPCs ) and objects navigate the game environment, essential for AI behavior and movement mechanics.

- AI behavior: Algorithms that dictate how NPCs and enemies respond to player actions and their environment, adding depth and challenge to the gameplay.

- Physics simulations: Algorithms that model real-world physics, used in various mechanics like object interactions, projectiles, and fluid dynamics
    
- Two-dimensional space: Games are confined to a 2D plane, using X and Y coordinates

- Sprite-based graphics: 2D images or animations used to represent characters, objects, and environments

- Scrolling backgrounds: Backgrounds that move as the player navigates through the game, creating a sense of depth and movement

Typical genres of 2D games are:

- Platformers: Games where players navigate through levels by jumping between platforms and overcoming obstacles.
 -Shoot 'em ups: Players control a character or vehicle and shoot at waves of enemies while dodging obstacles and projectiles.
 -Fighting games: Players engage in one-on-one combat with a variety of characters, each with unique abilities and movesets.
- Puzzle games: Players solve puzzles by manipulating objects, recognizing patterns, or using logic and strategy.

Examples of game mechanics and algorithms in 2D games:

- Platformers: Precise character movement, variable jump heights, double jumps, wall jumps, and moving platforms.
- Shoot 'em ups: Bullet patterns, power-ups, screen-clearing bombs, and enemy spawning algorithms.
- Fighting games: Combo systems, special moves, blocking, and counters.
- Puzzle games: Tile-matching, object manipulation, physics-based challenges, and procedural puzzle generation.
- Common algorithms: Collision detection, pathfinding, AI behavior, and physics simulations.

On the other hand 3D games are different. These are games that take place in a three-dimensional space, often featuring polygonal graphics and a variety of camera perspectives.

Algorithms enable complex interactions and dynamic gameplay in a 3D environment. Some of these are:

- Collision detection: Algorithm used to determine when game objects collide in 3D space, essential for various mechanics like movement, combat, and physics.
- Pathfinding: Algorithms that help NPCs and objects navigate 3D environments, essential for AI behavior and movement mechanics
- AI behavior: Algorithms that dictate how NPCs and enemies respond to player actions and their environment, adding depth and challenge to the gameplay
- Physics simulations: Algorithms that model real-world physics, used in various mechanics like object interactions, projectiles, and fluid dynamics

Basic characteristics of 3D games are:

- Three-dimensional space: Games take place in a 3D environment, using X, Y, and Z coordinates.
- Polygonal graphics: 3D models and textures used to represent characters, objects, and environments.
- Camera perspectives: Players view the game world from different angles, such as first-person, third-person, or top-down perspectives.

Typical genres of 3D Games are:

- First-person shooters: Players control a character from a first-person perspective, focusing on ranged combat and often including multiplayer mechanics.
- Action-adventure games: Players navigate a 3D world, solving puzzles, engaging in combat, and completing quests to progress the story.
- Role-playing games: Players develop characters by leveling up, acquiring new abilities, and making choices that impact the game world and narrative.
- Racing games: Players control vehicles and compete against other racers on various tracks, often featuring realistic physics and handling.

Some examples of gameplay mechanics and algorithms in 3D games:

- First-person shooters: Weapon handling, cover systems, health and damage systems, and multiplayer mechanics.
- Action-adventure games: Environmental puzzles, context-sensitive actions, and branching     narratives.
- Role-playing games: Character progression, branching dialogue options, moral choices, and quest systems.
- Racing games: Vehicle handling, track design, AI opponents, and various race modes.
- Common algorithms: Collision detection, pathfinding, AI behavior, and physics simulations.

2D and 3D games in comparison have their advantages and disadvantages: 2D games often have simpler graphics and controls, while 3D games offer more immersive and visually appealing experiences. 

In terms of complexity and development time: 3D games typically require more resources and time to develop, but can offer richer gameplay experiences.

In the future we might see some interesting new developments in game mechanics. For example:

- Emerging technologies: Virtual reality ( VR ), augmented reality ( AR ), and artificial intelligence ( AI ) provide new opportunities for innovative game mechanics.
- Evolving player expectations: As the gaming audience grows, players demand more complex, engaging, and diverse game mechanics.
- Cross-genre experiments: Designers continue to blend and adapt mechanics from various genres to create unique gaming experiences.

In the end, I give you a few secret best practices in game mechanics design:

- Playtesting: Regularly testing game mechanics to identify issues, gather feedback, and refine gameplay experiences.
- Iterative design: Continuously refining and improving mechanics based on playtesting and player feedback.
- Player feedback: Actively seeking input from players to ensure game mechanics are engaging, balanced, and enjoyable.
- Prototyping: Creating simplified versions of game mechanics to test their functionality and feasibility before full-scale implementation.
   """,
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
        'message':"""This is our movement performer. 

Movement mechanics are different types of movement mechanics, such as walking, running, jumping, climbing, swimming, and flying, allow players to navigate the game world. 

And now move, move, move!!!""",
    },
    'resource': {
        'path': 'assets/entities/resource/resource-crafting.png',
        'num_layers': 16,
        'scale': 1,
        'y_offset': 20,
        'message':"""And here is our master craftsman! 

This is a special type of resource management mechanic.

Other types include inventory systems, gathering resources, trading, the afore mentioned crafting and economics which govern the acquisition and use of in-game items and resources.""",
    },
    'combat': {
        'path': 'assets/entities/combat/combat.png',
        'num_layers': 69,
        'scale': 1,
        'y_offset': 20,
        'message':"""And here for some combat mechanics. 

There are multiple types of combat mechanics including melee combat, ranged combat, magic systems, and stealth mechanics which provide various ways for players to engage in battles and confrontations- 

If you use the up arrow you can see a ranged combat mechanic.""",
    },
    'tetris': {
        'path': 'assets/entities/tetris/tetris.png',
        'num_layers': 239,
        'scale': 1,
        'y_offset': 20,
        'message':"""How about a puzzle? 

Physics-based puzzles, logic puzzles, pattern recognition, and environmental manipulation challenge players' problem-solving skills.""",
    },
    'globe': {
        'path': 'assets/entities/globe/globe.png',
        'num_layers': 86,
        'scale': 2,
        'y_offset': 20,
        'message':"""Do you want to explore the world? 

Exploration game mechanichs include open-world exploration, procedurally generated worlds, non-linear level design, and hidden areas encourage players to discover new locations and secrets.""",
    },
    'upgrades': {
        'path': 'assets/entities/upgrades/upgrades.png',
        'num_layers': 24,
        'scale': 1,
        'y_offset': 20,
        'message':"""And here is the upgradable trio!!! They are quite fun!

Character progression like leveling up, skill trees, ability unlocks, and equipment upgrades allow players to develop and customize their characters.""",
    },
    'ui': {
        'path': 'assets/entities/ui/ui.png',
        'num_layers': 7,
        'scale': 1,
        'y_offset': 20,
        'message':"""Another important game mechanic is related to the user interface and controls. 

It might include  HUD elements, camera perspectives, control schemes, and accessibility options that ensure that players can effectively interact with the game.""",
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
        'num_frames': 1,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
    },
    'tree5': {
        'path': 'assets/stacked_sprites/tree5.png',
        'num_layers': 60,
        'num_frames': 1,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
    },
    'tree6': {
        'path': 'assets/stacked_sprites/tree6.png',
        'num_layers': 46,
        'num_frames': 1,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
    },
    'tree7': {
        'path': 'assets/stacked_sprites/tree7.png',
        'num_layers': 48,
        'num_frames': 1,
        'scale': 8,
        'y_offset': -130,
        'transparency': True,
        'mask_layer': 3,
    },
    'flower1': {
        'path': 'assets/stacked_sprites/flower1.png',
        'num_layers': 9,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower2': {
        'path': 'assets/stacked_sprites/flower2.png',
        'num_layers': 8,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower3': {
        'path': 'assets/stacked_sprites/flower3.png',
        'num_layers': 10,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower4': {
        'path': 'assets/stacked_sprites/flower4.png',
        'num_layers': 9,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower5': {
        'path': 'assets/stacked_sprites/flower5.png',
        'num_layers': 8,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower6': {
        'path': 'assets/stacked_sprites/flower6.png',
        'num_layers': 9,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'flower7': {
        'path': 'assets/stacked_sprites/flower7.png',
        'num_layers': 9,
        'num_frames': 1,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 3,
        'outline': False,
    },
    'animacija': {
        'path': 'assets/stacked_sprites/animacija.png',
        'num_layers': 4,
        'num_frames': 4,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 1,
        'outline': False,
    },
    'deer': {
        'path': 'assets/stacked_sprites/deer.png',
        'num_layers': 27,
        'num_frames': 4,
        'animation_speed': 10,
        'scale': 8,
        'y_offset': 10,
        'mask_layer': 1,
        'outline': False,
    },
    'chicken': {
        'path': 'assets/stacked_sprites/chicken.png',
        'num_layers': 15,
        'num_frames': 1,
        'scale': 10,
        'y_offset': 10,
        'message':'''You have found the Easterchick!!! Go to the professor in private and say the magic words: 

MAMA SC!!!
---------------------------------------
---------------------------------------
---------------------------------------
---------------------------------------
---------------------------------------
---------------------------------------
''' + CREDITS
    },
    'bike': {
        'path': 'assets/stacked_sprites/bike.png',
        'num_layers': 14,
        'num_frames': 1,
        'scale': 10,
        'y_offset': 10,
    },
}




