#!/usr/bin/env python3
import asyncio
import threading
import time
import types
import websockets
import logging
import pygame as pg
logging.basicConfig(level=logging.INFO)

import json
from ZEO.ClientStorage import ClientStorage
from ZODB import DB, Connection
import transaction
from BTrees.OOBTree import OOBTree
import persistent

import atexit

from config import SHOST, SPORT, DBHOST, DBPORT

vec2 = pg.math.Vector2

class dbGlobal:
    db = None
    connection = None
    root = None

    def start_edit():
        pass
    
    def end_edit():
        transaction.commit()

def setup_database():
    print( 'Connecting to ZEO server' ) # Too much clutter
    storage = ClientStorage( ( DBHOST, DBPORT ) )
    db = DB( storage )
    connection: Connection = db.open()
    root = connection.root()

    dbGlobal.connection = connection
    dbGlobal.root = root

    if not hasattr( root, 'players' ):
        print( 'Creating new database' )
        root.players = OOBTree()
        transaction.commit()

    if not hasattr( root, 'entities' ):
        print( 'Creating new entity database' )
        root.entities = OOBTree()
        transaction.commit()
    
    template_player = Player( "tmp", "tmp" )

    # Ensure playeres in the database all follow the CURRENT template
    for player_id, player in dbGlobal.root.players.items():       
        for attr in dir(template_player):
            if( type(getattr(template_player, attr)) == types.MethodType ):
                continue
            
            if( not hasattr(player,attr) ):
                setattr( player, attr, getattr(template_player, attr) )
                logging.warn( f"Player {player.username} has missing attribute {attr}, adding default value...")
    
    transaction.commit()

    return db

# Player position model
class Player( persistent.Persistent ):
    """Player's position model on the server

    Args:
        persistent ( persistent ): _description_
    """    
    def __init__( self, username, password ):
        self.username = username
        self.password = password
        self.x = 0
        self.y = 0
        self.velx = 0
        self.vely = 0
        self.logged_in = False
        self.quests = {}

    def login( self, password: str ) -> bool:
        """Logins the player

        Args:
            password ( str ): player's password

        Returns:
            bool: whether login was successful
        """        
        if password == self.password:
            self.logged_in = True
            return True
        return False

    def logout( self, password ):
        if password == self.password:
            self.logged_in = False

    def update( self, position, velocity ):
        if self.logged_in:
            self.x = position['x']
            self.y = position['y']
            self.velx = velocity['x']
            self.vely = velocity['y']   

# Set to keep track of connected clients
connected_clients = set()

