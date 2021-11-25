from libtad.base_service import BaseService
from libtad.datatypes.holidays import HolidayType, Holiday
from libtad.common import XmlUtils
import libtad.constants as Constants
import xml.etree.ElementTree as ET
from urllib.parse import ParseResult, urlunparse, urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext
from datetime import datetime
from typing import Dict, List


class HolidaysService(BaseService):
    """
    The holidays service can be used to retrieve the list of holidays for a country.

    ...

    Attributes
    ----------
    types : HolidayType
        Holiday types which shoud be returned.
        To combine multiple classes, use the binary OR operator.

        Example:
        ``service.IncludedHolidayTypes = HolidayType.Local``
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
    holidays_for_country(country_code, year=datetime.now().year)
        The holidays service can be used to retrieve the list of holidays for a country.
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

        super().__init__(access_key, secret_key, "holidays")
        self.types: HolidayType = HolidayType(0)

    def __get_holiday_types(self) -> str:
        included_strings: List[str] = []
        for hol_item in HolidayType:
            if self.types & hol_item:
                included_strings.append(HolidayType.resolve(hol_item)[1])
        included: str = ",".join(included_strings)
        return included

    def __from_xml(self, result: str) -> List[Holiday]:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return [Holiday(hol_node) for hol_node in xml.find("holidays")]

    def __get_arguments(self, country_code: str, year: int) -> Dict[str, str]:
        args: Dict[str, object] = self._authentication_options.copy()
        types: str = self.__get_holiday_types()
        args["country"] = country_code
        args["lang"] = ",".join(self.language)
        args["version"] = str(self._version)
        args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        args["out"] = Constants.DEFAULTRETURNFORMAT

        if types:
            args["types"] = types

        if year > 0:
            args["year"] = str(year)

        return args

    def __retrieve_holidays(self, country_code: str, year: int) -> List[Holiday]:
        arguments: Dict[str, str] = self.__get_arguments(country_code, year)
        url: str = Constants.ENTRYPOINT + "/" + self._service_name + "?" + urlencode(arguments)
        req = Request(
                url,
                headers = { "User-Agent": "libtad-py"}
                )

        with urlopen(req, context=SSLContext()) as f:
            result: str = f.read().decode("utf-8")

        return self.__from_xml(result)

    def holidays_for_country(self, country_code: str, year: int = datetime.now().year) -> List[Holiday]:
        """
        The holidays service can be used to retrieve the list of holidays for a country.
        If the argument `year` is not passed in, the current year is used.

        Parameters
        ----------
        country_code : str 
            Specify the ISO3166-1-alpha-2 Country Code for which you would like to 
            retrieve the list of holidays.
        year : int, optional
            The year for which the holidays should be retrieved.            
            Uses the current year by default.

        Returns
        -------
        holiday_list : list of Holiday
            List of holidays for a given country.

        """

        if not country_code or year <= 0:
            raise ValueError("An argument is invalid")
        return self.__retrieve_holidays(country_code, year)

