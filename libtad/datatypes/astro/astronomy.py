from .astronomy_object_type import AstronomyObjectType
from .astronomy_event import AstronomyEvent
from .astronomy_event_type import AstronomyEventType
from .astronomy_special import AstronomySpecial
from libtad.datatypes.time import TADDateTime
from libtad.common.exceptions import MalformedXMLException
import xml.etree.ElementTree as ET
from typing import List, Union

class Astronomy:
    """
    Astronomical information – sunrise and sunset times. 
    Only for the timeservice and if requested.

    ...

    Attributes
    ----------
    name : AstronomyObjectType
        Object name. Currently, the sun is the only supported astronomical object.
    events : list of AstronomyEvent
        Lists all sunrise/sunset events during the day.
    special : AstronomySpecial
        This element is only present if there are no astronomical events. In this
        case it will indicate if the sun is up or down the whole day.
    """

    def __init__(self, node: ET.Element):
        self.name: AstronomyObjectType = None
        self.events: List[AstronomyEvent] = []
        self.special: AstronomySpecial = None

        name = node.get("name")
        events = node.findall("event")
        special = node.find("special")

        if name:
            object_name = name.capitalize()
            try:
                self.name = AstronomyObjectType[object_name]
            except KeyError:
                pass

        if not self.name:
            raise MalformedXMLException(f"The XML Received from Time and Date did not include an object name which complies with an AstronomyObjectType enum: {name}", 
                    ignore_default=True)

        if events:
            for event in events:
                self.events.append(AstronomyEvent(event))

        if special is not None:
            self.special = AstronomySpecial(special)
            

    @property
    def sunset(self) -> Union[TADDateTime, None]:
        """
        This returns the hour and minute of the sunset in TADDateTime format. If 
        there is no sunset, None will be returned, but the Special-property will 
        say whether or not the sun is up or down.

        Returns
        -------
        sunset : TADDateTime or None
            The sunset in TADDateTime. None if there is no sunset that day.
        """
        sets = [event for event in self.events if event.type == AstronomyEventType.Set]
        if len(sets) == 1:
            return sets[0].time
        elif len(sets) > 1:
            sets.sort(key=lambda x : x.time)
            return sets[-1].time
        else:
            return None

    @property
    def sunrise(self) -> Union[TADDateTime, None]:
        """
        This returns the hour and minute of the sunrise in TADDateTime format. If 
        there is no sunrise, None will be returned, but the Special-property will 
        say whether or not the sun is up or down.

        Returns
        -------
        sunrise : TADDateTime or None
            The sunrise in TADDateTime. None if there is no sunrise that day.
        """
        rises = [event for event in self.events if event.type == AstronomyEventType.Rise]
        if len(rises) == 1:
            return rises[0].time
        elif len(rises) > 1:
            rises.sort(key=lambda x : x.time)
            return rises[-1].time
        else:
            return None

