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

        self.WIDTH, self.HEIGHT = 400, 200
 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (200, 200, 200)

        self.CHAT_BOX_HEIGHT = 100
        self.input_box = pg.Rect(self.WIDTH - 10 - (self.WIDTH - 20), self.HEIGHT - self.CHAT_BOX_HEIGHT + 10, self.WIDTH - 20, 32)
        self.chat_display_box = pg.Rect(self.WIDTH - 10 - (self.WIDTH - 20), 10, self.WIDTH - 20, self.HEIGHT - self.CHAT_BOX_HEIGHT - 20)

        self.active = False
        self.text = ''
        self.chat_messages = []
        self.chat_scroll_offset = 0  # Offset for scrolling

        # Font
        self.font = pg.font.Font(None, 32)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, 100)
        
        # Transparent surfaces
        self.chat_surface = pg.Surface((self.chat_display_box.width, self.chat_display_box.height))
        self.chat_surface.set_alpha(128)  # Adjust alpha for transparency
        self.input_surface = pg.Surface((self.input_box.width, self.input_box.height))
        self.input_surface.set_alpha(128)  # Adjust alpha for transparency

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

        # player credentials
        self.username = username
        self.password = password

        # server connection
        self.messages_to_send: list = []
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
            self.draw_chat()
        except Exception as e:
            logging.info( f"Couldn't draw scene {str(e)}" )
        

        pg.display.flip()

    def draw_chat(self):
        # Draw chat display box with transparency
        self.chat_surface.fill((self.GREY[0], self.GREY[1], self.GREY[2], 128))  # Transparent background
        y = 10 + self.chat_scroll_offset
        for message in self.chat_messages:
            msg_surface = self.font.render(message, True, self.BLACK)
            self.chat_surface.blit(msg_surface, (5, y))
            y += msg_surface.get_height() + 5

        # Draw input box with transparency
        self.input_surface.fill((self.WHITE[0], self.WHITE[1], self.WHITE[2], 128))  # Transparent background
        txt_surface = self.font.render(self.text, True, self.BLACK)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.input_surface.blit(txt_surface, (5, 5))

        # Draw chat surfaces on the main screen
        self.screen.blit(self.chat_surface, (self.chat_display_box.x, self.chat_display_box.y))
        self.screen.blit(self.input_surface, (self.input_box.x, self.input_box.y))

        pg.draw.rect(self.screen, self.BLACK, self.chat_display_box, 2)
        pg.draw.rect(self.screen, self.BLACK, self.input_box, 2)

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
            elif e.type == pg.MOUSEBUTTONDOWN:
                # to do seperate this into its own function for testing and handling
                clicked = False
                max = 0
                interact = ''
                for clickable in self.clickable_group:
                    interaction = clickable.try_interact()
                    if interaction != '':
                        clicked = True
                        if interaction[ 'z' ] >= max:
                            max = interaction[ 'z' ]
                            interact = interaction[ 'interaction' ]
                if not clicked:
                    self.player.single_fire( event=e )
                else:
                    interact()
            else:
                self.player.single_fire( event=e )
            
            # Chat input handling
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(e.pos):
                    self.active = True
                else:
                    self.active = False
            if e.type == pg.KEYDOWN:
                if self.active:
                    if e.key == pg.K_RETURN:
                        # Send chat message to server
                        if self.text.strip() != '':
                            self.send_chat_message(self.text)
                        self.text = ''
                    elif e.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += e.unicode
            # Scroll chat messages
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.chat_display_box.collidepoint(e.pos):
                    self.active = True
            if e.type == pg.MOUSEBUTTONDOWN and self.chat_display_box.collidepoint(e.pos):
                if e.button == 4:  # Scroll up
                    self.chat_scroll_offset = min(self.chat_scroll_offset + 20, 0)
                if e.button == 5:  # Scroll down
                    self.chat_scroll_offset = max(self.chat_scroll_offset - 20, -max(0, len(self.chat_messages) * 37 - self.chat_display_box.height))

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

            if self.scene.done and player != self.username and not player_exists: 
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
        sender = json_message["sender"]
        chat_message = json_message["message"]
        self.chat_messages.append(f"{sender}: {chat_message}")

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
