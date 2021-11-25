from .geo import Geo
from libtad.datatypes.astro import Astronomy
from libtad.datatypes.time import TimeChange, TADTime
import xml.etree.ElementTree as ET
from typing import List

class Location:
    """
    An object containing data for location.

    ...

    Attributes
    ----------
    id : str
        The id of the location.
    geography : Geo
        Geographical information about the location.
    time : TADTime
        Time information about the location. Only present if requested.
    time_changes : list of TimeChange
        Time changes (daylight savings time). Only present if requested and 
        information is available.
    astronomy : list of Astronomy
        Astronomical information – sunrise and sunset times.
        Only for the timeservice and if requested.
    """

    def __init__(self, node: ET.Element):
        self.id: str = None
        self.geography: Geo = None
        self.time: TADTime = None
        self.time_changes: List[TimeChange] = []
        self.astronomy: List[Astronomy] = []

        ID = node.get("id")
        geo = node.find("geo")
        time = node.find("time")
        timechanges = node.find("timechanges")
        astronomy = node.find("astronomy")

        if ID:
            self.id = ID

        if geo is not None:
            self.geography = Geo(geo)

        if time is not None:
            self.time = TADTime(time)

        if timechanges is not None:
            self.time_changes = [TimeChange(change) for change in timechanges.findall("change")]

        if astronomy is not None:
            self.astronomy = [Astronomy(obj) for obj in astronomy.findall("object")]

