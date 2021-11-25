from libtad.base_service import BaseService
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.astro import AstronomyLocation, AstronomyObjectType
from libtad.datatypes.places import LocationId
from libtad.common import XmlUtils
import libtad.constants as Constants
from typing import List, Dict, Union
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext

class AstrodataService(BaseService):
    """
    The astrodata service can be used retrieve the altitude, azimuth and 
    distance to the Moon and the Sun for all locations in our database. The 
    service also returns the moon phase, the fraction of the Moons illuminated 
    side as well as the midpoint angle of the Moons bright limb at any point in 
    time.

    ...

    Attributes
    ----------
    is_localtime : bool
        Whether or not the intervals is in local time for the locations queried 
        or UTC time.        
    include_isotime : bool
        Adds time stamps (local time) in ISO 8601 format to all events.
    include_utctime : bool
        Adds UTC time stamps in ISO 8601 format to all events.
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
    get_astrodata(object_type, place_id, interval)
        Gets astronomical data for an object at a specific place on specific 
        points in time.
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

        super().__init__(access_key, secret_key, "astrodata")
        self.is_localtime: bool = False
        self.include_isotime: bool = False
        self.include_utctime: bool = False
        self.radius: int = None

    def get_astrodata(self, object_type: AstronomyObjectType, place_id: LocationId, interval: Union[TADDateTime, List[TADDateTime]]) -> List[AstronomyLocation]:
        """
        Gets astronomical data for an object at a specific place on specific 
        points in time.

        Parameters
        ----------
        object_type : AstronomyObjectType
            The astronomical object type.
        place_id : LocationId
            Place identifier.
        interval : TADDateTime or list of TADDateTime
            Points in time to query for, using comma to separate multiple 
            timestamps, in ISO 8601 timestamp format.

        Returns
        -------
        astronomy_locations : list of AstronomyLocation
            A list of astronomical information

        """

        if type(interval) is TADDateTime:
            interval = [interval]

        if type(place_id) is not LocationId or not object_type \
                or not interval or type(interval) is not list or type(interval[0]) is not TADDateTime:
            raise ValueError("An argument is invalid")

        ID = str(place_id)
        if not ID:
            raise ValueError("An argument is invalid")

        args: Dict[str, object] = self._authentication_options.copy()
        args["placeid"] = place_id
        args["object"] = object_type.name.lower()
        args["interval"] = ",".join([i._get_second_precision_str() for i in interval])

        return self.__retrieve_astrodata(args)

    def __retrieve_astrodata(self, args: Dict[str, object]) -> List[AstronomyLocation]:
        arguments: Dict[str, object] = self.__get_optional_arguments(args)
        url: str = Constants.ENTRYPOINT + "/" + self._service_name + "?" + urlencode(arguments)
        req = Request(
            url,
            headers = { "User-Agent": "libtad-py"}
            )

        with urlopen(req, context=SSLContext()) as f:
            result: str = f.read().decode("utf-8")

        return self.__from_xml(result)

    def __get_optional_arguments(self, args: Dict[str, object]) -> Dict[str, object]:
        optional_args: Dict[str, str] = args
        
        optional_args["localtime"] = int(self.is_localtime)
        optional_args["isotime"] = int(self.include_isotime)
        optional_args["lang"] = ",".join(self.language)
        optional_args["utctime"] = int(self.include_utctime)
        optional_args["out"] = Constants.DEFAULTRETURNFORMAT
        optional_args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        optional_args["version"] = str(self._version)

        if self.radius is not None:
            optional_args["radius"] = str(self.radius)

        return optional_args

    def __from_xml(self, result: str) -> List[AstronomyLocation]:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return [AstronomyLocation(location) for location in xml.findall("location")]

