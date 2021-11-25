from libtad.base_service import BaseService
from libtad.datatypes.places import Place
from libtad.common import XmlUtils
import libtad.constants as Constants
import xml.etree.ElementTree as ET
from urllib.parse import ParseResult, urlunparse, urlencode
from urllib.request import urlopen, Request
from ssl import SSLContext
from typing import List, Dict


class PlacesService(BaseService):
    """
    The places service can be used to retrieve the list of supported places. 

    ...

    Attributes
    ----------
    include_coordinates : bool
        Return coordinates for the Geography object.

    Methods
    -------
    get_places()
        Gets list of supported places.
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

        super().__init__(access_key, secret_key, "places")
        self.include_coordinates: bool = True

    def get_places(self) -> List[Place]:
        """
        Gets list of supported places.

        Returns
        -------
        places : list of Place
            List of all currently known places, their identifiers and their 
            geographical location (if requested).

        """

        args = self.__get_arguments()
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
        args["geo"] = int(self.include_coordinates)
        args["version"] = str(self._version)
        args["out"] = Constants.DEFAULTRETURNFORMAT
        args["verbosetime"] = str(Constants.DEFAULTVERBOSETIMEVALUE)

        return args

    def __from_xml(self, result: str) -> List[Place]:
        XmlUtils.check_for_errors(result)
        xml: ET.Element = ET.fromstring(result)
        places = xml.find("places")
        return [Place(place_node) for place_node in places.findall("place")]

