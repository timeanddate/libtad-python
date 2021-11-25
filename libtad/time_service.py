from libtad.base_service import BaseService
from libtad.datatypes.places import LocationId, Location
from libtad.common import XmlUtils
import libtad.constants as Constants
from typing import List, Dict, Union
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext
import xml.etree.ElementTree as ET

class TimeService(BaseService):
    """
    The timeservice service can be used to retrieve the current time in one 
    or more places. Additionally, information about time zones and related 
    changes and the time of sunrise and sunset can be queried.

    ...

    Attributes
    ----------
    radius : int
        Search radius for translating coordinates (parameter placeid) to locations. 
        Coordinates that could not be translated will yield results for the actual 
        geographical position.

        The radius in kilometers. Default is infinite, but only locations within 
        the same country and time zone are considered.
    include_coordinates : bool
        Return coordinates for the Geography object.
    include_sunrise_and_sunset : bool
        Controls if the astronomy element with information about sunrise and 
        sunset shall be added to the result.
    include_current_time_to_location : bool
        Adds current time under the location object.
    include_list_of_time_changes : bool
        Add a list of time changes during the year to the location object. This 
        listing e.g. shows changes caused by daylight savings time.
    include_timezone_information : bool
        Add timezone information under the time object.

    Methods
    -------
    current_time_for_place(place_id)
        Retrieves the current time for place by ID.
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

        super().__init__(access_key, secret_key, "timeservice")
        self.radius: int = None
        self.include_coordinates: bool = True
        self.include_sunrise_and_sunset: bool = True
        self.include_current_time_to_location: bool = True
        self.include_list_of_time_changes: bool = True
        self.include_timezone_information: bool = True

    def current_time_for_place(self, place_id: Union[LocationId, List[LocationId]]) -> List[Location]:
        """
        Retrieves the current time for place by ID.

        Parameters
        ----------
        place_id : LocationId or list of LocationId
            Place identifier.

        Returns
        -------
        location_times : list of Location
            The current time for place.

        """

        place_id_str = ""
        if isinstance(place_id, LocationId):
            place_id_str = str(place_id)
        elif isinstance(place_id, list) and all(isinstance(pid, LocationId) for pid in place_id):
            place_id_str = ",".join([str(pid) for pid in place_id])

        if not place_id_str:
            raise ValueError("An argument is invalid")

        args: Dict[str, object] = self._authentication_options.copy()
        args["placeid"] = place_id_str

        return self.__retrieve_current_time(args)

    def __retrieve_current_time(self, args: Dict[str, object]) -> List[Location]:
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
        args["geo"] = int(self.include_coordinates)
        args["lang"] = ",".join(self.language)
        args["sun"] = int(self.include_sunrise_and_sunset)
        args["time"] = int(self.include_current_time_to_location)
        args["timechanges"] = int(self.include_list_of_time_changes)
        args["tz"] = int(self.include_timezone_information)
        args["out"] = Constants.DEFAULTRETURNFORMAT
        args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        args["version"] = str(self._version)

        if self.radius is not None:
            args["radius"] = self.radius

        return args
    
    def __from_xml(self, result: str) -> List[Location]:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return [Location(loc) for loc in xml.findall("location")]

