from . import TADDateTime
import xml.etree.ElementTree as ET

class TimeChange:
    """
    A class used to store information about time change.

    ...

    Attributes
    ----------
    new_daylight_saving_time : int
        New DST offset in seconds. Value will be null if there is
        no DST for this location.
    new_timezone_offset : int
        New timezone offset to UTC in seconds if there is a timezone
        change for this place. Otherwise the value will be null.
        Time zones changes happen only very rarely, so the field will
        be null on most occasions.
    new_total_offset : int
        New total offset to UTC in seconds.
    utc_time : TADDateTime
        The UTC time of the transition.
    old_local_time : TADDateTime
        The old local time before the transition.
    new_local_time : TADDateTime
        The new local time after the transition.
    """

    def __init__(self, node: ET.Element):
        self.new_daylight_saving_time: int = None
        self.new_timezone_offset: int = None
        self.new_total_offset: int = None
        self.utc_time: TADDateTime = None
        self.old_local_time: TADDateTime = None
        self.new_local_time: TADDateTime = None

        newdst = node.get("newdst")
        newzone = node.get("newzone")
        newoffset = node.get("newoffset")
        utctime = node.get("utctime")
        oldlocal = node.get("oldlocaltime")
        newlocal = node.get("newlocaltime")

        if newdst:
            try:
                self.new_daylight_saving_time = int(newdst)
            except ValueError:
                pass

        if newzone:
            try:
                self.new_timezone_offset = int(newzone)
            except ValueError:
                pass

        if newoffset:
            try:
                self.new_total_offset = int(newoffset)
            except ValueError:
                pass

        if utctime:
            self.utc_time = TADDateTime._parse(utctime)

        if oldlocal:
            self.old_local_time = TADDateTime._parse(oldlocal)

        if newlocal:
            self.new_local_time = TADDateTime._parse(newlocal)

