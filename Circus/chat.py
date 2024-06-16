from dialogue import Dialogue

class Chat ( Dialogue ):
    def __init__ ( self ):
        super().__init__( type = 'chat-box', font_size=10, max_lines=8 )