class ServerSideException(Exception):
    def __init__(self, message: str):
        super().__init__(f"An error occured on server-side: {message}")

class MalformedXMLException(Exception):
    def __init__(self, message: str, ignore_default=False):
        super().__init__(("The XML returned from Time and Date contained an unsupported name: " if not ignore_default else "") + message)

class QueriedDateOutOfRangeException(Exception):
    pass

