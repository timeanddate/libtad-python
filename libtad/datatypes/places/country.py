import xml.etree.ElementTree as ET

class Country:
    '''
    A class used for country data

    ...

    Attributes
    ----------
    id : str
        The ISO 3166-1-alpha-2 country code.
    name : str
        Full name of the country.
    '''

    def __init__(self, node: ET.Element):
        self.id: str = None
        self.name: str = None

        if node is not None and node.text:
            self.name = node.text
            cid = node.get("id")
            if cid:
                self.id = cid

