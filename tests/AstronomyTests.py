import sys
from pathlib import Path


from libtad.astronomy_service import AstronomyService
from libtad.datatypes.astro import AstronomyEventCode, AstronomyEventClass, AstronomyObjectType
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.places import LocationId
from configparser import ConfigParser
from urllib.parse import urlunparse
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestAstronomyApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAstronomyApi, self).__init__(*args, **kwargs)
        self.service = AstronomyService(access_key, secret_key)
        
    def test_all_events(self):
        service = AstronomyService(access_key, secret_key)
        for event in AstronomyEventClass:
            service.types = event
            result = service.get_astronomical_info(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))

    def test_all_astro_objects(self):
        for astro_object in AstronomyObjectType:
            result = self.service.get_astronomical_info(astro_object, LocationId(3), TADDateTime(year=2020, month=3, day=5))
            self.assertTrue(result[0].objects[0].days)

    def test_multiple_days(self):
        service = AstronomyService(access_key, secret_key)
        result = service.get_astronomical_info(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=1), TADDateTime(year=2020, month=3, day=20))

        days = result[0].objects[0].days
        self.assertEqual(20, len(days))

        for day in days:
            self.assertTrue(day.date is not None)
            events = day.events
            self.assertTrue(events)
            for event in events:
                self.assertTrue(event.type)
                self.assertTrue(event.azimuth is not None)

    def test_lang(self):
        service = AstronomyService(access_key, secret_key)
        service.language = ["es"]
        result = service.get_astronomical_info(AstronomyObjectType.Sun, LocationId(187), TADDateTime(year=2020, month=3, day=1))
        self.assertEqual(result[0].geography.country.name, "Noruega")

    def test_geo(self):
        result = self.service.get_astronomical_info(AstronomyObjectType.Sun, LocationId(3), TADDateTime(year=2021, month=3, day=15))
        geo = result[0].geography
        self.assertEqual(geo.name, "Acapulco")
        self.assertEqual(geo.state, "Guerrero")
        self.assertEqual(geo.country.id, "mx")
        self.assertEqual(geo.country.name, "Mexico")
        self.assertEqual(geo.coordinates.latitude, 16.860)
        self.assertEqual(geo.coordinates.longitude, -99.877)
        
    def test_isotime(self):
        service = AstronomyService(access_key, secret_key)
        service.include_isotime = service.include_utctime = True
        result = service.get_astronomical_info(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        isotime = result[0].objects[0].days[0].events[0].isotime
        datetime = isotime.date_time
        timespan = isotime.time_span

        self.assertEqual(datetime.year, 2020)
        self.assertEqual(datetime.month, 3)
        self.assertEqual(datetime.day, 5)
        self.assertEqual(datetime.hour, 3)
        self.assertEqual(datetime.minute, 24)
        self.assertEqual(datetime.second, 58)
        self.assertEqual(timespan.get_in_seconds(), -6 * 3600)

    def test_utctime(self):
        service = AstronomyService(access_key, secret_key)
        service.include_isotime = service.include_utctime = True
        result = service.get_astronomical_info(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        isotime = result[0].objects[0].days[0].events[0].utctime
        datetime = isotime.date_time

        self.assertEqual(datetime.year, 2020)
        self.assertEqual(datetime.month, 3)
        self.assertEqual(datetime.day, 5)
        self.assertEqual(datetime.hour, 9)
        self.assertEqual(datetime.minute, 24)
        self.assertEqual(datetime.second, 58)

    def test_events(self):
        result = self.service.get_astronomical_info(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        
        event0 = result[0].objects[0].days[0].events[0]
        self.assertEqual(event0.type, AstronomyEventCode.Set)
        self.assertEqual(event0.azimuth, 294.4)

        event1 = result[0].objects[0].days[0].events[1]
        self.assertEqual(event1.type, AstronomyEventCode.Rise)
        self.assertEqual(event1.azimuth, 66.0)

    def test_current_event(self):
        service = AstronomyService(access_key, secret_key)
        service.include_isotime = service.include_utctime = True
        service.types = AstronomyEventClass.Current
        result = service.get_astronomical_info(AstronomyObjectType.Moon, LocationId(3), TADDateTime(year=2020, month=3, day=5))
        current = result[0].objects[0].current

        self.assertTrue(current.utctime)
        self.assertTrue(current.isotime)
        self.assertTrue(current.azimuth is not None)
        self.assertTrue(current.altitude is not None)
        self.assertTrue(current.distance is not None)
        self.assertTrue(current.illuminated is not None)
        self.assertTrue(current.posangle is not None)
        self.assertTrue(current.moonphase)


if __name__ == "__main__":
    unittest.main()

