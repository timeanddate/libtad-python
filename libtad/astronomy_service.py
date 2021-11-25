from libtad.base_service import BaseService
from libtad.datatypes.astro import AstronomyEventClass, AstronomyObjectType, AstronomyLocation
from libtad.datatypes.places import LocationId
from libtad.datatypes.time import TADDateTime
from libtad.common.exceptions import QueriedDateOutOfRangeException
from libtad.common import XmlUtils
import libtad.constants as Constants
from typing import List, Dict
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext

class AstronomyService(BaseService):
    """
    The astronomy service can be used retrieve the sunrise, sunset, moonrise, 
    moonset, solar noon and twilight times for all locations in our database.

    ...

    Attributes
    ----------
    types : AstronomyEventClass
        Selection of which astronomical events you are interested in.
        To combine multiple classes, use the binary OR operator.

        Example:
        ``service.Types = AstronomyEventClass.CivilTwilight | AstronomyEventClass.NauticalTwilight``
    include_coordinates : bool
        Return longitude and latitude for the geo object.
    include_isotime : bool
        Adds timestamps (local time) to all events.
    include_utctime : bool
        Adds UTC timestamps to all events.
    radius : int
        Search radius for translating coordinates (parameter placeid) to locations. 
        Coordinates that could not be translated will yield results for the actual 
        geographical position – if you would like to query for times at an exact 
        location, specify a radius of zero (0).

        The radius in kilometers. Default is infinite, but only locations within 
        the same country and time zone are considered.
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
    get_astronomical_info(object_type, place_id, start_date, end_date=None)
        Gets the specified object type for a specified place by start date.        
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

        super().__init__(access_key, secret_key, "astronomy")
        self.types: AstronomyEventClass = AstronomyEventClass(0)
        self.include_coordinates: bool = True
        self.include_isotime: bool = False
        self.include_utctime: bool = False
        self.radius: int = None

    def get_astronomical_info(self, object_type: AstronomyObjectType, place_id: LocationId, start_date: TADDateTime, end_date: TADDateTime = None) -> List[AstronomyLocation]:
        """
        Gets the specified object type for a specified place by start date.

        Parameters
        ----------
        object_type : AstronomyObjectType
            The astronomical object type.
        place_id : LocationId
            Place identifier.
        start_date : TADDateTime
            Start date.
        end_date : TADDateTime, optional
            End date.
        
        Returns
        -------
        astronomy_locations : list of AstronomyLocation
            A list of astronomical information.

        """

        if type(place_id) is not LocationId or start_date.year == 0 or not object_type:
            raise ValueError("An argument is invalid")

        ID = str(place_id)
        if not ID:
            raise ValueError("An argument is invalid")

        if end_date and end_date < start_date:
            QueriedDateOutOfRangeException("End date cannot be before start date")

        args: Dict[str, object] = self._authentication_options.copy()
        args["placeid"] = place_id
        args["object"] = object_type.name.lower()
        args["startdt"] = str(start_date)
        if end_date:
            args["enddt"] = str(end_date)

        return self.__retrieve_astronomical_info(args)

    def __retrieve_astronomical_info(self, args: Dict[str, object]) -> List[AstronomyLocation]:
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
        types: int = self.__get_astronomy_event_types()

        optional_args["geo"] = int(self.include_coordinates)
        optional_args["isotime"] = int(self.include_isotime)
        optional_args["lang"] = ",".join(self.language)
        optional_args["utctime"] = int(self.include_utctime)
        optional_args["out"] = Constants.DEFAULTRETURNFORMAT
        optional_args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        optional_args["version"] = str(self._version)

        if self.radius is not None:
            optional_args["radius"] = str(self.radius)
        if types:
            optional_args["types"] = types

        return optional_args

    def __from_xml(self, result: str) -> List[AstronomyLocation]:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return [AstronomyLocation(location) for location in xml.findall("location")]

    def __get_astronomy_event_types(self) -> str:
        included_strings: List[str] = []
        for astro_item in AstronomyEventClass:
            if astro_item & self.types:
                included_strings.append(AstronomyEventClass.resolve(astro_item)[1])
        included: str = ",".join(included_strings)
        return included

