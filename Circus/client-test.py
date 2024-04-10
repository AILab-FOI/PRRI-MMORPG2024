import websocket
import threading
import json
import random
import time

def on_message( ws, message ):
    print( f"Received message: {message}" )

def on_error( ws, error ):
    print( f"Error: {error}" )

def on_close( ws, close_status_code, close_msg ):
    print( "### closed ###" )

def on_open( ws ):
    message = json.dumps( { "command":"register", "id": "ivek", "password": 'lozinka' } )
    ws.send( message )
    print( f"Sent: {message}" )
    message = json.dumps( { "command":"login", "id": "ivek", "password": 'lozinka' } )
    ws.send( message )
    print( f"Sent: {message}" )

    def run( *args ):
        for i in range( 10 ):  # Send 10 position updates
            x = random.randint( 0, 100 )
            y = random.randint( 0, 100 )
            message = json.dumps( { "command":"update", "id": "ivek", "position": { "x": x, "y": y } } )
            ws.send( message )
            print( f"Sent: {message}" )
            time.sleep( 1 )  # Sleep for demonstration purposes

        time.sleep( 1 )
        message = json.dumps( { "command":"logout", "id": "ivek", "password": 'lozinka' } )
        ws.send( message )
        print( f"Sent: {message}" )
        ws.close()
        print( "Thread terminating..." )

    thread = threading.Thread( target=run )
    thread.start()

if __name__ == "__main__":
    #websocket.enableTrace( True )
    ws = websocket.WebSocketApp( "ws://localhost:6789",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close )

    ws.run_forever()

