from entity import *
import logging

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


class Bullet( Entity ):
    def __init__( self, name='bullet', pos=vec2(0,0) ):
        print(pos)
        super().__init__( name, pos )
        # Entity multiplies our pos with TILE_SIZE, so undo that
        self.pos /= TILE_SIZE
        self.player = clientApp().player

        self.speed = 40
        self.life_time_cycles = 20
        self.cycles = 0
        self.bullet_direction = self.player.forward()

        self.always_update = True

    def check_collision( self ):
        if( not self.sprite ):
            return

        hits = pg.sprite.spritecollide( self.sprite, clientApp().collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask )
        if hits:
            Explosion( pos=( self.pos + self.player.offset ) / TILE_SIZE )

            # animation switching testing
            if hits[0].name == 'dog':
                if hits[0].state == 0:
                    hits[0].change_animation('run')
                elif hits[0].state == 1:
                    hits[0].change_animation('walk')
                elif hits[0].state == 2:
                    hits[0].change_animation('idle')

            self.kill()

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

    def run( self ):
        self.set_pos( self.pos + (self.bullet_direction * self.speed) )