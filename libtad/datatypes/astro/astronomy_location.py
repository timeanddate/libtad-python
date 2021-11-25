from .astronomy_object_details import AstronomyObjectDetails
from libtad.datatypes.places import Geo
import xml.etree.ElementTree as ET
from typing import List

class AstronomyLocation:
    """
    A class that wraps the information for the locations in the request.

    ...

    Attributes
    ----------
    id : str
        The id of the location.
    geography : Geo
        Geographical information about the location.
    objects : list of AstronomyObjectDetails
        Requested astronomical information.
    """

    def __init__(self, node: ET.Element):
        self.id: str = ""
        self.matchparam: str = ""
        self.geography: Geo = None
        self.objects: List[AstronomyObjectDetails] = []

        ID = node.get("id")
        matchparam = node.get("matchparam")
        geo = node.find("geo")
        astro = node.find("astronomy")

        if ID:
            self.id = ID

        if matchparam:
            self.matchparam = matchparam

        if geo is not None:
            self.geography = Geo(geo)

        if astro is not None:
            for object_node in astro:
                if object_node is not None:
                    self.objects.append(AstronomyObjectDetails(object_node))

