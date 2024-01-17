class TabletDisconnected(ConnectionError):
    def __init__(self, message="HUION Tablet not found."):
        self.message = message
        super().__init__(self.message)