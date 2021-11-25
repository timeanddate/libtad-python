from .geo import Geo
import xml.etree.ElementTree as ET

class Place:
    """
    A class used for places

    ...

    Attributes
    ----------
    id : int
        Numerical id of the referenced place.
    urlid : str
        Textual id of the referenced place.
    geography : Geo
        Geographical information about the location.
    """

    def __init__(self, node: ET.Element):
        self.id: int = None
        self.urlid: str = ""
        self.geography: Geo = None

        ID = node.get("id")
        urlid = node.get("urlid")
        geo = node.find("geo")

        if ID:
            self.id = ID

        if urlid:
            self.urlid = urlid

        if geo is not None:
            self.geography = Geo(geo)

