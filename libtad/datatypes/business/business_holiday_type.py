from .business_filter_method import BusinessFilterMethod
from libtad.datatypes.holidays import Holiday
import xml.etree.ElementTree as ET
from typing import List

class BusinessHolidayType:
    def __init__(self, node: ET.Element):
        """
        Holidays which occur in a given period.

        ...

        Attributes
        ----------
        type : BusinessFilterMethod
            Specifies whether or not the holidays in the result array were 
            included or excluded when queried.
        count : int
            The number of holidays in the results.
        list : list of Holiday
            Holidays which occur in the requested period.
        """

        self.type: BusinessFilterMethod = None
        self.count: int = 0
        self.list: List[Holiday] = []

        _type = node.get("type")
        count = node.get("count")
        _list = node.find("list")

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

        if _list is not None:
            self.list = [Holiday(holiday) for holiday in _list.findall("holiday")]

