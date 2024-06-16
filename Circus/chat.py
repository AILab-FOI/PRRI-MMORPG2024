from dialogue import Dialogue
import pygame as pg
from shared import *

class Chat ( Dialogue ):
    def __init__ ( self, max_messages=50 ):
        super().__init__( name = 'chat-box', font_size=10, max_lines=max_messages, color=(150, 150, 150) )
        self.max_messages = max_messages
        self.messages = []
        self.chat_scroll_offset = 0 
        self.active = False
        self.onHold = False
        self.text = ''

        self.chat_display_box = pg.Rect(self.text_pos, (self.text_area[ 'width' ], self.text_area[ 'height' ]))

    def update( self ):
        super().update()
        self.get_dialogue_msg()
        if self.onHold:
            self.onHold = False

    def add_message( self, message ):
        if len(self.messages) >= self.max_lines - 1:
            del self.messages[0]
        self.messages.append( message )

    def get_dialogue_msg( self ):
        msg = ''
        for message in self.messages:
            msg += message + '\n'
        self.set_message( msg, width=5 )
        self.display(offset=self.chat_scroll_offset)
            

    def activate( self ):
        self.active = True
        clientApp().player.inControl = False

        self.onHold = True

    def check_event( self, e ):
        if e.type == pg.MOUSEBUTTONDOWN:
            if self.active and not self.onHold:
                self.active = False
                clientApp().player.inControl = True

        if e.type == pg.KEYDOWN:
            if self.active:
                if e.key == pg.K_RETURN:
                    # Send chat message to server
                    if self.text.strip() != '':
                        clientApp().send_chat_message(self.text)
                        self.active = False
                        clientApp().player.inControl = True
                    self.text = ''
                elif e.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += e.unicode
        # Scroll chat messages
        # NOT CURRENTLY WORKING

        if e.type == pg.MOUSEBUTTONDOWN and self.chat_display_box.collidepoint(e.pos):
            if e.button == 5:  # Scroll down
                self.chat_scroll_offset = min(self.chat_scroll_offset + 10, 0)
            if e.button == 4:  # Scroll up
                self.chat_scroll_offset = max(self.chat_scroll_offset - 10, -max(0, len(self.messages) * 11 - self.chat_display_box.height))
