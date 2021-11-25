from libtad.base_service import BaseService
from libtad.datatypes.dst import DST
import libtad.constants as Constants
from libtad.common import XmlUtils
from typing import List, Dict
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext

class DSTService(BaseService):
    """
    The dstlist service can be used to obtain data about time zones for all
    supported countries in our database. This includes the start and end
    date of daylight savings time, and UTC offset for the time zones.

    The resulting data is aggregated on country and time zone level. 
    By default, only information from countries which actually observe DST 
    is returned without listing the individually affected locations – see 
    the parameters listplaces and onlydst to change this behavior.

    ...

    Attributes
    ----------
    include_time_changes : bool
        Add a list of time changes during the year to the dstentry object. 
        This listing e.g. shows changes caused by daylight savings time.

    include_only_dst_countries : bool
        Return only countries which actually observe DST in the queried year. 
        Other countries will be suppressed.

    include_places_for_every_country : bool
        For every time zone/country, list the individual places that belong to
        each record.

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
    get_daylight_saving_time(country_code=None, year=None)
        Gets the daylight saving time by country and year.
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

        super().__init__(access_key, secret_key, "dstlist")
        self.include_time_changes: bool = False
        self.include_only_dst_countries: bool = True
        self.include_places_for_every_country: bool = True

    def get_daylight_saving_time(self, country_code: str = None, year: int = None) -> List[DST]:
        """
        Gets the daylight saving time by country and year.

        If `country_code` is unspecified, information for all countries will be
        returned. If `year` is unspecified, current year is used.

        Parameters
        ----------
        country_code : str, optional
            ISO3166-1-alpha-2 Country Code.
            Uses all countries by default.
        year : int, optional
            Year.
            Uses the current year by default.

        Returns
        -------
        dst_list : list of DST
            The DST information for each country or region.

        """

        args: Dict[str, object] = {}
        
        if country_code and type(country_code) is str:
            args["country"] = country_code
        if year and type(year) is int:
            if year <= 0:
                raise ValueError("An argument is invalid")
            args["year"] = str(year)
            self.include_only_dst_countries = False

        return self.__retrieve_dst_list(args)

    def __retrieve_dst_list(self, args: Dict[str, object]) -> List[DST]:
        args.update(self.__get_arguments())
        url: str = Constants.ENTRYPOINT + "/" + self._service_name + "?" + urlencode(args)
        req = Request(
                url,
                headers = { "User-Agent": "libtad-py"}
                )

        with urlopen(req, context=SSLContext()) as f:
            result: str = f.read().decode("utf-8")

        return self.__from_xml(result)

    def __get_arguments(self) -> Dict[str, object]:
        args: Dict[str, object] = self._authentication_options.copy()
        args["lang"] = ",".join(self.language)
        args["out"] = Constants.DEFAULTRETURNFORMAT
        args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        args["version"] = str(self._version)
        args["timechanges"] = int(self.include_time_changes)
        args["onlydst"] = int(self.include_only_dst_countries)
        args["listplaces"] = int(self.include_places_for_every_country)
        return args

    def __from_xml(self, result: str) -> List[DST]:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        dstlist: ET.Element = xml.find("dstlist")
        return [DST(dstentry) for dstentry in dstlist.findall("dstentry")]

