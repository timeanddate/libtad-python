from .coordinates import Coordinates
from .place import Place
from typing import Union

class LocationId:
    """
    LocationId class represents the different kinds of IDs that Time and Date API
    does support. 

    ...

    Attributes
    ----------
    textual_id : str
        Can be country code, country name, city, etc.
    numeric_id : int
        Usually an integer ID that is returned from a previous API call.
    coordinates : Coordinates
        Provide an coordinate object to LocationId.
    """

    def __init__(self, location: Union[str, int, Coordinates, Place]):
        self.__textual_id: str = None
        self.numeric_id: int = None
        self.__coordinates: Coordinates = None
        
        if type(location) is str:
            self.__textual_id = location
        elif type(location) is int:
            self.numeric_id = location
        elif type(location) is Coordinates:
            self.__coordinates = location
        elif type(location) is Place:
            self.numeric_id = location.id
        else:
            raise ValueError("Location argument must be of type str, int, Coordinates or Place");

    @property
    def textual_id(self) -> str:
        return self.__textual_id

    @property
    def coordinates(self) -> Coordinates:
        return self.__coordinates

    def __str__(self):
        if self.numeric_id is not None:
            return str(self.numeric_id)
        elif self.__textual_id is not None:
            return self.__textual_id
        elif self.__coordinates is not None:
            return str(self.__coordinates)
        else:
            return ""

