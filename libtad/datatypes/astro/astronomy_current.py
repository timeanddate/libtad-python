from libtad.datatypes.time import TADDateTimeOffset
from .moon_phase import MoonPhase
import xml.etree.ElementTree as ET

class AstronomyCurrent:
    """
    A class used to store current data for an astronomy object.

    ...

    Attributes
    ----------
    utctime: TADDateTimeOffset
        UTC time stamp for the data in ISO 8601 format.
    isotime : TADDateTimeOffset
        Local time stamp for the data in ISO 8601 format (including UTC offset).
    azimuth : float 
        Horizontal direction of the astronomical object at set/rise time 
        (referring to true north). North is 0 degrees, east is 90 degrees, south 
        is 180 degrees and west is 270 degrees. 
    altitude : float 
        Altitude of the center of the queried astronomical object above an 
        ideal horizon. 
    distance : float 
        Distance of the earth's center to the center of the queried astronomical 
        object in kilometers. 
    illuminated : float 
        The fraction of the Moon's surface illuminated by the Sun's rays as seen 
        from the selected location. Only available for the moon object. 
    posangle : float 
        The counterclockwise angle of the midpoint of the Moon's bright limb as 
        seen from the selected location. Only available for the moon object. 
    moonphase : MoonPhase
        The current phase of the moon. Only available for the moon object. 
    """

    def __init__(self, node: ET.Element):
        self.utctime: TADDateTimeOffset = None
        self.isotime: TADDateTimeOffset = None
        self.azimuth: float = None
        self.altitude: float = None
        self.distance: float = None
        self.illuminated: float = None
        self.posangle: float = None
        self.moonphase: MoonPhase = MoonPhase.NotRequested

        utctime = node.get("utctime")
        isotime = node.get("isotime")
        azimuth = node.find("azimuth")
        altitude = node.find("altitude")
        distance = node.find("distance")
        illuminated = node.find("illuminated")
        posangle = node.find("posangle")
        moonphase = node.find("moonphase")
        
        if utctime:
            self.utctime = TADDateTimeOffset._parse(utctime)

        if isotime:
            self.isotime = TADDateTimeOffset._parse(isotime)

        if azimuth is not None:
            self.azimuth = float(azimuth.text)

        if altitude is not None:
            self.altitude = float(altitude.text)

        if distance is not None:
            self.distance = float(distance.text)

        if illuminated is not None:
            self.illuminated = float(illuminated.text)

        if posangle is not None:
            self.posangle = float(posangle.text)

        if moonphase is not None:
            self.moonphase = MoonPhase._parse(moonphase.text)

