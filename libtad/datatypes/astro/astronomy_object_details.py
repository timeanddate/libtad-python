from .astronomy_object_type import AstronomyObjectType
from .astronomy_day import AstronomyDay
from .astronomy_current import AstronomyCurrent
from libtad.common.exceptions import MalformedXMLException
import xml.etree.ElementTree as ET
from typing import List

class AstronomyObjectDetails:
    """
    A class used to store astronomy objects

    ...

    Attributes
    ----------
    name : AstronomyObjectType
        Object name.
    days : list of AstronomyDay
        astronomy service: Lists all the requested days where events are happening.

        astrodata service: N/A
    current : AstronomyCurrent
        astronomy service: The current data for the object. Only if requested.

        astrodata service: N/A
    current : list of AstronomyCurrent
        astronomy service: N/A

        astrodata service: The specific data for the object at isotime/utctime.

    """

    def __init__(self, node: ET.Element):
        self.name: AstronomyObjectType = AstronomyObjectType(0)
        self.days: List[AstronomyDay] = None
        self.current: AstronomyCurrent = None
        self.result: List[AstronomyCurrent] = None

        name = node.get("name")
        days = node.findall("day")
        current = node.find("current")
        results = node.findall("result")
        
        if name and name.capitalize() in AstronomyObjectType.__members__:
            self.name = AstronomyObjectType[name.capitalize()]
        else:
            raise MalformedXMLException(name)
        
        if days:
            self.days = [AstronomyDay(day) for day in days]

        if current is not None:
            self.current = AstronomyCurrent(current)

        if results:
            self.result = [AstronomyCurrent(result) for result in results]

