import copy
import math
from pygame import Rect, Surface
from shared import *
import os

class MapData(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height

class Layer(object):
	def __init__( self, layerIndex, mapObject ):
		#Layer index from tiled map
		self.layerIndex = layerIndex
		
		#Create gruop of tiles for this layer
		self.tiles = pg.sprite.Group()
		
		#Create tiles in the right position for each layer
		for x in range(self.mapObject.width):
			for y in range(self.mapObject.height):
				tile = self.mapObject.get_tile(x, y, self.layerIndex)
				self.tiles.add( tile )
		# Tile(image = img, x = (x * self.mapObject.tilewidth), y = (y * self.mapObject.tileheight))

	#Draw layer
	def draw( self, screen ):
		self.tiles.draw(screen)

# Base class for anything that is within the world
# Handles displaying the object on the screen based on a given viewpoint
# Viewpoint can be any class with an offset and angle
class WorldObject:
	def __init__( self, pos ):
		self.pos = vec2( pos )
		self.screen_pos = vec2( 0 )
		self.screen_ang = 0
		self.viewpoint = None

	def update( self ):
		self.calculate_viewpoint_position()

	def calculate_viewpoint_position( self ):
		view_pos = self.pos - self.viewpoint.offset
		view_pos = view_pos.rotate_rad( self.viewpoint.angle )
		self.screen_pos = view_pos + CENTER

		self.screen_ang = -math.degrees( self.viewpoint.angle )

class Material:
	def __init__( self, file: str ):
		if( os.path.isfile(file) ):
			self.image: Surface = pg.image.load( file )
		else:
			self.image: Surface = pg.image.load( "assets/materials/missing.png" )

#Tile class with an image, x and y
class Tile( pg.sprite.Sprite, WorldObject ):
	def __init__( self, material: Material, pos, group ):
		# TODO: Da li da uzimamo direktan pos ili
		# da uzimamo Tile pos pa onda izračunamo konkretan pos
		self.group = group
		super().__init__( group )
		super( pg.sprite.Sprite, self ).__init__( pos )

		# Temporary
		self.viewpoint = g.client_app.player

		self.material: Material = material
		size = material.image.get_size()
		self.resize = vec2( TILE_SIZE / size[0], TILE_SIZE / size[1] )
		print(self.resize)
		self.image: Surface = material.image.__copy__()
		self.rect: Rect = self.image.get_rect()
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

		self.calculate_viewpoint_position()

	def update( self ):
		super().update()
		super( pg.sprite.Sprite, self ).update()

		self.image = pg.transform.scale( self.material.image, vec2(TILE_SIZE, TILE_SIZE) )
		self.image = pg.transform.rotate( self.image, self.screen_ang )
		
		self.rect: Rect = self.image.get_rect()
		self.rect.center = self.screen_pos