# WebSocket server handling
# Unutar funkcije handle_connection, nakon logike koja već obrađuje dolazne poruke
async def handle_connection(websocket, path: str):
    """Handles websocket connection

    Args:
        websocket ( websocket ): _description_
        path (string ): _description_
    """    
    logging.info( f"New connection: {path}" )
    connected_clients.add( websocket )

    try:
        # Existing connection handling logic...
        async for message in websocket:
            # Handle incoming messages...
            data = json.loads( message )

            notify_message = True

            try:
                if data['command'] == 'skip':
                    notify_message = False
                elif data[ 'command' ] == 'register':
                    player_id = data[ 'id' ]

                    if register_player( player_id, data[ 'password' ] ):
                        if( login_player( player_id, data[ 'password' ] ) ):
                            await send_message_to_player(websocket, {"command": "login_successful"})
                        
                        player: Player = dbGlobal.root.players[ player_id ]
                        for quest_id in player.quests:
                            await send_quest_info_to_player(websocket, quest_id, player)
                        
                        await broadcast_positions()
                    else:
                        logging.info( f'Error registring: username already taken {data}' )
                elif data[ 'command' ] == 'login':
                    player_id = data[ 'id' ]

                    if not login_player( player_id, data[ 'password' ] ):
                        await send_message_to_player( websocket, {"command": "login_failed", "data":"player_doesnt_exist"} )
                        logging.info( f'Invalid login attempt {data}' )
                    else:
                        await send_message_to_player(websocket, {"command": "login_successful"})      

                        player: Player = dbGlobal.root.players[ player_id ]
                        for quest_id in player.quests:
                            await send_quest_info_to_player(websocket, quest_id, player)
                        await broadcast_positions()                  
                elif data[ 'command' ] == 'logout':
                    logout_player( data[ 'id' ], data[ 'password' ] )
                    logging.info( f'User logged out {data}' )
                elif data[ 'command' ] == 'update':
                    notify_message = False
                    player_id = data[ 'id' ]

                    latest_message = get_latest_update_message_and_remove_the_rest( websocket, player_id )

                    if( latest_message == None ):
                        latest_message = message

                    new_data = json.loads(latest_message)

                    position = new_data['position']
                    velocity = new_data['velocity']

                    update_player_position( player_id, position, velocity )

                    await broadcast_positions()
                elif data[ 'command' ] == 'chat_message':
                    # Dodajte logiku za distribuciju chat poruke ostalim klijentima
                    sender = data['sender']
                    send_message = data['message']
                    logging.info(f"Received chat message from {sender}: {send_message}")

                    # Ovdje dodajte logiku za distribuciju poruke ostalim klijentima
                    await broadcast_message_to_all(data)
                elif data['command'] == 'keep_connection':
                    notify_message = False
                elif data['command'] == 'request_quest_info':
                    notify_message = False
                    player_id = data[ 'player' ]
                    quest_id = data['quest']
                    player: Player = dbGlobal.root.players[ player_id ]
                    
                    if( quest_id in player.quests ):
                        await send_quest_info_to_player(websocket, quest_id, player)
                    else:
                        create_quest_info(quest_id, player)
                elif data['command'] == 'update_quest_info':
                    notify_message = False
                    player_id = data[ 'player' ]
                    quest_id = data['quest']
                    dbGlobal.start_edit()
                    player: Player = dbGlobal.root.players[ player_id ]
                    
                    if( not quest_id in player.quests ):
                        player.quests[quest_id] = {}
                    
                    player.quests[quest_id]['accepted'] = data['accepted']
                    player.quests[quest_id]['finished'] = data['finished']
                    player.quests[quest_id]['progress'] = data['progress']
                    dbGlobal.end_edit()
                else:
                    print( 'Invalid command', data )
            except websockets.exceptions.ConnectionClosedOK as e:
                pass
                #logging.info(f"Connection handled successfully: {e.reason} {e.code}")
            except Exception as e:
                logging.info( f'Invalid message {data} {str(e)}' )

            if( notify_message ):
                logging.info( f"Messages left: {len(websocket.messages)}" )
                logging.info( f"Message received: {message}" )

            #await websocket.ping()  
    except websockets.exceptions.ConnectionClosedOK as e:
        logging.warning(f"Connection handled successfully: {e.reason} {e.code}")
        logging.warning(f"Command: {data}")
        connected_clients.remove( websocket )
    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"Connection closed: {e.reason} {e.code}")
        logging.warning(f"Command: {data}")
        connected_clients.remove( websocket )
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        connected_clients.remove( websocket )
    finally:
        logging.info("Connection handler exiting")

def create_quest_info(quest_id, player):
    dbGlobal.start_edit()
    player.quests[quest_id] = {}
    player.quests[quest_id]['accepted'] = False
    player.quests[quest_id]['finished'] = False
    player.quests[quest_id]['progress'] = {}
    dbGlobal.end_edit()

async def send_quest_info_to_player(websocket, quest_id, player):
    send_message = { 'command': 'quest_info', 'quest': quest_id }
    send_message['accepted'] = player.quests[quest_id]['accepted']
    send_message['finished'] = player.quests[quest_id]['finished']
    send_message['progress'] = player.quests[quest_id]['progress']

    await send_message_to_player(websocket, send_message)

def get_next_message( websocket ):
    messages = websocket.messages

    if( len(messages) <= 1 ):
        return None
    
    next = messages[1]

    try:
        data = json.loads( next )
    except:
        return None

    return data

