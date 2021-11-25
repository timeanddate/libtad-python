from .astronomy_event_code import AstronomyEventCode
from libtad.datatypes.time import TADDateTimeOffset
import xml.etree.ElementTree as ET

class AstronomyDayEvent:
    """
    A class used to store events happening at a given day.

    ...

    Attributes
    ----------
    type : AstronomyEventCode
        Indicates the type of the event.
    isotime : TADDateTimeOffset
        Local time at which the event is happening (including UTC offset).
        The time does not include the seconds.
    utctime : TADDateTimeOffset
        UTC time at which the event is happening. The time does not include
        the seconds.
    altitude : float
        Altitude of the center of the queried astronomical object above an
        ideal horizon.

        Only for meridian type events.
    azimuth : float
        Horizontal direction of the astronomical object at set/rise time
        (referring to true north). North is 0 degrees, east is 90 degrees,
        south is 180 degrees and west is 270 degrees.

        Only for rise and set type events.
    distance : float
        Distance of the earth's center to the center of the queried
        astronomical object in kilometers.

        Only for meridian type events.
    illuminated : float
        The fraction of the Moon's surface illuminated by the Sun's
        rays as seen from the selected location.

        Only for the moon for meridian type events.
    posangle : float
        The counterclockwise angle of the midpoint of the Moon's bright limb as seen from the selected location.

        Only for the moon for meridian type events.

    """

    def __init__(self, node: ET.Element):
        self.type: AstronomyEventCode = None
        self.isotime: TADDateTimeOffset = None
        self.utctime: TADDateTimeOffset = None
        self.altitude: float = None
        self.azimuth: float = None
        self.distance: float = None
        self.illuminated: float = None
        self.posangle: float = None
        
        astro_type = node.get("type")
        isotime = node.get("isotime")
        utctime = node.get("utctime")
        altitude = node.get("altitude")
        azimuth = node.get("azimuth")
        distance = node.get("distance")
        illuminated = node.get("illuminated")
        posangle = node.get("posangle")

        if astro_type:
            self.type = AstronomyEventCode.resolve(astro_type)

        if isotime:
            self.isotime = TADDateTimeOffset._parse(isotime)

        if utctime:
            self.utctime = TADDateTimeOffset._parse(utctime)
        
        if altitude:
            self.altitude = float(altitude)

        if azimuth:
            self.azimuth = float(azimuth)

        if distance:
            self.distance = float(distance)

        if illuminated:
            self.illuminated = float(illuminated)

        if posangle:
            self.posangle = float(posangle)

