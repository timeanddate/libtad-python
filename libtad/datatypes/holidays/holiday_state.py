import xml.etree.ElementTree as ET

class HolidayState:
    '''
    A class used for holidays in states

    ...

    Attributes
    ----------
    id : int
        Unique id of the state/subdivision. (default is -1)
    iso : str
        An ISO 3166-1 country or ISO 3166-2 country state code (see [ISO3166]).
    abbreviation : str
        Abbreviation of the state/subdivision.
    name : str
        Common name of the state/subdivision.
    exception : str
        Eventual exception if the holiday does not affect
        the whole state/subdivision.
    '''
    def __init__(self, node: ET.Element):
        self.id: int = -1
        self.iso: str = ""
        self.abbreviation: str = ""
        self.name: str = ""
        self.exception: str = ""

        ID = node.find("id")
        iso = node.get("iso")
        abbr = node.find("abbrev")
        name = node.find("name")
        excp = node.find("exception")

        if ID is not None:
            self.id = int(ID.text)

        if iso:
            self.iso = iso

        if abbr is not None:
            self.abbreviation = abbr.text

        if name is not None:
            self.name = name.text

        if excp is not None:
            self.exception = excp.text
    
