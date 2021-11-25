from .country import Country
from .coordinates import Coordinates
import xml.etree.ElementTree as ET

class Geo:
    """
    The geographical information type.

    ...

    Attributes
    ----------
    name : str
        The name of the location.
    state : str
        The state of the location within the country (only if applicable).
    country : Country
        Country of the location.
    coordinates : Coordinates
        Geographical coordinates of the location.
    """

    def __init__(self, node: ET.Element):
        self.name: str = None
        self.state: str = None
        self.country: Country = None
        self.coordinates: Coordinates = None

        latitude = node.find("latitude")
        longitude = node.find("longitude")
        name = node.find("name")
        state = node.find("state")
        country = node.find("country")

        if all(l is not None and l.text is not None for l in (latitude, longitude)):
            self.coordinates = Coordinates(float(latitude.text), float(longitude.text))

        if name is not None:
            self.name = name.text

        if state is not None:
            self.state = state.text

        if country is not None:
            self.country = Country(country)

