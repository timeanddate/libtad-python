import sys
from pathlib import Path


from libtad.astrodata_service import AstrodataService
from libtad.datatypes.astro import AstronomyObjectType, MoonPhase
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.places import LocationId, Coordinates
from configparser import ConfigParser
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestAstrodataApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAstrodataApi, self).__init__(*args, **kwargs)
        self.service = AstrodataService(access_key, secret_key)

    def test_by_coordinates(self):
        coordinates = Coordinates(59.743, 10.204)
        result = self.service.get_astrodata(AstronomyObjectType.Moon, LocationId(coordinates), TADDateTime(year=2020, month=3, day=5))
        coords_reply = result[0].geography.coordinates
        self.assertAlmostEqual(coordinates.latitude, coords_reply.latitude)
        self.assertAlmostEqual(coordinates.longitude, coords_reply.longitude)
        self.assertEqual(str(coordinates), str(coords_reply))

    def test_all_astro_objects(self):
        for astro_object in AstronomyObjectType:
            result = self.service.get_astrodata(astro_object, LocationId(3), TADDateTime(year=2020, month=3, day=5))
            self.assertTrue(result[0].objects[0].result)

    def test_multiple_intervals(self):
        service = AstrodataService(access_key, secret_key)
        intervals = [TADDateTime(year=2020, month=m, day=d, hour=5, minute=4, second=s) for m, d, s in zip(range(1, 5), range(5, 9), range(12, 16))]
        result = service.get_astrodata(AstronomyObjectType.Moon, LocationId(3), intervals)

        results = result[0].objects[0].result
        self.assertEqual(4, len(results))

        for res in results:
            self.assertTrue(res is not None)
            self.assertTrue(res.azimuth is not None)
            self.assertTrue(res.altitude is not None)
            self.assertTrue(res.distance is not None)
            self.assertTrue(res.illuminated is not None)
            self.assertTrue(res.posangle is not None)
            self.assertTrue(res.moonphase is not MoonPhase.NotRequested)
            

    def test_lang(self):
        service = AstrodataService(access_key, secret_key)
        service.language = ["es"]
        result = service.get_astrodata(AstronomyObjectType.Sun, LocationId(187), TADDateTime(year=2020, month=3, day=1))
        self.assertEqual(result[0].geography.country.name, "Noruega")

    def test_geo(self):
        result = self.service.get_astrodata(AstronomyObjectType.Sun, LocationId(3), TADDateTime(year=2021, month=3, day=15))
        geo = result[0].geography
        self.assertEqual(geo.name, "Acapulco")
        self.assertEqual(geo.state, "Guerrero")
        self.assertEqual(geo.country.id, "mx")
        self.assertEqual(geo.country.name, "Mexico")
        self.assertEqual(geo.coordinates.latitude, 16.860)
        self.assertEqual(geo.coordinates.longitude, -99.877)
        
    def test_isotime(self):
        service = AstrodataService(access_key, secret_key)
        service.include_isotime = True
        result = service.get_astrodata(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        isotime = result[0].objects[0].result[0].isotime
        datetime = isotime.date_time
        timespan = isotime.time_span

        self.assertEqual(datetime.year, 2020)
        self.assertEqual(datetime.month, 3)
        self.assertEqual(datetime.day, 4)
        self.assertEqual(datetime.hour, 18)
        self.assertEqual(datetime.minute, 0)
        self.assertEqual(datetime.second, 0)
        self.assertEqual(timespan.get_in_seconds(), -6 * 3600)

    def test_utctime(self):
        service = AstrodataService(access_key, secret_key)
        service.include_utctime = True
        result = service.get_astrodata(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        utctime = result[0].objects[0].result[0].utctime
        datetime = utctime.date_time

        self.assertEqual(datetime.year, 2020)
        self.assertEqual(datetime.month, 3)
        self.assertEqual(datetime.day, 5)
        self.assertEqual(datetime.hour, 0)
        self.assertEqual(datetime.minute, 0)
        self.assertEqual(datetime.second, 0)

    def test_islocaltime(self):
        service = AstrodataService(access_key, secret_key)
        result1 = service.get_astrodata(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        service.is_localtime = True
        result2 = service.get_astrodata(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        
        object1 = result1[0].objects[0]
        object2 = result2[0].objects[0]

        self.assertNotEqual(object1.result[0].azimuth, object2.result[0].azimuth);
        self.assertNotEqual(object1.result[0].altitude, object2.result[0].altitude);
        self.assertNotEqual(object1.result[0].distance, object2.result[0].distance);
        self.assertNotEqual(object1.result[0].illuminated, object2.result[0].illuminated);
        self.assertNotEqual(object1.result[0].posangle, object2.result[0].posangle);


if __name__ == "__main__":
    unittest.main()

