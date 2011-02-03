class GameraMeiError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class GameraMeiFormNotFoundError(GameraMeiError): pass
class GameraMeiPitchNotFoundError(GameraMeiError): pass
class GameraMeiNoteIntervalMismatchError(GameraMeiError): pass