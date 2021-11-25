class Coordinates:
    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude

    def __str__(self) -> str:
        coords = ""
        lat = self.latitude
        long_ = self.longitude

        if lat >= 0:
            coords += "+"
        coords += str(lat)

        if long_ >= 0:
            coords += "+"
        coords += str(long_)

        return coords

