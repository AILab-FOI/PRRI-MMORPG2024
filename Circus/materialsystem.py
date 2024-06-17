import asyncio
import math
import types
from shared import *
from pygame import Surface
import os
import json

class Material:
    def __init__( self, file: str ):
        if( os.path.isfile(file) ):
            if( file.endswith(".material") ):
                raw = open(file)
                
                if( raw == None ):
                    return
                
                data = json.load(raw)
                raw.close()

                self.__dict__ = data.copy()
                self.key = file
                self.image: Surface = pg.image.load( "assets/" + self.path )

                if( self.type == "tile" ):
                    self.image = pg.transform.scale( self.image, vec2(TILE_SIZE+1, TILE_SIZE+1) )
                    self.rotated_image = self.image

            else:
                self.key = file
                self.type = "tile"
                self.path = file
                self.image: Surface = pg.image.load( "assets/" + self.path )
        else:
            self.key = "materials/missing.png"
            self.type = "sprite"
            self.path = "materials/missing.png"
            self.image: Surface = pg.image.load( "assets/" + self.path )
            self.image = pg.transform.scale( self.image, vec2(TILE_SIZE, TILE_SIZE) )

class MaterialSystem:
    def __init__( self ):
        self.material_registry = {}
        self.material_registry["missing"] = Material("materials/missing.png")
        self.material_registry["materials/missing.png"] = self.material_registry["missing"]
	
    def register_material( self, file: str ) -> Material:
        ret = self.material_registry.get(file)
        
        if( ret != None ):
            return ret
        
        ret = Material(file)
        self.material_registry[file] = ret

        return ret

    def recalculate_tile_rotation(self):
        if( clientApp().active_viewpoint == None ):
            return

        angle = clientApp().active_viewpoint.angle
        angle = -math.degrees(angle)

        for material in self.material_registry.values():
            if( material.type != "tile" ):
                continue            
            
            material.rotated_image = pg.transform.rotate( material.image, angle )