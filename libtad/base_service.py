from libtad.authentication import Authentication
import libtad.constants as Constants
from typing import Dict, List

class BaseService:
    def __init__(self, access_key: str, secret_key: str, service_name: str):
        self._version: int = 3
        self.__language: List[str] = [Constants.DEFAULTLANGUAGE]
        self._service_name: str = service_name
        auth = Authentication(service_name, access_key, secret_key)
        self._authentication_options: Dict[str, object] = auth.get_authentication_args()

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if type(value) is str:
            self.__language = [value]
        else:
            self.__language = value

