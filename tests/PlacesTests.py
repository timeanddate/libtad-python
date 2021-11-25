import sys
from pathlib import Path


from libtad.places_service import PlacesService
from libtad.datatypes.places import Place
from configparser import ConfigParser
from urllib.parse import urlunparse
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestPlacesApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPlacesApi, self).__init__(*args, **kwargs)
        self.service = PlacesService(access_key, secret_key)
        self.result = self.service.get_places()

    def test_single_place(self):
        place = self.result[21]
        geo = place.geography

        self.assertEqual(place.id, "22")
        self.assertEqual(place.urlid, "new-zealand/auckland")
        self.assertTrue(geo)
        self.assertEqual(geo.name, "Auckland")
        self.assertEqual(geo.state, "Auckland")
        self.assertTrue(geo.country)
        self.assertEqual(geo.country.id, "nz")
        self.assertEqual(geo.country.name, "New Zealand")
        self.assertTrue(geo.coordinates)
        self.assertEqual(geo.coordinates.latitude, -36.849)
        self.assertEqual(geo.coordinates.longitude, 174.762)

    def test_all_places(self):
        for index, place in enumerate(self.result, 1):
            geo = place.geography
            self.assertEqual(place.id, str(index))
            self.assertTrue(place.urlid)
            self.assertTrue(geo)
            self.assertTrue(geo.name)
            self.assertTrue(geo.country)
            self.assertTrue(geo.country.id)
            self.assertTrue(geo.country.name)
            self.assertTrue(geo.coordinates)
            self.assertTrue(geo.coordinates.latitude is not None)
            self.assertTrue(geo.coordinates.longitude is not None)

    def test_no_coords(self):
        service = PlacesService(access_key, secret_key)
        service.include_coordinates = False
        result = service.get_places()

        place = result[21]
        geo = place.geography

        self.assertEqual(place.id, "22")
        self.assertEqual(place.urlid, "new-zealand/auckland")
        self.assertTrue(geo)
        self.assertEqual(geo.name, "Auckland")
        self.assertEqual(geo.state, "Auckland")
        self.assertTrue(geo.country)
        self.assertEqual(geo.country.id, "nz")
        self.assertEqual(geo.country.name, "New Zealand")
        self.assertFalse(geo.coordinates)


if __name__ == "__main__":
    unittest.main()