def get_latest_update_message_and_remove_the_rest( websocket, player_id ):
    latestUpdateMessage = None
    for messageIndex in range(len(websocket.messages)-1, -1,-1):
        message = websocket.messages[messageIndex]
        data = json.loads( message )
        if( data['command'] != 'update' ):
            continue

        if( data['id'] != player_id ):
            continue

        if latestUpdateMessage == None:
            latestUpdateMessage = message
    
        data['command'] = 'skip'
        websocket.messages[messageIndex] = json.dumps(data)
    
    return latestUpdateMessage

# Register player
def register_player( player_id: str, password: str ) -> bool:
    """Registers the player
    
    Note: last 4 lines will never be executed, connection to db won't be closed and transaction won't be committed.

    Args:
        player_id ( str ): player username
        password ( str ): password string

    Returns:
        bool: whether registration was successful
    """    
    print( f"Registering player {player_id}" )
    dbGlobal.start_edit()
    if not player_id in dbGlobal.root.players:
        print("Added player!")
        dbGlobal.root.players[ player_id ] = Player( player_id, password )
        dbGlobal.end_edit()
        return True
    else:
        print( 'Error: username already taken!' )
        dbGlobal.end_edit()
        return False
    
    return authenticated

# Login player
def login_player( player_id: str, password: str ) -> bool:
    """Logins the player

    Args:
        player_id ( str): player's username
        password ( str ): player's password

    Returns:
        bool: login success
    """    
    print( f"Checking player credentials for {player_id}" )
    dbGlobal.start_edit()

    if not dbGlobal.root.players.has_key(player_id):
        return False

    authenticated = dbGlobal.root.players[ player_id ].login( password )
    dbGlobal.end_edit()
    return authenticated

def logout_player( player_id: str, password: str ):
    """Logs out the player

    Args:
        player_id ( str ): player's username
        password ( str ): player's password
    """    
    print( f"Logging out player {player_id}" )
    dbGlobal.start_edit()
    dbGlobal.root.players[ player_id ].logout( password )
    dbGlobal.end_edit()

# Update player position in the database
def update_player_position( player_id: str, position, velocity ):
    """_summary_

    Args:
        player_id (str): player's username
        x (float): x coordinate
        y (float): y coordinate
    """  
    #print( f"Updating position of player {player_id} to {x},{y}" ) # Too much clutter
    dbGlobal.start_edit()
    try:
        dbGlobal.root.players[ player_id ].update( position, velocity )
    except KeyError:
        print( f'No such player {player_id}' )
    dbGlobal.end_edit()

WEBSOCKET_SEMAPHORE = threading.BoundedSemaphore(value=1)

# Broadcast positions to all clients
async def send_message_to_player( client, object ):  
    # Send to all connected clients
    WEBSOCKET_SEMAPHORE.acquire()
    message = json.dumps( object )
    logging.info(f"Sending message{message} to client {client}")
    await client.send( message )

    WEBSOCKET_SEMAPHORE.release()

async def broadcast_message_to_all( object ):
    WEBSOCKET_SEMAPHORE.acquire()
    message = json.dumps( object )
    await asyncio.gather( *( client.send( message ) for client in connected_clients ) )
    WEBSOCKET_SEMAPHORE.release()

# Broadcast positions to all clients
async def broadcast_positions():
    """broadcasts the positions to all clients
    """    
    #print( "Broadcasting positions" ) # Too much clutter
    dbGlobal.start_edit()
    object_to_send = {"command": "player_pos"}
    positions = {
        player_id: {
            "position":{'x': player.x, 'y': player.y},
            "velocity":{'x': player.velx, 'y': player.vely}
            } 
        for player_id, player in dbGlobal.root.players.items()
        }
    object_to_send["data"] = positions

    # Send to all connected clients
    await broadcast_message_to_all( object_to_send )
    dbGlobal.end_edit()

