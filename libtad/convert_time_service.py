from libtad.base_service import BaseService
from libtad.datatypes.places import LocationId
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.converted_times import ConvertedTimes
from libtad.common import XmlUtils
import libtad.constants as Constants
from typing import List, Dict, Union
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext

class ConvertTimeService(BaseService):
    """
    The converttime service can be used to convert any time from UTC or any of 
    the supported locations to any other of the supported locations.
    ...

    Attributes
    ----------
    radius : int
        Search radius for translating coordinates (parameters fromid and toid)
        to locations. Coordinates that could not be translated will yield results
        for the actual geographical position.
    include_time_changes : bool
        Add a list of time changes during the year to the location object. This listing
        e.g. shows changes caused by daylight savings time.
    include_timezone_information : bool
        Add timezone information under the time object.
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
    convert_time(from_id, time, to_ids=None)
        Converts the time by using a LocationId, a ISO-string and optionally a list 
        of IDs to convert to.
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

        super().__init__(access_key, secret_key, "converttime")
        self.radius: int = None
        self.include_time_changes: bool = True
        self.include_timezone_information: bool = True
        
    def convert_time(self, from_id: LocationId, time: Union[str, TADDateTime], to_ids : List[LocationId] = None) -> ConvertedTimes:
        """
        Converts the time by using a LocationId, a ISO-string and optionally a list
        of IDs to convert to.

        Parameters
        ----------
        from_id : LocationId
            The places identifier.
        time : str or TADDateTime
            ISO 8601-formatted string or TADDateTime object.
        to_ids : list of LocationId, optional
            The place IDs to convert to.
        
        Returns
        -------
        converted_time : ConvertedTimes
            An object containing UTC time stamp of requested time and a list of time 
            information for the locations in the request.

        """

        if (not isinstance(from_id, LocationId)
                or not (isinstance(time, TADDateTime) or isinstance(time, str))
                or not (not to_ids or (isinstance(to_ids, list) and all(isinstance(to_id, LocationId) for to_id in to_ids)))):
            raise ValueError("An argument is invalid")

        from_id_str = str(from_id)
        if isinstance(time, TADDateTime):
            time_str = str(time)

        if not from_id_str or not time_str:
            raise ValueError("An argument is invalid")

        args: Dict[str, object] = self._authentication_options.copy()
        args["fromid"] = from_id_str
        args["iso"] = time_str

        if to_ids:
            args["toid"] = ",".join([str(to_id) for to_id in to_ids])

        return self.__retrieve_converted_times(args)

    def __retrieve_converted_times(self, args: Dict[str, object]) -> ConvertedTimes:
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

        optional_args["timechanges"] = int(self.include_time_changes)
        optional_args["tz"] = int(self.include_timezone_information)
        optional_args["lang"] = ",".join(self.language)
        optional_args["out"] = Constants.DEFAULTRETURNFORMAT
        optional_args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)
        optional_args["version"] = str(self._version)

        if self.radius is not None:
            optional_args["radius"] = str(self.radius)

        return optional_args

    def __from_xml(self, result: str) -> ConvertedTimes:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        return ConvertedTimes(xml.find("utc"), [location for location in xml.findall("location")])

