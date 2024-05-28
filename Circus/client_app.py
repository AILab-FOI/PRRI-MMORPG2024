import time
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
from materialsystem import MaterialSystem

class ClientApp:
    """Client app base class
    """    
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
        self.material_system = MaterialSystem()
        self.collision_group = pg.sprite.Group()
        
        self.transparent_objects = []

        self.done_counter = 0

        # game objects
        self.player: Player = None

        # player credentials
        self.username = username
        self.password = password

        # server connection

        self.messages_to_send : list = []
        self.closing = False
        self.closed = False
        self.connect()
    
        self.players_pos = {}
        
        self.cache = None
        self.scene = None
        self.message = Message( [self.screen.get_size()[0],self.screen.get_size()[1] / 2], self.screen.get_size(), font_size=20 )
        self.fps_counter = Message( [0, 0], [200, 80], font_size= 10 )

        self.active_viewpoint: Viewpoint = None
    
    def set_local_player( self, player: Player ):
        """Set the local player

        Args:
            player (Player): player to set local
        """        
        self.player = player
        self.active_viewpoint = player.viewpoint
        self.draw_manager.set_dirty()

    def set_active_scene( self, scene ):
        """Sets the active scene

        Args:
            scene (Scene): Scene to set as active
        """        
        self.scene = scene

    def tick( self ):
        """A single game tick
        """        

        start = time.time()


        if self.player:
            self.check_events()
        
        self.get_time()
        self.update()
        self.draw()

        end = time.time()
        delta_time = end - start
        fps = "Inf"
        if( delta_time != 0 ):
            fps = 1 / max(delta_time, 0.000000000001)

        clientApp().fps_counter.set_message( "Fps: " + str(fps) )
        clientApp().fps_counter.active = True
    
    def update( self ):
        """Updates the systems
        """        
        # Send our input first and foremost
        self.websocket_loop()

        if self.scene:
            self.scene.update()
            pg.display.set_caption( 'The Circus of Game Mechanics' ) #( f'{self.clock.get_fps(): .1f}' )
            self.delta_time = self.clock.tick()
        
        self.entity_system.think()
        self.draw_manager.update()

    def draw( self ):
        """Draws the scene
        """        
        try:
            self.scene.draw()
        except:
            self.screen.fill( BG_COLOR )
            self.draw_manager.draw()
            self.message.draw()
            self.fps_counter.draw()
        
        
        pg.display.flip()

    def check_events( self ):
        """Checks events
        """        
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
        """Gets the time
        """        
        self.time = pg.time.get_ticks() * 0.001

    
    def connect( self ):
        """Connects self to websocket
        """        
        self.ws = websocket.WebSocketApp( URI,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close )
        self.websocket_thread = threading.Thread( target=lambda: self.ws.run_forever( ping_interval=0.25 ) )
        self.websocket_thread.start()
        

    def websocket_loop( self ):
        while len(self.messages_to_send) > 0 and not self.closed:
            message = self.messages_to_send[0]
            try:
                print(f"Sending message: {message}")
                self.ws.send( json.dumps(message) )
                self.messages_to_send.pop(0)
            # If we fail to send because the connection closed, break
            except:
                print("Connection closed!!")
                break

    def push_websocket_message( self, message: object, override = True ):
        print(f"Adding message: {message}")

        if( override ):
            for i in range(len(self.messages_to_send)):
                if( self.messages_to_send[i]["command"] == message["command"] ):
                    self.messages_to_send[i] = message
                    return

        self.messages_to_send.append( message )

    def on_message( self, ws: websocket, message: Message ):
        """On message received from websocket, updates the player based on message

        Args:
            ws ( Websocket ): Websocket
            message ( Message ): Message
        """        
        logging.info( f"Message received: {message}" )
        if not self.scene:
            self.scene = LoadingScene()
        
        json_message = json.loads( message )

        print(json_message)

        match json_message["command"]:
            case "player_pos":
                data = json_message["data"]
                for player in data:
                    if player != self.username:
                        x = data[ player ][ 'x' ]
                        y = data[ player ][ 'y' ]
                        print( player, x, y )
                        pos = vec2( x, y )
                        self.players_pos[ player ] = pos
            case "login_failed":
                data = json_message["data"]
                if data == "player_doesnt_exist":
                    message = {"command":"register", "id": self.username, "password": self.password }
                    self.push_websocket_message(message)
                    logging.info( f"Sent: {message}" )

    def on_error( self, ws: websocket, error ):
        """On error

        Args:
            ws (websocket): websocket
            error (error): error
        """        
        logging.error( f"Connection error: {error}" )

    def on_close( self, ws: websocket, close_status_code, close_msg ):

        logging.info(close_status_code)
        logging.info(close_msg)

        logging.warning( "Connection to server closed" )
        self.closed = True

        if not self.closing:
            logging.info( "Attempting to reconnect..." )
            self.connect()

    def on_open( self, ws: websocket ):
        """On open

        Args:
            ws (websocket): websocked to open
        """        
        self.closed = False
        logging.info( "Connection established" )

        # Try to log in
        message = {"command":"login", "id": self.username, "password": self.password }
        self.push_websocket_message(message)
        logging.info( f"Sent: {message}" )

        logging.info( "Login sequence finished..." )