class Entity(object):
    def __init__(self) -> types.NoneType:
        self.index = -1
        self.position = vec2(0)
        self.velocity = vec2(0)
        self.last_network_info = {}

    def tick(self):
        self.physics_think()
        self.think()
        self.gather_network_info()
        self.send_network_info()

    def think(self):
        pass

    def physics_think(self):
        if( self.velocity == vec2(0) ):
            return
        
        # Delta time is *probably* not needed because we use a consistent tick time
        # However, in the cases that it skips a frame or two, this will help
        self.position += self.velocity * gameApp().delta_time

    def gather_network_info(self) -> dict:
        network_info = {}
        network_info["netid"] = self.index
        network_info["position"] = self.position
        network_info["velocity"] = self.velocity

    def network_info_changed(self, network_info) -> bool:
        return network_info == self.last_network_info

    def send_network_info(self):
        network_info = self.gather_network_info()

        # Only push if something changed
        if( not self.network_info_changed(network_info) ):
            return

        network_info["command"] = "server_ent_update"

        gameApp().push_network_message(network_info)

        self.last_network_info = network_info

ENTITY_SEMAPHORE = threading.BoundedSemaphore(value=1)

class EntitySystem(object):
    def __init__(self) -> types.NoneType:
        self.entitylist: dict[Entity] = {}
        self.freeindex = 0
    
    def load_from_db(self):
        dbGlobal.start_edit()

        for entindex, ent in dbGlobal.root.entities.items():
            self.entitylist[entindex] = ent

        dbGlobal.end_edit()

    def add_to_db(self, entity: Entity):
        # Already exists
        if entity.index in dbGlobal.root.entities:
            return

        dbGlobal.start_edit()
        dbGlobal.root.entities[ entity.index ] = entity
        dbGlobal.end_edit()

    def add_entity(self, entity: Entity):
        entity.index = self.freeindex
        self.entitylist[entity.index] = entity
        self.add_to_db(entity)

        self.freeindex += 1

    def tick(self):
        ENTITY_SEMAPHORE.acquire()
        for entity in self.entitylist:
            entity.think()
        ENTITY_SEMAPHORE.release()

class GameApp( object ):
    def __init__(self) -> types.NoneType:
        self.clock = pg.time.Clock()
        self.start_time = time.time()
        self.delta_time = 0.01
        self.currtick = 0
        self.network_messages = []
        self.entity_handler = EntitySystem()

    def get_delta_time_ms(self):
        return self.delta_time
    
    def get_delta_time_sec(self):
        return self.delta_time * 0.001

    async def _tick(self):
        await self.tick()
        self.currtick += 1
        self.delta_time = self.clock.tick(TARGET_TICKRATE)

    async def tick(self):
        self.entity_handler.tick()
        await self.handle_network_messages()
    
    def push_network_message( self, message ):
        self.network_messages.append(message)
    
    async def handle_network_messages( self ):
        for message in self.network_messages:
            await broadcast_message_to_all(message)

TARGET_TICKRATE = 60

def game_start():
    asyncio.run( game_loop() )

async def game_loop():
    _globals.app = GameApp()

    while( True ):
        await gameApp()._tick()

        if( _globals.stop_thread ):
            return

def gameApp() -> GameApp:
    return _globals.app

class _globals:
    game_thread: threading.Thread = None
    stop_thread: bool = False
    app: GameApp = None

# Run the server
async def main():
    print( "Setting up database" )
    dbGlobal.db = setup_database()  # Initialize database
    dbGlobal.start_edit()
    dbGlobal.end_edit()
    _globals.game_thread = threading.Thread(target=game_start)
    _globals.game_thread.start()

    print( "Starting websocket server" )
    try:
        async with websockets.serve( handle_connection, SHOST, SPORT ):
            await asyncio.Future()  # run forever
    finally:
        exit_handler()

    dbGlobal.db.close()
    _globals.stop_thread = True

def exit_handler():
    if( dbGlobal.db != None ):
        dbGlobal.connection.close()
        dbGlobal.db.close()

    _globals.stop_thread = True
    print( "Exited program" )

if __name__ == "__main__":
    print( "Server starting" )
    atexit.register(exit_handler)
    asyncio.run( main() )

