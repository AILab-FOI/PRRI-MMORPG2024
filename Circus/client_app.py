from shared import *

from message import Message

from config import URI
import threading
from scene import LoadingScene

import logging
import websocket

import json

from draw_manager import DrawManager
from player import Player
from viewpoint import Viewpoint
from entity_system import EntitySystem

import pygame as pg

class ClientApp:
    def __init__( self, username: str, password: str ):
        if __import__( "sys" ).platform == "emscripten": # change to !=
            self.screen = pg.display.set_mode( RES, pg.FULLSCREEN )
        else:
            self.screen = pg.display.set_mode( RES ) 
        
        pg.font.init()

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer( self.anim_event, 100 )
        
        # groups

        self.entity_system = EntitySystem()
        self.draw_manager = DrawManager()
        self.collision_group = pg.sprite.Group()
        
        self.transparent_objects = []

        self.done_counter = 0

        # game objects
        self.player: Player = None

        # player credentials
        self.username = username
        self.password = password

        # server connection
        self.closing = False
        self.connect()
    
        self.players_pos = {}
        
        self.cache = None
        self.scene = None
        self.message = Message( self.screen.get_size() )

        self.active_viewpoint: Viewpoint = None
    
    def set_local_player( self, player: Player ):
        self.player = player
        self.active_viewpoint = player.viewpoint
        self.draw_manager.dirty = True

    def set_active_scene( self, scene ):
        self.scene = scene

    def tick( self ):
        if self.player:
            self.check_events()
        
        self.get_time()
        self.update()
        self.draw()

    def update( self ):
        if self.scene:
            self.scene.update()
            pg.display.set_caption( 'The Circus of Game Mechanics' ) #( f'{self.clock.get_fps(): .1f}' )
            self.delta_time = self.clock.tick()
        
        self.entity_system.think()
        self.draw_manager.update()

    def draw( self ):
        try:
            self.scene.draw()
        except:
            self.screen.fill( BG_COLOR )
            self.draw_manager.draw()
            self.message.draw()
        
        
        pg.display.flip()

    def check_events( self ):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or ( e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE ):
                if __import__( "sys" ).platform != "emscripten":
                    print( CREDITS )
                    logging.info( 'Closing server connection ...' )
                    self.ws.keep_running = False
                    self.closing = True
                    pg.quit()
                    sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            elif e.type == pg.KEYDOWN:
                self.player.single_fire( event=e )

    def get_time( self ):
        self.time = pg.time.get_ticks() * 0.001

    
    def connect( self ):
        self.ws = websocket.WebSocketApp( URI,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close )
        self.thread = threading.Thread( target=lambda: self.ws.run_forever( ping_interval=60 ) )
        self.thread.start()

    def on_message( self, ws, message ):
        logging.info( f"Message received: {message}" )
        if not self.scene:
            self.scene = LoadingScene()
        data = json.loads( message )
        for player in data:
            if player != self.username:
                x = data[ player ][ 'x' ]
                y = data[ player ][ 'y' ]
                print( player, x, y )
                pos = vec2( x * TILE_SIZE, y * TILE_SIZE ) + vec2( 0.5 )
                self.players_pos[ player ] = pos

    def on_error( self, ws, error ):
        logging.error( f"Connection error: {error}" )

    def on_close( self, ws, close_status_code, close_msg ):
        logging.warning( "Connection to server closed" )
        self.closed = True
        if not self.closing:
            logging.info( "Attempting to reconnect..." )
            self.connect()

    def on_open( self, ws ):
        self.closed = False
        logging.info( "Connection established" )
        message = json.dumps( {"command":"register", "id": self.username, "password": self.password } )
        ws.send( message )
        logging.info( f"Sent: {message}" )

        # In case that fails, try to log them in
        message = json.dumps( {"command":"login", "id": self.username, "password": self.password } )
        ws.send( message )
        logging.info( f"Sent: {message}" )

        logging.info( "Login sequence finished..." )

