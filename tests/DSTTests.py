import sys
from pathlib import Path


from libtad.dst_service import DSTService
from libtad.datatypes.dst import DST, DSTSpecialType
from configparser import ConfigParser
from urllib.parse import urlunparse
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestDSTApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDSTApi, self).__init__(*args, **kwargs)
        self.service = DSTService(access_key, secret_key)
        self.result = self.service.get_daylight_saving_time()

    def test_all_regions(self):
        regions = [res.region for res in self.result]
        self.assertGreater(len(regions), 0)
        for region in regions:
            self.assertTrue(region.description)
            self.assertTrue(region.biggest_place)

            self.assertTrue(region.country)

            self.assertTrue(region.locations)
            for loc in region.locations:
                self.assertTrue(loc.id)
                self.assertTrue(loc.name)

    def test_all_std_timezones(self):
        std_zones = [res.standard_timezone for res in self.result]
        self.assertGreater(len(std_zones), 0)
        for stdz in std_zones:
            self.assertTrue(stdz)
            self.assertTrue(stdz.abbreviation)
            self.assertTrue(stdz.offset)
            self.assertTrue(stdz.basic_offset is not None)
            self.assertTrue(stdz.dst_offset is not None)
            self.assertTrue(stdz.total_offset is not None)
            if stdz.total_offset != 0:
                self.assertTrue(stdz.name)

    def test_all_dst_timezones(self):
        dst_zones = [res.dst_timezone for res in self.result if res.dst_timezone]
        self.assertTrue(len(dst_zones), 0)
        for dstz in dst_zones:
            self.assertTrue(dstz)
            self.assertTrue(dstz.abbreviation)
            self.assertTrue(dstz.offset)
            self.assertTrue(dstz.basic_offset is not None)
            self.assertTrue(dstz.dst_offset is not None)
            self.assertTrue(dstz.total_offset is not None)
            if dstz.total_offset != 0:
                self.assertTrue(dstz.name)

    def test_all_specials(self):
        specials = [res.special for res in self.result if res.special is not None]
        self.assertGreater(len(specials), 0)
        for s in specials:
            self.assertTrue(s in DSTSpecialType)

    def test_all_dst_start(self):
        dst_starts = [res.dst_start for res in self.result if res.dst_start is not None]
        self.assertGreater(len(dst_starts), 0)
        for ds in dst_starts:
            self.assertTrue(ds)

    def test_all_dst_end(self):
        dst_ends = [res.dst_end for res in self.result if res.dst_end is not None]
        self.assertGreater(len(dst_ends), 0)
        for de in dst_ends:
            self.assertTrue(de)

    def test_all_time_changes(self):
        service = DSTService(access_key, secret_key)
        service.include_time_changes = True
        result = service.get_daylight_saving_time()
        all_time_changes = [res.time_changes for res in result if res.time_changes]
        self.assertGreater(len(all_time_changes), 0)
        for tcs in all_time_changes:
            for tc in tcs:
                self.assertTrue(tc.utc_time)
                self.assertTrue(tc.old_local_time)
                self.assertTrue(tc.new_local_time)
                self.assertIsInstance(tc.new_total_offset, int)
                if tc.new_daylight_saving_time is not None:
                    self.assertIsInstance(tc.new_daylight_saving_time, int)
                if tc.new_timezone_offset is not None:
                    self.assertIsInstance(tc.new_timezone_offset, int)

    def test_exclude_only_dst_countries(self):
        service = DSTService(access_key, secret_key)
        service.include_only_dst_countries = False
        result = service.get_daylight_saving_time()
        self.assertGreater(len(result), 0)
        for res in result:
            pass

    def test_exclude_places_for_every_country(self):
        service = DSTService(access_key, secret_key)
        service.include_places_for_every_country = False
        result = service.get_daylight_saving_time()
        self.assertGreater(len(result), 0)
        locations = [res.region.locations for res in result if res.region.locations]
        self.assertEqual(len(locations), 0)

    def test_single_country(self):
        result = self.service.get_daylight_saving_time("no")
        self.assertEqual(len(result), 1)
        res = result[0]

        region = res.region
        self.assertEqual(region.country.id, "no")
        self.assertEqual(region.country.name, "Norway")
        self.assertEqual(region.description, "All locations")
        self.assertEqual(region.biggest_place, "Oslo")
        self.assertGreater(len(region.locations), 0)

        locations = (
                    ("Oslo", "187", None),
                    ("Longyearbyen", "737", "Svalbard"),
                    )

        for l in locations:
            location = next((loc for loc in region.locations if loc.name.capitalize() == l[0]), None)
            self.assertTrue(location)
            self.assertEqual(location.name, l[0])
            self.assertEqual(location.id, l[1])
            self.assertEqual(location.state, l[2])

    def test_years(self):
        years = {
                2018: (3, 25, 10, 28),
                2019: (3, 31, 10, 27),
                2020: (3, 29, 10, 25),
                }

        for year, value in years.items():
            result = self.service.get_daylight_saving_time("no", year)
            self.assertEqual(len(result), 1)
            res = result[0]

            s = res.dst_start
            self.assertEqual(s.year, year)
            self.assertEqual(s.month, value[0])
            self.assertEqual(s.day, value[1])

            e = res.dst_end
            self.assertEqual(e.year, year)
            self.assertEqual(e.month, value[2])
            self.assertEqual(e.day, value[3])

    def test_single_country_and_year(self):
        result = self.service.get_daylight_saving_time("no", 2020)
        self.assertEqual(len(result), 1)
        res = result[0]

        self.assertEqual(res.standard_timezone.offset.get_in_seconds(), 3600)
        self.assertEqual(res.dst_timezone.offset.get_in_seconds(), 7200)

        s = res.dst_start
        self.assertEqual(s.year, 2020)
        self.assertEqual(s.month, 3)
        self.assertEqual(s.day, 29)

        e = res.dst_end
        self.assertEqual(e.year, 2020)
        self.assertEqual(e.month, 10)
        self.assertEqual(e.day, 25)


if __name__ == "__main__":
    unittest.main()

