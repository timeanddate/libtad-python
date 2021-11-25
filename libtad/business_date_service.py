import libtad.constants as Constants
from libtad.base_service import BaseService
from libtad.datatypes.business import BusinessDaysOperatorType, BusinessDaysFilterType, BusinessDates
from libtad.datatypes.places import LocationId
from libtad.datatypes.time import TADDateTime
from libtad.common import XmlUtils
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext
from typing import List, Dict, Union

class BusinessDateService(BaseService):
    """
    The businessdate service can be used to find a business date from a 
    specified number of days. 

    You can choose if you want to calculate the business date by 
    adding (default) or subtracting the given days, and whether or not a 
    specific filter should be applied to the result. By default the result 
    will be filtered on excluding weekends and public holidays, but you 
    can specify a custom filter to modify this.   

    ...

    Attributes
    ----------
    include : bool
        Specify whether the result should be calculated by including instead 
        of excluding the days.
    
    filter : BusinessDaysFilterType or list of BusinessDaysFilterType
        Choose a set of types or days you want to filter on.

    operator : BusinessDaysOperatorType
        Set if the service should do an addition or subtraction of the 
        specified days.

    repeat : int
        Set how many times the calculation should be repeated (only applicable 
        when days parameter has exactly one number).

    language : list of str
        The preferred language(s) for the texts. An error will be raised if the
        language code cannot be recognized. In case the text for a specific event
        cannot be retrieved in any of the requested languages it will be returned
        in English instead.

        It is possible to query all available languages in a single request by
        specifying a primary text language, followed by the special value _all_.
        This value can not be specified as the first language.

        Example:
        ``service.language = ["de"]``

        Example:
        ``service.language.append("de")``

    Methods
    -------
    get_business_date_for_place(place_id, start_date, days)
        Gets the business dates by place id.   
    get_business_date_for_country(country_iso, start_date, days, state_iso=None)
        Gets the business dates by country and an optional state.   
    """

    def __init__(self, access_key: str, secret_key: str):
        """
        Parameters
        ----------
        access_key : str
            Access key.
        secret_key : str
            Secret key.
        """

        super().__init__(access_key, secret_key, "businessdate")
        self.include: bool = False
        self.filter: Union[BusinessDaysFilterType, List[BusinessDaysFilterType]] = BusinessDaysFilterType.Weekendholidays
        self.operator: BusinessDaysOperatorType = BusinessDaysOperatorType.Add
        self.repeat: int = 1

    def get_business_date_for_place(self, place_id: LocationId, start_date: TADDateTime, days: Union[int, List[int]]) -> BusinessDates:
        """
        Gets the business dates by place id.   

        Parameters
        ----------
        place_id : LocationId
            Place identifier.
        start_date : TADDateTime
            The first date to count.
        days : int or list of int
            How many business days to count.

        Returns
        -------
        business_dates : BusinessDates
            Object containing geographical information and a list of the 
            calculated result for the requested period.

        """

        if not isinstance(place_id, LocationId):
            raise ValueError("An argument is invalid")

        ID = str(place_id)
        if not ID:
            raise ValueError("An argument is invalid")

        args: Dict[str, object] = {"placeid": ID}
        return self.__get_business_date(args, start_date, days)

    def get_business_date_for_country(self, country_iso: str, start_date: TADDateTime, days: Union[int, List[int]], state_iso: str = None) -> BusinessDates:
        """
        Gets the business dates by country and an optional state.   

        Parameters
        ----------
        country_iso : LocationId
            The country for which you would like to calculate the business date.
        start_date : TADDateTime
            The first date to count.
        days : int or list of int
            How many business days to count.
        state_iso : str, optional
            The state in the given country you want to calculate the business date.
            Uses no states as default.

        Returns
        -------
        business_dates : BusinessDates
            Object containing geographical information and a list of the 
            calculated result for the requested period.

        """

        if not (isinstance(country_iso, str) and (not state_iso or isinstance(state_iso, str))):
            raise ValueError("An argument is invalid")

        args: Dict[str, object] = {"country": country_iso}
        if (state_iso):
            args["state"] = state_iso

        return self.__get_business_date(args, start_date, days)

    def __get_business_date(self, args: Dict[str, object], start_date: TADDateTime, days: Union[int, List[int]]) -> BusinessDates:
        if not isinstance(start_date, TADDateTime):
            raise ValueError("An argument is invalid")

        if isinstance(days, int):
            days_str = str(days)
        elif isinstance(days, list) and all(isinstance(day, int) for day in days):
            days_str = ",".join(map(str, days))
        else:
            raise ValueError("An argument is invalid")

        if isinstance(days, int) or len(days) == 1:
            args["repeat"] = self.repeat

        args.update(self._authentication_options)
        args["startdt"] = str(start_date)
        args["days"] = days_str

        return self.__retrieve_business_date(args)

    def __retrieve_business_date(self, args: Dict[str, object]) -> BusinessDates:
        arguments: Dict[str, object] = self.__get_optional_arguments(args)
        url: str = Constants.ENTRYPOINT + "/" + self._service_name + "?" + urlencode(arguments)
        req = Request(
                url,
                headers = {"User-Agent": "libtad-py"}
                )

        with urlopen(req, context=SSLContext()) as f:
            result: str = f.read().decode("utf-8")

        return self.__from_xml(result)

    def __get_optional_arguments(self, args: Dict[str, object]) -> Dict[str, object]:
        optional_args: Dict[str, str] = args

        optional_args["include"] = int(self.include)
        optional_args["lang"] = ",".join(self.language)
        optional_args["out"] = Constants.DEFAULTRETURNFORMAT
        optional_args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        optional_args["version"] = str(self._version)

        if isinstance(self.filter, BusinessDaysFilterType):
            optional_args["filter"] = str(self.filter)
        elif isinstance(self.filter, list) and all(isinstance(filter, BusinessDaysFilterType) for filter in self.filter):
            optional_args["filter"] = ",".join(map(str, self.filter))

        if isinstance(self.operator, BusinessDaysOperatorType):
            optional_args["op"] = self.operator.name.lower()

        return optional_args

    def __from_xml(self, result: str) -> BusinessDates:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return BusinessDates(xml.find("geo"), [period for period in xml.findall("period")])

