from shared import *
from entity import WorldObject
from materialsystem import Material

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

#Tile class with an image, x and y
class Tile( WorldObject ):
	def __init__( self, material: Material, pos, group ):
		# TODO: Da li da uzimamo direktan pos ili
		# da uzimamo Tile pos pa onda izračunamo konkretan pos
		self.material: Material = material
		self.sprite = pg.sprite.Sprite( group )

		size = material.image.get_size()
		self.resize = vec2( TILE_SIZE / size[0], TILE_SIZE / size[1] )

		self.sprite.image = material.image.__copy__()
		self.sprite.rect = self.sprite.image.get_rect()
		self.sprite.rect.x = pos.x
		self.sprite.rect.y = pos.y

		super().__init__( pos )

	def update_screenpos(self):
		self.sprite.image = pg.transform.scale( self.material.image, vec2(TILE_SIZE, TILE_SIZE) )
		self.sprite.image = pg.transform.rotate( self.sprite.image, self.screen_ang )
		
		self.sprite.rect = self.sprite.image.get_rect()
		self.sprite.rect.center = self.screen_pos