#!/usr/bin/env python3


import platform
import asyncio
import logging

from shared import *
from client_app import ClientApp

from scene import LoadingScene

logging.basicConfig(level=logging.INFO)

async def run( app ):
    while True:
        app.tick()
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

    setClientApp( ClientApp( args.username, args.password ) )
    asyncio.run( run( clientApp() ) )
