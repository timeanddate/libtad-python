from .astronomy_event_type import AstronomyEventType
from libtad.common.exceptions import MalformedXMLException
import xml.etree.ElementTree as ET

class AstronomyEvent:
    """
    Contains sunrise/sunset event of a given day.

    ...

    Attributes
    ----------
    type : AstronomyEventType
        Indicates the type of the event.
    hour : int
        Hour at which the event is happening (local time).
    minute : int
        minute at which the event is happening (local time).
    """

    def __init__(self, node: ET.Element):
        self.type: AstronomyEventType = None
        self.hour: int = None
        self.minute: int = None

        type_ = node.get("type")
        hour = node.get("hour")
        minute = node.get("minute")

        if type_:
            try:
                self.type = AstronomyEventType[type_.capitalize()]
            except KeyError:
                pass

        if not self.type:
            raise MalformedXMLException("The XML Received from Time and Date did not "
                + "include an event type which complies with an AstronomyEventType enum: " + type_, ignore_default=True)

        if hour and hour.isdecimal():
            self.hour = int(hour)

        if minute and minute.isdecimal():
            self.minute = int(minute)

