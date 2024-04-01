from settings import *
import os
from main import app

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
		self.viewpoint = None

	def update( self ):
		self.calculate_viewpoint_position( self.viewpoint )

	def calculate_viewpoint_position( self ):
		view_pos = self.pos - self.viewpoint.offset
		view_pos = view_pos.rotate_rad( self.viewpoint.angle )
		self.screen_pos = view_pos + CENTER

#Tile class with an image, x and y
class Tile( pg.sprite.Sprite, WorldObject ):
	def __init__( self, material, pos ):
		super().__init__( pos )

		self.sprite.image = material.image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Material:
	def __init__( self, file ):
		if( os.path.isfile(file) ):
			self.image = pg.image.load( file )
		else:
			self.image = pg.image.load( "assets/materials/missing.png" )