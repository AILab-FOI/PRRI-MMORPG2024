from settings import *
from interactible import Interactible
from interface import Interface

class DialogueInterface ( Interface ):
    def __init__(self, app, name):
        super().__init__( app, name )
        self.quest = QUEST_ATTRS[ name ]

    def update( self ):
        super().update()
    
    def get_image( self ):
        super().get_image()
        #dialogue text here