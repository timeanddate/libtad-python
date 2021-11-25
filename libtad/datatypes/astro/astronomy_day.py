from libtad.datatypes.time import TADDateTime, TADTimeSpan
from .moon_phase import MoonPhase
from .astronomy_day_event import AstronomyDayEvent
import xml.etree.ElementTree as ET
from typing import List

class AstronomyDay:
    """
    A class used for storing astronomy object information for a given day.

    ...

    Attributes
    ----------
    date : TADDateTime
        Date for the current information.
    day_length : TADTimeSpan
        Length of this day (time between sunrise and sunset). If the sun is not
        up on this day, 00:00 will reported. If the sun does not set on this day,
        the value will read 24:00.
    moonphase : MoonPhase
        Moon phase for the day. Only if requested.
    events : list of AstronomyDayEvent
        Lists all events during the day.

    """

    def __init__(self, node: ET.Element):
        self.date: TADDateTime = None
        self.day_length: TADTimeSpan = None
        self.moonphase: MoonPhase = MoonPhase.NotRequested
        self.events: List[AstronomyDayEvent] = []

        date = node.get("date")
        day_length = node.get("daylength")
        moonphase = node.get("moonphase")
        events = node.findall("event")

        if date:
            self.date = TADDateTime._parse(date)

        if day_length:
            self.day_length = TADTimeSpan._parse(day_length)

        if moonphase:
            phase = MoonPhase._parse(moonphase)
            if phase:
                self.moonphase: MoonPhase = phase

        if events:
            self.events = [AstronomyDayEvent(event) for event in events]

