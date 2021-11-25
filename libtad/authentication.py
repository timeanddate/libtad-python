import base64, datetime, hashlib, hmac, urllib
from datetime import datetime
from typing import Dict

class Authentication:
    def __init__(self, service: str, access_key: str, secret_key: str):
        self.__service: str = service
        self.__access_key: str = access_key
        self.__secret_key: str = secret_key

    def get_authentication_args(self, seed: Dict[str, object] = None) -> Dict[str, object]:
        timestamp = datetime.utcnow().isoformat()
        message = self.__access_key + self.__service + timestamp;
        digester = hmac.new(bytes(self.__secret_key, encoding="utf8"), bytes(message, encoding="utf8"), hashlib.sha1)

        args: Dict[str, object] = seed if seed is not None else {}
        args["accesskey"] = self.__access_key
        args["timestamp"] = timestamp
        args["signature"] = base64.b64encode(digester.digest())

        return args

