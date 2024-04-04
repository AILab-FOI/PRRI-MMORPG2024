from entity import *


class Explosion( Entity ):
    def __init__( self, name='explosion', pos=( 0, 0 )):
        super().__init__( name, pos )
        self.life_time_cycles = self.attrs[ 'num_layers' ] - 1
        self.cycles = 0

    def should_think(self) -> bool:
        return True

    def think( self ):
        self.check_life_time()

    def change_layer( self ):
        self.sprite.groups()[0].change_layer( self.sprite, self.sprite.rect.centery )

    def check_life_time( self ):
        if clientApp().anim_trigger:
            self.cycles += 1
            if self.cycles > self.life_time_cycles:
                self.kill()


class Bullet( BaseSpriteEntity ):
    def __init__( self, name='bullet', pos=( 0, 0 )):
        super().__init__( name )
        self.pos = vec2( pos )
        self.player = clientApp().player
        self.y_offset = self.attrs[ 'y_offset' ]

        self.speed = 0.7
        self.bullet_direction = vec2( 0, -self.speed )
        self.life_time_cycles = 20
        self.cycles = 0
        self.angle = self.player.angle

    def check_collision( self ):
        hits = pg.sprite.spritecollide( self.sprite, clientApp().collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask )
        if hits:
            #Explosion( pos=( self.pos + self.player.offset ) / TILE_SIZE )
            self.kill()

    def change_layer( self ):
        self.sprite.groups()[0].change_layer( self.sprite, self.sprite.rect.centery - self.y_offset )

    def load_images( self ):
        return clientApp().cache.cached_entity_data[ self.name ]

    def check_life_time( self ):
        if clientApp().anim_trigger:
            self.cycles += 1
            if self.cycles > self.life_time_cycles:
                self.kill()

    def should_think(self) -> bool:
        return True
    
    def think( self ):
        self.run()
        self.check_life_time()
        self.check_collision()

    def update_visuals( self ):
        self.rotate()
        self.change_layer()

    def rotate( self ):
        pos = self.pos
        new_pos = pos.rotate_rad( self.player.angle )
        self.sprite.rect.center = new_pos + CENTER
        self.sprite.rect.centery += self.y_offset

    def run( self ):
        bullet_direction = self.bullet_direction * clientApp().delta_time
        self.pos += bullet_direction.rotate_rad( -self.angle ) - self.player.inc
