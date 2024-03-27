class MapData(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height

class Layer(object):
	def __init__( self, layerIndex, mapObject ):
		#Layer index from tiled map
		self.layerIndex = layerIndex
		
		#Create gruop of tiles for this layer
		self.tiles = pygame.sprite.Group()
		
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
class Tile(pygame.sprite.Sprite):
	def __init__( self, material, x, y ):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = material.image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Material:
	def __init__( self, file ):
		if( os.path.isfile(file) ):
			self.image = pygame.image.load( file )
		else:
			self.image = pygame.image.load( "assets/materials/missing.png" )