from libtad.datatypes.time import TADTime
from libtad.datatypes.places import Location
import xml.etree.ElementTree as ET
from typing import List

class ConvertedTimes:
    """
    An object containing UTC time stamp of requested time and a list of time
    information for the locations in the request.

    ...

    Attributes
    ----------
    utc : TADTime
        UTC time stamp of requested time.
    locations : list of Location
        This element contains the time information for the locations mentioned 
        in the request.
    """

    def __init__(self, node_utc: ET.Element, node_locations: List[ET.Element]):
        self.utc: TADTime = None
        self.locations: List[Location] = []

        time = node_utc.find("time")

        if time is not None:
            self.utc = TADTime(time)

        if node_locations:
            self.locations = [Location(loc) for loc in node_locations]

