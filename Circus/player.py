from shared import *
from shared import _globals
import math
from entity import BaseSpriteEntity
from bullet import Bullet
from itertools import cycle
import json
import logging
from dialogue import Dialogue
from viewpoint import Viewpoint
import inventory
import inventory_item

from slash import Slash
from fireball import Fireball
from lightning import Lightning
from heal import Heal
from datetime import datetime, timedelta

class Player( BaseSpriteEntity ):
    """Player base class

    Args:
        BaseSpriteEntity ( BaseSpriteEntity ): Sprite entity to create the player from
    """    
    def __init__( self, name='player' ):
        super().__init__( name )

        self.offset = vec2( 0 )
        self.last_offset = vec2( 0 )
        
        self.inc = vec2( 0 )
        self.prev_inc = vec2( 0 )
        self.last_inc = vec2( 0 )
        self.angle = 0

        self.viewpoint = Viewpoint()

        self.down_ind = [ 3, 7, 11, 15 ]
        self.down_list = cycle( self.down_ind )
        self.up_ind = [ 2, 6, 10, 14 ]
        self.up_list = cycle( self.up_ind )
        self.left_ind = [ 1, 5, 9, 13 ]
        self.left_list = cycle( self.left_ind )
        self.right_ind = [ 0, 4, 8, 12 ]
        self.right_list = cycle( self.right_ind )

        self.tick_time = datetime.now()

        self.direction = 'DOWN'
        self.moving = False
        
        self.health = 100
        self.armor = 0
        self.mana = 100
        self.alive = True

        self.inventoryDisplay = Dialogue(name='inventory-display')
        self.inventoryDisplay.set_message("")
        self.inventoryDisplay.display()
        
        self.inventory : inventory.Inventory = inventory.Inventory(owner=self)
        if( _globals.tmp_inv != None ):
            self.inventory.load_from_net(_globals.tmp_inv)
            _globals.tmp_inv = None

        self.inControl = True

        clientApp().trackables['player-health'] = {'object': self, 'attr': 'health', 'max': 100}
        clientApp().trackables['player-mana'] = {'object': self, 'attr': 'mana', 'max': 100}

        self.questDialogue = Dialogue()


        slash = ENTITY_SPRITE_ATTRS[ 'ability_slash' ]
        fireball = ENTITY_SPRITE_ATTRS[ 'ability_fireball' ]
        lightning = ENTITY_SPRITE_ATTRS[ 'ability_lightning' ]
        heal = ENTITY_SPRITE_ATTRS[ 'ability_heal' ]
        self.gcd = datetime.now()
        self.abilities = []
        self.abilities.append({'cooldown': slash['cooldown'], 'used-time': datetime.now()})
        self.abilities.append({'cooldown': fireball['cooldown'], 'used-time': datetime.now()})
        self.abilities.append({'cooldown': lightning['cooldown'], 'used-time': datetime.now()})
        self.abilities.append({'cooldown': heal['cooldown'], 'used-time': datetime.now()})

    def on_start_drawing(self):
        super().on_start_drawing()
        self.sprite.groups()[0].change_layer( self.sprite, CENTER.y )

        self.sprite.rect = self.sprite.image.get_rect( center=CENTER )

    def forward( self ):
        ret = vec2()
        ret.x = math.cos(-self.angle-(math.pi/2))
        ret.y = math.sin(-self.angle-(math.pi/2))
        return ret
    
    def right( self ):
        ret = vec2()
        ret.x = math.cos(-self.angle)
        ret.y = math.sin(-self.angle)
        return ret

    def animate( self ):
        if clientApp().anim_trigger:
            if self.direction == 'DOWN':
                if self.moving:
                    self.frame_index = next( self.down_list )
                else:
                    self.frame_index = self.down_ind[ 1 ]
            elif self.direction == 'UP':
                if self.moving:
                    self.frame_index = next( self.up_list )
                else:
                    self.frame_index = self.up_ind[ 1 ]
            elif self.direction == 'LEFT':
                if self.moving:
                    self.frame_index = next( self.left_list )
                else:
                    self.frame_index = self.left_ind[ 1 ]
            else:
                if self.moving:
                    self.frame_index = next( self.right_list )
                else:
                    self.frame_index = self.right_ind[ 1 ]

            self.sprite.image = self.images[ self.frame_index ]


    def use_mana( self, amount ):
        if self.mana - amount <= 0:
            self.mana = 0
        else:
            self.mana -= amount

    def retrieve_mana ( self ):
        elapsed = datetime.now() - self.tick_time
        if elapsed.seconds >= 0.5:
            if self.mana + 8 >= 100:
                self.mana = 100
            else:
                self.mana += 8
            self.tick_time = datetime.now()

        

    def control( self ):
        if not self.inControl:
            return
        
        self.moving = False
        self.last_inc[0] = self.inc[0]
        self.last_inc[1] = self.inc[1]
        self.inc = vec2( 0 )
        speed = PLAYER_SPEED * clientApp().delta_time
        rot_speed = PLAYER_ROT_SPEED * clientApp().delta_time

        key_state = pg.key.get_pressed()

        if key_state[ pg.K_q ]:
            self.angle += rot_speed
        if key_state[ pg.K_e ]:
            self.angle -= rot_speed

        if key_state[ pg.K_w ]:
            self.inc += vec2( 0, -speed ).rotate_rad( -self.angle )
            self.direction = 'UP'
            self.moving = True
        if key_state[ pg.K_s ]:
            self.inc += vec2( 0, speed ).rotate_rad( -self.angle )
            self.direction = 'DOWN'
            self.moving = True
        if key_state[ pg.K_a ]:
            self.inc += vec2( -speed, 0 ).rotate_rad( -self.angle )
            self.direction = 'LEFT'
            self.moving = True
        if key_state[ pg.K_d ]:
            self.inc += vec2( speed, 0 ).rotate_rad( -self.angle )
            self.direction = 'RIGHT'
            self.moving = True

        if self.inc.x and self.inc.y:
            self.inc.normalize()
            self.inc.scale_to_length( speed )
            
    def damage( self, amount ):
        if self.health - amount <= 0:
            self.health = 0
        else:
            self.health -= amount
    def heal( self, amount ):
        if self.health + amount >= 100:
            self.health = 100
        else:
            self.health += amount
    def single_fire( self, event ):     
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.questDialogue.handle_input()

    def check_collision( self ):
        if( self.sprite == None ):
            return

        hitobst = pg.sprite.spritecollide( self.sprite, clientApp().collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask )
        hit = pg.sprite.spritecollide( self.sprite, clientApp().draw_manager.layer_masks['entity_layer'],
                                      dokill=False, collided=pg.sprite.collide_mask )
        
        for obj in list(hit):
            if( "can_collide" in obj.entity.attrs and obj.entity.attrs["can_collide"] == False ):
                hit.remove(obj)

        for obj in list(hitobst):
            if( "can_collide" in obj.attrs and obj.attrs["can_collide"] == False ):
                hitobst.remove(obj)

        if len(hit) == 0:
            hit = None

        if len(hitobst) == 0:
            hitobst = None

        if not hitobst and not hit:
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            self.inc = -self.prev_inc
            if hit:
                clientApp().message.set_message( hit[ 0 ].entity.message )
                clientApp().message.active = True
            if hitobst and hitobst[ 0 ].message != '':
                clientApp().message.set_message( hitobst[ 0 ].message )
                clientApp().message.active = True

    def has_moved_this_frame(self) -> bool:
        x = self.offset[ 0 ]
        y = self.offset[ 1 ]
        x1 = self.last_offset[ 0 ]
        y1 = self.last_offset[ 1 ]

        return (x != x1 or y != y1)

    def has_velocity_changed( self ):
        x = self.inc[ 0 ]
        y = self.inc[ 1 ]
        x1 = self.last_inc[ 0 ]
        y1 = self.last_inc[ 1 ]

        return (x != x1 or y != y1)

    def move( self ):
        self.offset += self.inc
        
        if self.has_velocity_changed() or self.has_moved_this_frame():
            message = { "command":"update",
                        "id": clientApp().username,
                        "position": { "x": self.offset.x, "y": self.offset.y },
                        'velocity': { "x":self.inc.x, "y":self.inc.y } }
            clientApp().push_websocket_message( message )

        self.last_offset[ 0 ] = self.offset[ 0 ]
        self.last_offset[ 1 ] = self.offset[ 1 ]


    def should_think(self) -> bool:
        return True
    
    def update_visuals(self):
        self.animate()
        self.pos = self.offset
        self.viewpoint.set_ang( self.angle )
        self.viewpoint.set_pos( self.offset )

    def think( self ):
        self.retrieve_mana()
        self.control()
        self.check_collision()
        self.move()

    def set_pos(self, newPos):
        super().set_pos(newPos)
        self.offset = newPos

    def on_player_inventory_updated(self):
        inventoryMessage = "Inventory:\n"
        for item in self.inventory.items_list:
            itemMessage = f"{item.name}\n  {item.description}\n  Type:{item.type}\n  Power:{item.stat}\n"
            inventoryMessage += itemMessage

        print(inventoryMessage)
        self.inventoryDisplay.set_message(inventoryMessage)
        self.inventoryDisplay.display()

        for inv_item in self.inventory.items_list:
            # gleda se zadnji u listi
            if inv_item.type == "armor":
                self.armor = inv_item.stat

    def use_slash( self ):
        if self.check_cooldown(self.abilities[0]):
            Slash()
            ATTACK_SOUND.play()

    def use_fireball( self ):
        if self.check_cooldown(self.abilities[1]):
            if self.mana >= 15:
                Fireball()
                self.use_mana(50)

    def use_lightning( self ):
        if self.check_cooldown(self.abilities[2]):
            if self.mana >= 50:
                Lightning()
                self.use_mana(50)

    def use_heal( self ):
        if self.check_cooldown(self.abilities[3]):
            if self.mana >= 30:
                Heal()
                self.use_mana(30)

    def check_cooldown( self, ability ):

        global_elapsed = datetime.now() - self.gcd
        if global_elapsed.total_seconds() < 0.5:
            return False

        elapsed = datetime.now() - ability['used-time']

        if elapsed.total_seconds() > ability['cooldown']:
            self.gcd = datetime.now()
            ability['used-time'] = datetime.now()
            return True
        else:
            return False
