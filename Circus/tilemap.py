from shared import *
from entity import WorldObject
from materialsystem import Material
import os
import json

class MapData(object):
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

	def update_screenpos(self):
		self.sprite.image = self.material.image
		self.sprite.image = pg.transform.rotate( self.sprite.image, self.screen_ang )
		
		self.sprite.rect = self.sprite.image.get_rect()
		self.sprite.rect.center = self.screen_pos