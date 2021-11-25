from .astronomy_special_type import AstronomySpecialType
from libtad.common.exceptions import MalformedXMLException
import xml.etree.ElementTree as ET

class AstronomySpecial:
    """
    This element is only present if there are no astronomical events.

    ...

    Attributes
    ----------
    type : AstronomySpecialType
        Indicates if the sun is up or down all day.
    """

    def __init__(self, node: ET.Element):
        self.type: AstronomySpecialType = None

        type_ = node.get("type")

        if type_:
            type_cap = type_.capitalize()
            try:
                self.type = AstronomySpecialType[type_.capitalize()]
            except KeyError:
                pass

        if not self.type:
            raise MalformedXMLException("The XML Received from Time and Date did not include an event type which complies with an AstronomySpecialType enum", 
                    ignore_default=True)

