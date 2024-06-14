#!/usr/bin/env python3
import asyncio
import websockets
import logging
logging.basicConfig(level=logging.INFO)

import json
from ZEO.ClientStorage import ClientStorage
from ZODB import DB, Connection
import transaction
from BTrees.OOBTree import OOBTree
import persistent

import atexit

from config import SHOST, SPORT, DBHOST, DBPORT

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
        self.logged_in = False

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

    def update( self, x, y ):
        if self.logged_in:
            self.x = x
            self.y = y

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
            logging.info( f"Messages left: {len(websocket.messages)}" )
            logging.info( f"Message received: {message}" )
            # Handle incoming messages...
            data = json.loads( message )

            try:
                if data[ 'command' ] == 'register':
                    if register_player( data[ 'id' ], data[ 'password' ] ):
                        if( login_player( data[ 'id' ], data[ 'password' ] ) ):
                            await send_message_to_player(websocket, {"command": "login_successful"})
                        
                        await broadcast_positions()
                    else:
                        logging.info( f'Error registring: username already taken {data}' )
                elif data[ 'command' ] == 'login':
                    if not login_player( data[ 'id' ], data[ 'password' ] ):
                        await send_message_to_player( websocket, {"command": "login_failed", "data":"player_doesnt_exist"} )
                    else:
                        await send_message_to_player(websocket, {"command": "login_successful"})
                        logging.info( f'Invalid login attempt {data}' )							  
                elif data[ 'command' ] == 'logout':
                    logout_player( data[ 'id' ], data[ 'password' ] )
                    logging.info( f'User logged out {data}' )
                elif data[ 'command' ] == 'update':
                    player_id = data[ 'id' ]
                    position = data[ 'position' ]
                    
                    next_message = get_next_message(websocket)

                    # Skip our current update if we have a newer one on the next frame
                    if( next_message and next_message[ 'command' ] == 'update' 
                       and next_message['id'] == player_id ):
                        continue

                    update_player_position( player_id, position[ 'x' ], position[ 'y' ] )
                elif data[ 'command' ] == 'chat_message':
                    # Dodajte logiku za distribuciju chat poruke ostalim klijentima
                    sender = data['sender']
                    message = data['message']
                    logging.info(f"Received chat message from {sender}: {message}")

                    # Ovdje dodajte logiku za distribuciju poruke ostalim klijentima
                    await broadcast_message_to_all(data)
                else:
                    print( 'Invalid command', data )
            except Exception as e:
                connected_clients.remove( websocket )
                logging.info( f'Invalid message {data} {str(e)}' )
            
            await broadcast_positions()
            #await websocket.ping()  
    except websockets.exceptions.ConnectionClosedOK as e:
        logging.warning(f"Connection handled successfully: {e.reason} {e.code}")
        logging.warning(f"Command: {data}")
    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"Connection closed: {e.reason} {e.code}")
        logging.warning(f"Command: {data}")
        connected_clients.remove( websocket )
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
    finally:
        logging.info("Connection handler exiting")

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
def update_player_position( player_id: str, x: float, y: float ):
    """_summary_

    Args:
        player_id (str): player's username
        x (float): x coordinate
        y (float): y coordinate
    """  
    #print( f"Updating position of player {player_id} to {x},{y}" ) # Too much clutter
    dbGlobal.start_edit()
    try:
        dbGlobal.root.players[ player_id ].update( x, y )
    except KeyError:
        print( f'No such player {player_id}' )
    dbGlobal.end_edit()

# Broadcast positions to all clients
async def send_message_to_player( client, object ):  
    # Send to all connected clients
    message = json.dumps( object )
    logging.info(f"Sending message{message} to client {client}")
    await client.send( message )

async def broadcast_message_to_all( object ):
    message = json.dumps( object )
    await asyncio.gather( *( client.send( message ) for client in connected_clients ) )

# Broadcast positions to all clients
async def broadcast_positions():
    """broadcasts the positions to all clients
    """    
    print( "Broadcasting positions" ) # Too much clutter
    dbGlobal.start_edit()
    object_to_send = {"command": "player_pos"}
    positions = {player_id: {'x': position.x, 'y': position.y} for player_id, position in dbGlobal.root.players.items()}
    object_to_send["data"] = positions

    # Send to all connected clients
    await broadcast_message_to_all( object_to_send )
    dbGlobal.end_edit()

# Run the server
async def main():
    print( "Setting up database" )
    dbGlobal.db = setup_database()  # Initialize database
    dbGlobal.start_edit()
    dbGlobal.end_edit()

    print( "Starting websocket server" )
    async with websockets.serve( handle_connection, SHOST, SPORT ):
        await asyncio.Future()  # run forever

    dbGlobal.db.close()

def exit_handler():
    if( dbGlobal.db != None ):
        dbGlobal.connection.close()
        dbGlobal.db.close()

if __name__ == "__main__":
    print( "Server starting" )
    atexit.register(exit_handler)
    asyncio.run( main() )

