import sys
from pathlib import Path


from libtad.holidays_service import HolidaysService
from libtad.datatypes.holidays import HolidayType
from configparser import ConfigParser
from urllib.parse import urlunparse
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestHolidaysApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHolidaysApi, self).__init__(*args, **kwargs)
        self.service = HolidaysService(access_key, secret_key)

    def test_country_year(self):
        hol_list = self.service.holidays_for_country("us", 2014)
        first_holiday = hol_list[0]

        self.assertIsNotNone(first_holiday)
        self.assertEqual("New Year's Day", first_holiday.name["en"])
        self.assertEqual("0007d600000007de", first_holiday.uid)
        self.assertEqual("https://www.timeanddate.com/holidays/us/new-year-day", urlunparse(first_holiday.url))
        self.assertEqual(2006, first_holiday.id)
        self.assertEqual("2014-01-01", first_holiday.date.iso)

    def test_states(self):
        hol_list = self.service.holidays_for_country("us", 2021)
        first_holiday = next(hol for hol in hol_list if hol.states)
        
        self.assertIsNotNone(first_holiday)
        self.assertIsNotNone(first_holiday.states)
        self.assertEqual("District of Columbia", first_holiday.states[0].name)

    def test_types(self):
        service_custom = HolidaysService(access_key, secret_key)
        service_custom.types = HolidayType.Christian | HolidayType.Buddhism
        hol_list = service_custom.holidays_for_country("us", 2014)
        first_holiday = hol_list[0]

        self.assertEqual(27, len(hol_list))
        self.assertTrue(all("Christian" in hol.types or "Buddhism" in hol.types for hol in hol_list))
        self.assertTrue(all(hol.country.id == "us" for hol in hol_list))
        self.assertTrue(first_holiday.oneliner)
        self.assertTrue(first_holiday.uid)
        self.assertIsNotNone(first_holiday.url)
        self.assertTrue(urlunparse(first_holiday.url))

    def test_langs(self):
        service_custom = HolidaysService(access_key, secret_key)
        service_custom.language = ["en", "de"]
        hol_list = service_custom.holidays_for_country("us", 2021)
        first_holiday = hol_list[0]

        self.assertIsNotNone(first_holiday.name)
        self.assertIsNotNone(first_holiday.oneliner)
        for lang in service_custom.language:
            self.assertIsNotNone(first_holiday.name[lang])
            self.assertIsNotNone(first_holiday.oneliner[lang])

        self.assertEqual("Neujahrstag", first_holiday.name["de"])
        self.assertEqual("Der Neujahrstag ist der erste Tag des Jahres im gregorianischen Kalender.", first_holiday.oneliner["de"])


if __name__ == "__main__":
    unittest.main()

