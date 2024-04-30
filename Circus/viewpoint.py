from shared import *

class Viewpoint(object):
    def __init__( self ):
        self.offset = vec2( 0 )
        self.angle = 0
        self.size = RES
        
    def set_pos( self, pos: vec2 ):
        if( self.offset == pos ):
            return

        self.offset = vec2( pos )
        self.call_viewpoint_update()
    
    def set_ang( self, ang ):
        if( self.angle == ang ):
            return
        
        self.angle = ang
        self.call_viewpoint_update()
    
    def call_viewpoint_update( self ):
        if( clientApp().active_viewpoint != self ):
            return

        clientApp().draw_manager.set_dirty()