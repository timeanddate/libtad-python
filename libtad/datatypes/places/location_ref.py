import xml.etree.ElementTree as ET

class LocationRef:
    """
    A class used for locations referenced by a region.

    ...

    Attributes
    ----------
    id : str
        The id of the location.
    name : str
        The name of the location.
    state : str
        The state of the location within the country (only if applicable).
    """

    def __init__(self, node: ET.Element):
        self.id: str = None
        self.name: str = None
        self.state: str = None

        ID = node.get("id")
        name = node.get("name")
        state = node.get("state")

        if ID:
            self.id = ID

        if name:
            self.name = name

        if state:
            self.state = state

