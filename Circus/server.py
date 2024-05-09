#!/usr/bin/env python3
import asyncio
import websockets
import logging
logging.basicConfig(level=logging.INFO)

import json
from ZEO.ClientStorage import ClientStorage
from ZODB import DB
import transaction
from BTrees.OOBTree import OOBTree
import persistent

from config import SHOST, SPORT, DBHOST, DBPORT

def setup_database():
    #print( 'Connecting to ZEO server' ) # Too much clutter
    storage = ClientStorage( ( DBHOST, DBPORT ) )
    db = DB( storage )
    connection = db.open()
    root = connection.root()

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
async def handle_connection( websocket, path: str ):
    """Websocket server handling

    Args:
        websocket ( websocket ): _description_
        path ( string ): _description_
    """    
    # Register websocket connection
    connected_clients.add( websocket )
    
    try:
        
        async for message in websocket:
            data = json.loads( message )
            try:
                if data[ 'command' ] == 'register':
                    if register_player( data[ 'id' ], data[ 'password' ] ):
                        login_player( data[ 'id' ], data[ 'password' ] )
                        await broadcast_positions()
                    else:
                        print( 'Error registring: username already taken', data )
                elif data[ 'command' ] == 'login':
                    if login_player( data[ 'id' ], data[ 'password' ] ):
                        await broadcast_positions()
                    else:
                        print( 'Invalid login attempt', data )
                elif data[ 'command' ] == 'logout':
                    logout_player( data[ 'id' ], data[ 'password' ] )
                    print( 'User logged out', data )
                elif data[ 'command' ] == 'update':
                    player_id = data[ 'id' ]
                    position = data[ 'position' ]
                    update_player_position( player_id, position[ 'x' ], position[ 'y' ] )
                else:
                    print( 'Invalid command', data )
            except Exception as e:
                connected_clients.remove( websocket )
                print( 'Invalid message', data, str( e ) )
            await broadcast_positions()
    except websockets.exceptions.ConnectionClosed:
        print( f"Client {websocket} disconnected" )
        try:
            logout_player( data[ 'id' ], data[ 'password' ] )
            connected_clients.remove( websocket )
        except:
            print( 'Error: Player already logged out', data )

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
            logging.info( f"Message received: {message}" )
            # Handle incoming messages...
            data = json.loads( message )
            try:
                if data[ 'command' ] == 'register':
                    if register_player( data[ 'id' ], data[ 'password' ] ):
                        login_player( data[ 'id' ], data[ 'password' ] )
                        await broadcast_positions()
                    else:
                        logging.info( f'Error registring: username already taken {data}' )
                elif data[ 'command' ] == 'login':
                    if login_player( data[ 'id' ], data[ 'password' ] ):
                        await broadcast_positions()
                    else:
                        logging.info( f'Invalid login attempt {data}' )
                elif data[ 'command' ] == 'logout':
                    logout_player( data[ 'id' ], data[ 'password' ] )
                    logging.info( f'User logged out {data}' )
                elif data[ 'command' ] == 'update':
                    player_id = data[ 'id' ]
                    position = data[ 'position' ]
                    update_player_position( player_id, position[ 'x' ], position[ 'y' ] )
                else:
                    print( 'Invalid command', data )
            except Exception as e:
                connected_clients.remove( websocket )
                logging.info( f'Invalid message {data} {str(e)}' )
            await broadcast_positions()
            #await websocket.ping()  
    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"Connection closed: {e.reason}")
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
    finally:
        logging.info("Connection handler exiting")


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
    db = setup_database()
    connection = db.open()
    root = connection.root()
    if not player_id in root.players:
        root.players[ player_id ] = Player( player_id, password )
        transaction.commit()
        return True
    else:
        print( 'Error: username already taken!' )
        return False
    transaction.commit()
    connection.close()
    db.close()
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
    db = setup_database()
    connection = db.open()
    root = connection.root()
    authenticated = root.players[ player_id ].login( password )
    transaction.commit()
    connection.close()
    db.close()
    return authenticated

def logout_player( player_id: str, password: str ):
    """Logs out the player

    Args:
        player_id ( str ): player's username
        password ( str ): player's password
    """    
    print( f"Logging out player {player_id}" )
    db = setup_database()
    connection = db.open()
    root = connection.root()
    root.players[ player_id ].logout( password )
    transaction.commit()
    connection.close()
    db.close()

# Update player position in the database
def update_player_position( player_id: str, x: float, y: float ):
    """_summary_

    Args:
        player_id (str): player's username
        x (float): x coordinate
        y (float): y coordinate
    """  
    #print( f"Updating position of player {player_id} to {x},{y}" ) # Too much clutter
    db = setup_database()
    connection = db.open()
    root = connection.root()
    try:
        root.players[ player_id ].update( x, y )
    except KeyError:
        print( f'No such player {player_id}' )
    transaction.commit()
    connection.close()
    db.close()

# Broadcast positions to all clients
async def broadcast_positions():
    """broadcasts the positions to all clients
    """    
    #print( "Broadcasting positions" ) # Too much clutter
    db = setup_database()
    connection = db.open()
    root = connection.root()
    positions = {player_id: {'x': position.x, 'y': position.y} for player_id, position in root.players.items()}
    message = json.dumps( positions )
    # Send to all connected clients
    await asyncio.gather( *( client.send( message ) for client in connected_clients ) )
    connection.close()
    db.close()

# Run the server
async def main():
    print( "Setting up database" )
    db = setup_database()  # Initialize database
    db.close()
    print( "Starting websocket server" )
    async with websockets.serve( handle_connection, SHOST, SPORT ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print( "Server starting" )
    asyncio.run( main() )

