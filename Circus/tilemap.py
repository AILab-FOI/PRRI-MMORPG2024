import math
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

		size = self.material.image.get_size()
		self.resize = vec2( TILE_SIZE / size[0], TILE_SIZE / size[1] )

		self.sprite.image = self.material.image.__copy__()
		self.sprite.rect = self.sprite.image.get_rect()
		self.sprite.rect.x = self.pos.x
		self.sprite.rect.y = self.pos.y

	def calculate_viewpoint_position( self ):
		viewpoint = clientApp().active_viewpoint

		if( viewpoint == None ):
			return

		view_pos = self.pos - viewpoint.offset
		self.screen_pos = view_pos + CENTER

		self.screen_ang = 0

	def update_screenpos(self):

		"""Updates the screen position of the tile
		"""     
		self.sprite.image = self.material.image

		self.sprite.rect = self.sprite.image.get_rect()
		xydiff=(RES.x-RES.y)/2
		self.sprite.rect.center = self.screen_pos + vec2(0, xydiff)