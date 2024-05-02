#!/usr/bin/env python3


import sys
import platform
import asyncio
from itertools import cycle
import websocket
import json
import threading
import logging

logging.basicConfig(level=logging.INFO)

from settings import *
from config import URI
from cache import Cache
from player import Player
from scene import Scene, LoadingScene
from message import Message

import random
import time

class App:
    def __init__( self, username, password ):
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
        self.main_group = pg.sprite.LayeredUpdates()
        self.entity_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.transparent_objects = []

        self.done_counter = 0

        # game objects
        self.player = None

        # player credentials
        self.username = username
        self.password = password

        # server connection
        self.closing = False
        self.connect()
    
        self.players_pos = {}

        
        self.cache = None
        self.scene = None
        self.message = Message( self )
        


    def update( self ):
        if self.scene:
            self.scene.update()
            self.entity_group.update()
            self.main_group.update()
            pg.display.set_caption( 'The Circus of Game Mechanics' ) #( f'{self.clock.get_fps(): .1f}' )
            self.delta_time = self.clock.tick()

    def draw( self ):
        try:
            self.scene.draw()
        except:
            self.screen.fill( BG_COLOR )
            self.entity_group.draw( self.screen )
            self.main_group.draw( self.screen )
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
            elif e.type == pg.MOUSEBUTTONDOWN: #1 lijevi klik, 2 scroll, 3 desni klik
                print("Mis pritisnut")
                if e.button == 1 or e.button == 3: 
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
            self.scene = LoadingScene( self )
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
        if not self.closing:
            logging.info( "Attempting to reconnect..." )
            self.connect()

    def on_open( self, ws ):
        logging.info( "Connection established" )
        message = json.dumps( {"command":"register", "id": self.username, "password": self.password } )
        ws.send( message )
        logging.info( f"Sent: {message}" )

        # In case that fails, try to log them in
        message = json.dumps( {"command":"login", "id": self.username, "password": self.password } )
        ws.send( message )
        logging.info( f"Sent: {message}" )

        logging.info( "Login sequence finished..." )


async def run( app ):
    while True:
        if app.player:
            app.check_events()
        app.get_time()
        app.update()
        app.draw()
        await asyncio.sleep( 0 )


if __name__ == '__main__':
    if __import__( "sys" ).platform == "emscripten":
        from time import sleep
        try:
            platform.document.body.style.background = '#000000'
        except:
            pass

    import argparse

    parser = argparse.ArgumentParser(description='MMORPG')

    parser.add_argument('--username', type=str, help='The username', required=True)
    parser.add_argument('--password', type=str, help='The password', required=True)

    args = parser.parse_args()


    args = parser.parse_args()

    app = App( args.username, args.password )
    asyncio.run( run( app ) )
