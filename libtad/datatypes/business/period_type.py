from .weekdays_type import WeekdaysType
from .business_holiday_type import BusinessHolidayType
from libtad.datatypes.time import TADTime
import xml.etree.ElementTree as ET

class PeriodType:
    """
    Calculated result for a given period.

    ...

    Attributes
    ----------
    included_days : int
        Number of days in the given period.
    calendar_days : int
        Number of calendar days in the given period.
    skipped_days : int
        Number of days which was skipped in the given period.
    start_date : TADTime
        The date the period started from.
    end_date : TADTime
        The date the period ended on.
    weekdays : WeekdaysType
        The spread of excluded or included weekdays in included_days.
    holidays : BusinessHolidayType
        Holidays which occur in the given period.
    """

    def __init__(self, node: ET.Element):
        self.included_days: int = None
        self.calendar_days: int = None
        self.skipped_days: int = None
        self.start_date: TADTime = None
        self.end_date: TADTime = None
        self.weekdays: WeekdaysType = None
        self.holidays: BusinessHolidayType = None

        includeddays = node.get("includeddays")
        calendardays = node.get("calendardays")
        skippeddays = node.get("skippeddays")
        startdate = node.find("startdate")
        enddate = node.find("enddate")
        weekdays = node.find("weekdays")
        holidays = node.find("holidays")

        if includeddays:
            try:
                self.included_days = int(includeddays)
            except ValueError:
                pass

        if calendardays:
            try:
                self.calendar_days = int(calendardays)
            except ValueError:
                pass

        if skippeddays:
            try:
                self.skipped_days = int(skippeddays)
            except ValueError:
                pass

        if startdate is not None:
            self.start_date = TADTime(startdate)

        if enddate is not None:
            self.end_date = TADTime(enddate)

        if weekdays is not None:
            self.weekdays = WeekdaysType(weekdays)
            
        if holidays is not None:
            self.holidays = BusinessHolidayType(holidays)

