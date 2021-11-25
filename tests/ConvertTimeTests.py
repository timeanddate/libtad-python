import sys
from pathlib import Path


from libtad.convert_time_service import ConvertTimeService
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.places import LocationId
from configparser import ConfigParser
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestConvertTimeApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestConvertTimeApi, self).__init__(*args, **kwargs)
        self.service = ConvertTimeService(access_key, secret_key)

    def test_utc(self):
        result = self.service.convert_time(LocationId(5), TADDateTime(2020, 5, 21))
        utc = result.utc
        datetime = utc.datetime

        self.assertEqual(utc.iso, "2020-05-20T14:30:00")
        self.assertEqual(datetime.year, 2020)
        self.assertEqual(datetime.month, 5)
        self.assertEqual(datetime.day, 20)
        self.assertEqual(datetime.hour, 14)
        self.assertEqual(datetime.minute, 30)
        self.assertEqual(datetime.second, 0)

    def test_tolocations(self):
        result = self.service.convert_time(LocationId(5), TADDateTime(2020, 5, 21), [LocationId(x) for x in range(1, 4)])
        locations = result.locations
        self.assertEqual(len(locations), 4)

    def test_location_geo(self):
        result = self.service.convert_time(LocationId(5), TADDateTime(2020, 5, 21))
        location = result.locations[0]
        geo = location.geography
        country = geo.country
        coords = geo.coordinates

        self.assertEqual(geo.name, "Adelaide")
        self.assertEqual(geo.state, "South Australia")
        self.assertEqual(country.id, "au")
        self.assertEqual(country.name, "Australia")
        self.assertEqual(coords.latitude, -34.927)
        self.assertEqual(coords.longitude, 138.6)

    def test_location_time(self):
        result = self.service.convert_time(LocationId(5), TADDateTime(2020, 5, 21))
        location = result.locations[0]
        time = location.time
        dt = time.datetime
        tz = time.timezone

        self.assertEqual(time.iso, "2020-05-21T00:00:00+09:30")

        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.month, 5)
        self.assertEqual(dt.day, 21)
        self.assertEqual(dt.hour, 0)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)

        self.assertEqual(tz.abbreviation, "ACST")
        self.assertEqual(tz.name, "Australian Central Standard Time")
        self.assertEqual(tz.offset.get_in_minutes(), 570)
        self.assertEqual(tz.basic_offset, 34200)
        self.assertEqual(tz.dst_offset, 0)
        self.assertEqual(tz.total_offset, 34200)

    def test_location_timechanges(self):
        result = self.service.convert_time(LocationId(5), TADDateTime(2020, 5, 21))
        location = result.locations[0]
        tc = location.time_changes[0]
        utc = tc.utc_time
        old = tc.old_local_time
        new = tc.new_local_time

        self.assertEqual(len(location.time_changes), 2)

        self.assertEqual(tc.new_daylight_saving_time, 0)
        self.assertEqual(tc.new_timezone_offset, None)
        self.assertEqual(tc.new_total_offset, 34200)

        self.assertEqual(utc.year, 2020)
        self.assertEqual(utc.month, 4)
        self.assertEqual(utc.day, 4)
        self.assertEqual(utc.hour, 16)
        self.assertEqual(utc.minute, 30)
        self.assertEqual(utc.second, 0)

        self.assertEqual(old.year, 2020)
        self.assertEqual(old.month, 4)
        self.assertEqual(old.day, 5)
        self.assertEqual(old.hour, 3)
        self.assertEqual(old.minute, 0)
        self.assertEqual(old.second, 0)

        self.assertEqual(new.year, 2020)
        self.assertEqual(new.month, 4)
        self.assertEqual(new.day, 5)
        self.assertEqual(new.hour, 2)
        self.assertEqual(new.minute, 0)
        self.assertEqual(new.second, 0)


if __name__ == "__main__":
    unittest.main()

