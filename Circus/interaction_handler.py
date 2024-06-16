class InteractionHandler:
    """Interaction Handler class
    """
    def __init__ ( self ):
        self.registered_interactions = {}

    def register( self, name, func ):
        """Registers an interaction

        Args:
            name (string): identifiable name of an interaction
            func (lambda): function to execute when interaction gets hit
        """
        self.registered_interactions[ name ] = func

    def hit( self, name ):
        """Engages an interaction by its name

        Args:
            name (string): identifiable name of a registered interaction
        """
        self.registered_interactions[ name ]()