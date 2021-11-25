from .tad_date_time import TADDateTime
from .tad_timezone import TADTimezone
import xml.etree.ElementTree as ET

class TADTime:
    '''
    A class used to store information about time and timezone.

    ...

    Attributes
    ----------
    iso : str
        ISO representation of date and time, timezone included if
        different from UTC. If time is not applicable, only the
        date is shown.

        Example: 2011-06-08T09:18:16+02:00

        Example: 2011-06-08T07:18:16 (UTC time)

        Example: 2011-06-08 (only date)

    datetime : TADDateTime
        Date and time representation of the ISO string.

    timezone : TADTimezone
        Timezone information. Element is only present if different
        from UTC and requested by specifying the
        IncludeTimezoneInformation parameter.
    '''

    def __init__(self, node: ET.Element):
        self.iso: str = ""
        self.datetime: TADDateTime = None
        self.timezone: TADTimezone = None
        
        iso = node.get("iso")
        timezone = node.find("timezone")
        datetime = node.find("datetime")

        if iso:
            self.iso = iso

        if timezone is not None:
            self.timezone = TADTimezone(timezone)

        if datetime is not None:
            year_node = datetime.find("year")
            month_node = datetime.find("month")
            day_node = datetime.find("day")
            hour_node = datetime.find("hour")
            minute_node = datetime.find("minute")
            second_node = datetime.find("second")

            year = int(year_node.text) if year_node is not None else 0
            month = int(month_node.text) if month_node is not None else 1
            day = int(day_node.text) if day_node is not None else 1
            hour = int(hour_node.text) if hour_node is not None else 0
            minute = int(minute_node.text) if minute_node is not None else 0
            second = int(second_node.text) if second_node is not None else 0

            self.datetime = TADDateTime(year, month, day, hour, minute, second, 0)
        elif self.iso:
            self.datetime = TADDateTime._parse(self.iso)

