from libtad.datatypes.places import Geo
from .period_type import PeriodType
import xml.etree.ElementTree as ET
from typing import List

class BusinessDates:
    """
    A class used to store geographical information and a list of 
    calculated results for a period.

    ...

    Attributes
    ----------
    geo : Geo
        Geographical information about the location
    periods : list of PeriodType
        List of calculated results for a period.
    """

    def __init__(self, node_geo: ET.Element, node_periods: List[ET.Element]):
        self.geo = Geo(node_geo)
        self.periods = [PeriodType(period) for period in node_periods]

