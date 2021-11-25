from .country import Country
from .location_ref import LocationRef
import xml.etree.ElementTree as ET

class Region:
    """
    The geographical region. Contains country, a textual description of 
    the region and the name of the biggest place.

    ...

    Attributes
    ----------
    country : Country
        The country.
    description : str
        Textual description of a region.

        Example: All locations

        Example: most of Newfoundland and Labrador

        Example: some regions of Nunavut Territory; small region of Ontario
    biggest_place : str
        Name of the biggest city within the region.
    locations : list of LocationRef
        A list of all locations referenced by this region. Only returned if 
        requested by specifying the parameter listplaces.
    """

    def __init__(self, node: ET.Element):
        self.country: Country = None
        self.description: str = ""
        self.biggest_place: str = ""
        self.locations: List[LocationRef] = []

        country = node.find("country")
        desc = node.find("desc")
        biggest_place = node.find("biggestplace")
        locations = node.find("locations")

        if country is not None:
            self.country = Country(country)

        if desc is not None:
            self.description = desc.text

        if biggest_place is not None:
            self.biggest_place = biggest_place.text

        if locations is not None:
            self.locations = [LocationRef(location) for location in locations.findall("location")]

