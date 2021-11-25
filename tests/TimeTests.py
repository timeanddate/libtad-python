import sys
from pathlib import Path

from libtad.time_service import TimeService
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.places import LocationId
from configparser import ConfigParser
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestTimeApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTimeApi, self).__init__(*args, **kwargs)
        self.service = TimeService(access_key, secret_key)

    def test_locations_argument(self):
        result = self.service.current_time_for_place(LocationId(5))
        many_results = self.service.current_time_for_place([LocationId(lid) for lid in range(1, 20)])
        self.assertEqual(len(result), 1)
        self.assertEqual(len(many_results), 19)

    def test_geo(self):
        result = self.service.current_time_for_place(LocationId(20))
        location = result[0]
        geo = location.geography
        country = geo.country
        coords = geo.coordinates

        self.assertEqual(geo.name, "Antananarivo")
        self.assertEqual(country.id, "mg")
        self.assertEqual(country.name, "Madagascar")
        self.assertEqual(coords.latitude, -18.91)
        self.assertEqual(coords.longitude, 47.526)

    def test_locations(self):
        result = self.service.current_time_for_place([LocationId(lid) for lid in range(50, 70)])
        for location in result:
            time = location.time
            self.assertTrue(time)
            self.assertTrue(time.iso)
            self.assertTrue(time.datetime)
            self.assertTrue(time.timezone)
            self.assertTrue(location.astronomy)
            for astrotype in location.astronomy:
                self.assertTrue(astrotype.name)
                self.assertTrue(astrotype.events)
                for event in astrotype.events:
                    self.assertTrue(event.type)
                    self.assertTrue(event.hour is not None)
                    self.assertTrue(event.minute is not None)
        

if __name__ == "__main__":
    unittest.main()

