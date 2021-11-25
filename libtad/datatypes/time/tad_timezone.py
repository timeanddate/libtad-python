from .tad_time_span import TADTimeSpan
import xml.etree.ElementTree as ET

class TADTimezone:
    '''
    A class used to store information about timezones.

    ...

    Attributes
    ----------
    abbreviation : str
        Abbreviated timezone name.

        Example: LHDT
    name : str
        Full timezone name.

        Example: Lord Howe Daylight Time
    offset : TADTimeSpan
        The timezone offset (from UTC) as TimeSpan.
    basic_offset : int
        Basic timezone offset (without DST) in seconds.
    dst_offset : int
        DST component of timezone offset in seconds.
    total_offset : int
        Total offset from UTC in seconds.
    '''

    def __init__(self, node: ET.Element):
        self.abbreviation: str = ""
        self.name: str = ""
        self.offset: TADTimeSpan = None
        self.basic_offset: int = None
        self.dst_offset: int = None
        self.total_offset: int = None

        zoneabb_node = node.find("zoneabb")
        name_node = node.find("zonename")
        zoneoffset_node = node.find("zoneoffset")
        zonedst_node = node.find("zonedst")
        totaloffset_node = node.find("zonetotaloffset")
        offset = node.get("offset")

        if zoneabb_node is not None:
            self.abbreviation = zoneabb_node.text

        if name_node is not None:
            self.name = name_node.text

        if zoneoffset_node is not None:
            self.basic_offset = int(zoneoffset_node.text)

        if zonedst_node is not None:
            self.dst_offset = int(zonedst_node.text)

        if totaloffset_node is not None:
            self.total_offset = int(totaloffset_node.text)

        if offset:
            self.offset = TADTimeSpan._parse(offset)

