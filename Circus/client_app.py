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
from shared import _globals
from viewpoint import Viewpoint
from entity_system import EntitySystem
from materialsystem import MaterialSystem
import sys
import pygame as pg  
from chat import Chat
import quest

from entity import RemotePlayer

class ClientApp:
    """Client app base class
    """    
    def __init__(self, username: str, password: str):
        if __import__("sys").platform == "emscripten":
            self.screen = pg.display.set_mode(RES, pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(RES) 
        
        pg.font.init()

        # Font
        self.font = pg.font.Font(None, 32)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, 100)
        
        # groups
        self.entity_system = EntitySystem()
        self.draw_manager = DrawManager()
        self.material_system = MaterialSystem()
        self.collision_group = pg.sprite.Group()
        
        self.clickable_group = []

        self.transparent_objects = []

        self.done_counter = 0

        self.trackables = {}
        # game objects
        self.player: Player = None

        self.chat: Chat = None
        # player credentials
        self.username = username
        self.password = password

        # server connection
        self.messages_to_send: list = []
        self.messages_to_receive: list = []
        self.closing = False
        self.closed = False
        self.connect()
    
        self.players_pos = {}
        self.quest_list = {}

        for id in _globals.tmp_quest_list.keys():
            quest = _globals.tmp_quest_list[id]
            self.add_quest(id, quest)
        
        _globals.tmp_quest_list = {}

        self.cache = None
        self.scene = None
        self.message = Message([self.screen.get_size()[0], self.screen.get_size()[1] / 2], self.screen.get_size(), font_size=20)
        self.fps_counter = Message([self.screen.get_size()[0]-200, 0], [200, 80], font_size=10)

        self.active_viewpoint: Viewpoint = None
    def set_chat(self, chat: Chat):
        """Set the Chat

        Args:
            chat (Chat): chat object
        """
        self.chat = chat

    def set_local_player(self, player: Player):
        """Set the local player

        Args:
            player (Player): player to set local
        """        
        self.player = player
        self.active_viewpoint = player.viewpoint
        self.draw_manager.set_dirty(True)

    def set_active_scene(self, scene):
        """Sets the active scene

        Args:
            scene (Scene): Scene to set as active
        """        
        self.scene = scene

    def add_quest(self, id, quest ):
        self.push_websocket_message({"command": "request_quest_info", "player": self.username, "quest": id})
        self.quest_list[id] = quest

    def tick(self):
        """A single game tick
        """
        if self.player:
            self.check_events()
        
        self.get_time()
        self.update()
        self.draw()

        self.delta_time = self.clock.tick()

        clientApp().fps_counter.set_message( "Fps: " + str(self.clock.get_fps()) )
        clientApp().fps_counter.active = True
    
    def update(self):
        """Updates the systems
        """        
        # Send our input first and foremost
        self.websocket_loop()

        if self.scene:
            self.scene.update()
            pg.display.set_caption('Age of Dogma a1.0')
            pg.display.set_icon(pg.image.load('assets/images/favicon.png'))
        
        self.entity_system.think()
        self.draw_manager.update()

    def draw(self):
        """Draws the scene
        """
        try:
            self.scene.draw()
        except AttributeError as e:
            # Scene doesn't have a draw method, just use regular draw
            self.screen.fill(BG_COLOR)
            self.draw_manager.draw()
            self.message.draw()
            self.fps_counter.draw()
            # Crtanje chata
            #self.draw_chat()
        except Exception as e:
            logging.info( f"Couldn't draw scene {str(e)}" )
        

        pg.display.flip()

    def print_quests( self ):
        for id, quest in self.quest_list.items():
            print(f"{id}: {quest.title}")
            print(f"{quest.text}")
            print(f"\tAccepted: {quest.accepted}")
            print(f"\tFinished: {quest.finished}")
            if( quest.reward ):
                print(f"\tRewards: {quest.reward.reward_string()}")
            print(f"\tProgress:")
            for progress_type, progress in quest.progress.items():
                print(f"\t\t{progress_type}: {progress}")

    def check_events(self):
        """Checks events
        """        
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                if __import__("sys").platform != "emscripten":
                    print(CREDITS)
                    logging.info('Closing server connection ...')
                    self.ws.keep_running = False
                    self.closing = True
                    pg.quit()
                    sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            else:
                self.check_interactable_events( e )


            self.chat.check_event( e=e )

    def check_interactable_events( self, event):

        interacted = []
        for clickable in self.clickable_group:
                interaction = clickable.try_interact( event )
                if interaction != '':
                    interacted.append(interaction)
        max_z_interaction = 0
        max_interaction = None
        for i in interacted:
            if i[ 'z' ] >= max_z_interaction:
                max_z_interaction = i[ 'z' ]
                max_interaction = i[ 'interaction' ]
        
        if max_interaction:
            max_interaction()
            

    def send_chat_message(self, message):
        chat_message = {"command": "chat_message", "message": message, "sender": self.username}
        self.push_websocket_message(chat_message)

    def get_time(self):
        """Gets the time
        """        
        self.time = pg.time.get_ticks() * 0.001

    def get_delta_time_ms(self) -> int:
        return self.delta_time

    def get_delta_time_sec(self):
        return self.delta_time * 0.001

    def connect(self):
        """Connects self to websocket
        """        
        self.ws = websocket.WebSocketApp(URI,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.websocket_thread = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=0.25))
        self.websocket_thread.start()

    def websocket_loop(self):
        self.handle_received_messages()
        self.send_websocket_messages()

    def send_websocket_messages(self):
        if( len(self.messages_to_send) <= 0 ):
            self.push_websocket_message({"command": "keep_connection"})

        while len(self.messages_to_send) > 0 and not self.closed:
            message = self.messages_to_send[0]
            try:
                #if( message['command'] != "keep_connection" ):
                #    print(f"Sending message: {message}")
                self.ws.send(json.dumps(message))
                self.messages_to_send.pop(0)
            # If we fail to send because the connection closed, break
            except:
                print("Connection closed!!")
                break

    def push_websocket_message(self, message: object, override=True):
        #if( message["command"] != "keep_connection" ):
            #print(f"Adding message: {message}")

        if override:
            for i in range(len(self.messages_to_send)):
                if self.messages_to_send[i]["command"] == message["command"]:
                    self.messages_to_send[i] = message
                    return

        self.messages_to_send.append(message)

    def on_message(self, ws: websocket, message: str):
        """On message received from websocket, updates the player based on message

        Args:
            ws (Websocket): Websocket
            message (Message): Message
        """        
        #logging.info( f"Message received: {message}" )
        
        self.messages_to_receive.append(message)

    def handle_received_messages(self):
        while( len(self.messages_to_receive) ):
            message = self.messages_to_receive[0]
            self.handle_received_message(message)
            self.messages_to_receive.pop(0)


    def handle_received_message(self, message):
        json_message = json.loads(message)

        #print(json_message)

        match json_message["command"]:
            case "player_pos":
                self.handle_player_pos_message(json_message)
            case "login_failed":
                message = self.handle_login_failed(json_message)
            case "login_successful":
                if not self.scene:
                    self.scene = LoadingScene()
            case "quest_info":
                self.handle_quest_info_update(json_message)
            case "chat_message":
                # Handle incoming chat message
                self.handle_chat_message(json_message)
            case "server_ent_update":
                self.handle_server_ent_update(message, json_message)
            case "inventory_update":
                data = json_message["inventory"]
                if( clientApp().player == None ):
                    _globals.tmp_inv = data
                else:
                    clientApp().player.inventory.load_from_net(data)

    def handle_server_ent_update(self, message, json_message):
        data = json_message["data"]
        netid = data["netid"]

        new_message = self.get_latest_update_message_and_remove_the_rest(netid)
        if( new_message == None ):
            json_message = json.loads(message)

        if( self.entity_system.test_ent != None ):
            newpos = vec2( data["position"]["x"],
                         data["position"]["y"] )
                    
            self.entity_system.test_ent.set_pos(newpos)

    def get_latest_update_message_and_remove_the_rest( self, entindex ):
        latestUpdateMessage = None
        for messageIndex in range(len(self.messages_to_receive)-1, -1,-1):
            message = self.messages_to_receive[messageIndex]
            data = json.loads( message )
            if( data['command'] != 'server_ent_update' ):
                continue

            if( data["data"]['netid'] != entindex ):
                continue

            if latestUpdateMessage == None:
                latestUpdateMessage = message
        
            data['command'] = 'skip'
            self.messages_to_receive[messageIndex] = json.dumps(data)
        
        return latestUpdateMessage

    def handle_player_pos_message(self, json_message):
        data = json_message["data"]
        for player in data:
            player_data = data[ player ]
            player_exists = player in self.players_pos

            position = player_data[ 'position' ]
            velocity = player_data[ 'velocity' ]

                    #if(player != self.username):
                    #    print( player, position, velocity )

            pos = vec2( position['x'], position['y'] )
            vel = vec2( velocity['x'], velocity['y'] )

            player_info = {}
            player_info["time"] = self.time
            player_info["position"] = pos
            player_info["velocity"] = vel

            if self.scene and self.scene.done and player != self.username and not player_exists: 
                RemotePlayer( 'remote_player', pos, player )

            self.players_pos[ player ] = player_info

    def handle_login_failed(self, json_message):
        data = json_message["data"]
        if data == "player_doesnt_exist":
            message = {"command": "register", "id": self.username, "password": self.password}
            self.push_websocket_message(message)
            logging.info(f"Sent: {message}")
        return message

    def handle_chat_message(self, json_message):
        if not self.chat:
            return
        sender = json_message["sender"]
        chat_message = json_message["message"]
        self.chat.add_message(f"{sender}: {chat_message}")

    def handle_quest_info_update(self, json_message):
        quest_id = json_message['quest']

        if( not quest_id in self.quest_list ):
            self.quest_list[quest_id] = quest.Quest(quest_id)
        
        self.quest_list[quest_id].accepted = json_message['accepted']
        self.quest_list[quest_id].finished = json_message['finished']
        self.quest_list[quest_id].progress = json_message['progress']

    def on_error(self, ws: websocket, error):
        """On error

        Args:
            ws (websocket): websocket
            error (error): error
        """        
        logging.error(f"Connection error: {error}")

    def on_close(self, ws: websocket, close_status_code, close_msg):
        logging.info(close_status_code)
        logging.info(close_msg)

        logging.warning("Connection to server closed")
        self.closed = True

        if not self.closing:
            logging.info("Attempting to reconnect...")
            self.connect()

    def on_open(self, ws: websocket):
        """On open

        Args:
            ws (websocket): websocked to open
        """        
        self.closed = False
        logging.info("Connection established")

        # Try to log in
        message = {"command": "login", "id": self.username, "password": self.password}
        self.push_websocket_message(message)
        logging.info(f"Sent: {message}")

        logging.info("Login sequence finished...")
