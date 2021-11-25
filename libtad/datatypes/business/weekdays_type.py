from .business_filter_method import BusinessFilterMethod
import xml.etree.ElementTree as ET

class WeekdaysType:
    """
    The spread of excluded or included weekdays.

    ...

    type : BusinessFilterMethod
        Specifies whether or not the weekdays counted were part of an included 
        or excluded filter.
    count : int
        How many days in total have been counted.
    mon : int
        Count for Mondays.
    tue : int
        Count for Tuesdays.
    wed : int
        Count for Wednesdays.
    thu : int
        Count for Thursdays.
    fri : int
        Count for Fridays.
    sat : int
        Count for Saturdays.
    sun : int
        Count for Sundays.
    """

    def __init__(self, node: ET.Element):
        self.type: BusinessFilterMethod = None
        self.count: int = None
        self.mon: int = None
        self.tue: int = None
        self.wed: int = None
        self.thu: int = None
        self.fri: int = None
        self.sat: int = None
        self.sun: int = None

        _type = node.get("type")
        count = node.get("count")
        mon = node.find("mon")
        tue = node.find("tue")
        wed = node.find("wed")
        thu = node.find("thu")
        fri = node.find("fri")
        sat = node.find("sat")
        sun = node.find("sun")

        if _type:
            try:
                self.type = BusinessFilterMethod[_type.capitalize()]
            except KeyError:
                pass

        if count:
            try:
                self.count = int(count)
            except ValueError:
                pass

        if mon is not None:
            try:
                self.mon = int(mon.text)
            except ValueError:
                pass

        if tue is not None:
            try:
                self.tue = int(tue.text)
            except ValueError:
                pass

        if wed is not None:
            try:
                self.wed = int(wed.text)
            except ValueError:
                pass

        if thu is not None:
            try:
                self.thu = int(thu.text)
            except ValueError:
                pass

        if fri is not None:
            try:
                self.fri = int(fri.text)
            except ValueError:
                pass

        if sat is not None:
            try:
                self.sat = int(sat.text)
            except ValueError:
                pass

        if sun is not None:
            try:
                self.sun = int(sun.text)
            except ValueError:
                pass

