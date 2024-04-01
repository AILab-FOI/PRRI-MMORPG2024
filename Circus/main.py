#!/usr/bin/env python3


import platform
import asyncio
import logging

from settings import *
from client import ClientApp

logging.basicConfig(level=logging.INFO)


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

    app = ClientApp( args.username, args.password )
    asyncio.run( run( app ) )
