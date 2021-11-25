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

class BusinessDurationService(BaseService):
    """
    The businessduration service can be used to calculate the number of business
    days between a specified start date and end date.

    When you query the businessduration service with a placeid or a country, a 
    start date and an end date the service will return the number of business 
    days in that date range by excluding public holidays and weekends. 
    Furthermore, you can apply additional filters such as individual days and 
    whether or not the calculation should include the filter result or 
    exclude it.

    ...

    Attributes
    ----------
    include : bool
        Specify whether the result should be calculated by including instead
        of excluding the days.
 
    filter : BusinessDaysFilterType or list of BusinessDaysFilterType
        Choose a set of types or days you want to filter on.

    include_last_date : bool
        Whether or not the last date (end_date) should be counted in the result.

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
    get_business_duration_for_place(place_id, start_date, days)
        Gets the business dates by place id.
    get_business_duration_for_country(country_iso, start_date, days, state_iso=None)
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

        super().__init__(access_key, secret_key, "businessduration")
        self.include: bool = False
        self.filter: Union[BusinessDaysFilterType, List[BusinessDaysFilterType]] = BusinessDaysFilterType.Weekendholidays
        self.include_last_date: bool = False

    def get_business_duration_for_place(self, place_id: LocationId, start_date: TADDateTime, end_date: TADDateTime) -> BusinessDates:
        """
        Gets the business dates by place id.

        Parameters
        ----------
        place_id : LocationId
            Place identifier.
        start_date : TADDateTime
            The first date to count.
        end_date : TADDateTime
            The last date to count.

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
        return self.__get_business_duration(args, start_date, end_date)

    def get_business_duration_for_country(self, country_iso: str, start_date: TADDateTime, end_date: TADDateTime, state_iso: str = None) -> BusinessDates:
        """
        Gets the business dates by country and an optional state.

        Parameters
        ----------
        country_iso : LocationId
            The country for which you would like to calculate the business date.
        start_date : TADDateTime
            The first date to count.
        end_date : TADDateTime
            The last date to count.
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

        return self.__get_business_duration(args, start_date, end_date)

    def __get_business_duration(self, args: Dict[str, object], start_date: TADDateTime, end_date: TADDateTime) -> BusinessDates:
        if not isinstance(start_date, TADDateTime) or not isinstance(end_date, TADDateTime):
            raise ValueError("An argument is invalid")

        if end_date < start_date:
            raise ValueError("End date cannot be before start date")

        args.update(self._authentication_options)
        args["startdt"] = str(start_date)
        args["enddt"] = str(end_date)

        return self.__retrieve_business_duration(args)

    def __retrieve_business_duration(self, args: Dict[str, object]) -> BusinessDates:
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
        optional_args["includelastdate"] = int(self.include_last_date)
        optional_args["lang"] = ",".join(self.language)
        optional_args["out"] = Constants.DEFAULTRETURNFORMAT
        optional_args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        optional_args["version"] = str(self._version)

        if isinstance(self.filter, BusinessDaysFilterType):
            optional_args["filter"] = str(self.filter)
        elif isinstance(self.filter, list) and all(isinstance(filter, BusinessDaysFilterType) for filter in self.filter):
            optional_args["filter"] = ",".join(map(str, self.filter))

        return optional_args

    def __from_xml(self, result: str) -> BusinessDates:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return BusinessDates(xml.find("geo"), [period for period in xml.findall("period")])

