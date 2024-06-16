from shared import *
from entity import WorldObject
from materialsystem import Material
import os
import json

class MapData(object):

	"""MapData base class
	"""    
	def __init__(self, file):
		if( not os.path.isfile(file) ):
			return
	
		if( not file.endswith(".map") ):
			return
	
		raw = open(file)

		if( raw == None ):
			return
		
		data = json.load(raw)
		raw.close()

		self.__dict__ = data.copy()


#Tile class with an image, x and y
class Tile( WorldObject ):
	"""Tile base class with an image, x and y coordinates

	Args:
		WorldObject ( WorldObject ): Which class the tile inherits from
	"""    
	def __init__( self, material: Material, pos, group ):
		# TODO: Da li da uzimamo direktan pos ili
		# da uzimamo Tile pos pa onda izračunamo konkretan pos
		self.material: Material = material
		self.group = group

		super().__init__( pos )
	
	def on_start_drawing( self ):
		self.reset_sprite()
	
	def on_stop_drawing( self ):
		self.sprite.kill()

	def reset_sprite( self ):
		self.sprite = pg.sprite.Sprite( self.group )

		self.sprite.image = self.material.rotated_image.__copy__()
		self.sprite.rect = self.sprite.image.get_rect()
		self.sprite.rect.x = self.pos.x
		self.sprite.rect.y = self.pos.y

	def update_screenpos(self):

		"""Updates the screen position of the tile
		"""
		self.sprite.kill()
		self.reset_sprite()
		self.sprite.rect.center = self.screen_pos