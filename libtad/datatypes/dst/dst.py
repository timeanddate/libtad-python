from .dst_special_type import DSTSpecialType
from libtad.datatypes.places import Region
from libtad.datatypes.time import TimeChange, TADDateTime, TADTimezone
import xml.etree.ElementTree as ET
from typing import List

class DST:
    """
    DST information for a given region.

    ...

    Attributes
    ----------
    region : Region
        The geographical region where this information is valid.
        Contains country, a textual description of the region and
        the name of the biggest place.
    standard_timezone : TADTimezone
        Information about the standard timezone. This element is
        always returned.
    dst_timezone : TADTimezone
        Information about the daylight savings timezone. Suppressed,
        if there are no DST changes in the queried year.

        Please note that if the region is on daylight savings time
        for the whole year, this information will be returned in the
        stdtimezone element. Additionally, the Special element will
        be set to DaylightSavingTimeAllYear.
    special : DSTSpecialType
        Indicates if the region does not observe DST at all, or is on
        DST all year long.
    dst_start : TADDateTime
        Starting date of daylight savings time. Suppressed, if there
        are no DST changes in the queried year.
    dst_end : TADDateTime
        Ending date of daylight savings time. Suppressed, if there are
        no DST changes in the queried year.
    time_changes : list of TimeChange
        Time changes (daylight savings time). Only present if requested
        and information is available.
    """

    def __init__(self, node: ET.Element):
        self.region: Region = None
        self.standard_timezone: TADTimezone = None
        self.dst_timezone: TADTimezone = None
        self.special: DSTSpecialType = None
        self.dst_start: TADDateTime = None
        self.dst_end: TADDateTime = None
        self.time_changes: List[TimeChange] = []

        region = node.find("region")
        stdtimezone = node.find("stdtimezone")
        dsttimezone = node.find("dsttimezone")
        special_node = node.find("special")
        special = special_node.get("type") if special_node is not None else None
        dststart = node.find("dststart")
        dstend = node.find("dstend")
        timechanges = node.find("timechanges")

        if region is not None:
            self.region = Region(region)

        if stdtimezone is not None:
            self.standard_timezone = TADTimezone(stdtimezone)
            
        if dsttimezone is not None:
            self.dst_timezone = TADTimezone(dsttimezone)

        if special:
            self.special = DSTSpecialType.resolve(special)

        if dststart is not None:
            self.dst_start = TADDateTime._parse(dststart.text)

        if dstend is not None:
            self.dst_end = TADDateTime._parse(dstend.text)

        if timechanges is not None:
            self.time_changes = [TimeChange(change) for change in timechanges.findall("change")]

