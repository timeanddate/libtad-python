import sys
from pathlib import Path


from libtad.business_duration_service import BusinessDurationService
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.places import LocationId
from libtad.datatypes.business import BusinessFilterMethod, BusinessDaysFilterType, BusinessDaysOperatorType
from configparser import ConfigParser
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestBusinessDurationApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBusinessDurationApi, self).__init__(*args, **kwargs)
        self.service = BusinessDurationService(access_key, secret_key)
        self.result = self.service.get_business_duration_for_place(LocationId(12), TADDateTime(2018, 11, 5), TADDateTime(2019, 1, 24))

    def test_geo(self):
        geo = self.result.geo

        self.assertTrue(geo)
        self.assertEqual(geo.name, "Albany")
        self.assertEqual(geo.state, "New York")
        self.assertTrue(geo.country)
        self.assertEqual(geo.country.id, "us")
        self.assertEqual(geo.country.name, "United States")
        self.assertTrue(geo.coordinates)
        self.assertEqual(round(geo.coordinates.latitude), round(42.651112))
        self.assertEqual(round(geo.coordinates.longitude), round(-73.754723))

    def test_period(self):
        period = self.result.periods[0]

        self.assertTrue(period)
        self.assertEqual(period.included_days, 51)
        self.assertEqual(period.calendar_days, 80)
        self.assertEqual(period.skipped_days, 29)

        sd = period.start_date
        sd_dt = sd.datetime
        self.assertEqual(sd.iso, "2018-11-05")
        self.assertEqual(sd_dt.year, 2018)
        self.assertEqual(sd_dt.month, 11)
        self.assertEqual(sd_dt.day, 5)

        ed = period.end_date
        ed_dt = ed.datetime
        self.assertEqual(ed.iso, "2019-01-24")
        self.assertEqual(ed_dt.year, 2019)
        self.assertEqual(ed_dt.month, 1)
        self.assertEqual(ed_dt.day, 24)

    def test_weekdays(self):
        weekdays = self.result.periods[0].weekdays

        self.assertTrue(weekdays)
        self.assertEqual(weekdays.type, BusinessFilterMethod.Excluded)
        self.assertEqual(weekdays.count, 22)
        self.assertEqual(weekdays.mon, 0)
        self.assertEqual(weekdays.tue, 0)
        self.assertEqual(weekdays.wed, 0)
        self.assertEqual(weekdays.thu, 0)
        self.assertEqual(weekdays.fri, 0)
        self.assertEqual(weekdays.sat, 11)
        self.assertEqual(weekdays.sun, 11)

    def test_holidays(self):
        holidays = self.result.periods[0].holidays

        self.assertTrue(holidays)

        holcount = holidays.count
        self.assertEqual(holidays.type, BusinessFilterMethod.Excluded)
        self.assertEqual(holcount, 7)
        
        hollist = holidays.list
        self.assertTrue(hollist)
        self.assertEqual(len(hollist), holcount)

        hol0 = hollist[0]
        self.assertTrue(hol0)
        self.assertEqual(hol0.id, 2036)
        self.assertEqual(hol0.uid, "0007f405800007e2")
        self.assertEqual(hol0.urlid, "us/election-day")
        self.assertTrue(hol0.url)

        self.assertTrue(hol0.name)
        self.assertTrue("en" in hol0.name)
        self.assertEqual(len(hol0.name), 1)
        self.assertEqual(hol0.name["en"], "Election Day")

        self.assertTrue(hol0.date)
        self.assertEqual(hol0.date.iso, "2018-11-06")

        hol0_dt = hol0.date.datetime
        self.assertTrue(hol0_dt)
        self.assertEqual(hol0_dt.year, 2018)
        self.assertEqual(hol0_dt.month, 11)
        self.assertEqual(hol0_dt.day, 6)

        for hol in hollist[1:]:
            self.assertTrue(hol)
            self.assertTrue(hol.id)
            self.assertTrue(hol.uid)
            self.assertTrue(hol.urlid)
            self.assertTrue(hol.url)

            self.assertTrue(hol.name)
            self.assertTrue("en" in hol.name)
            self.assertTrue(hol.name["en"])

            self.assertTrue(hol.date)
            self.assertTrue(hol.date.iso)

            hol_dt = hol.date.datetime
            self.assertTrue(hol_dt)
            self.assertIsInstance(hol_dt.year, int)
            self.assertIsInstance(hol_dt.month, int)
            self.assertIsInstance(hol_dt.day, int)

    def test_country_input(self):
        result = self.service.get_business_duration_for_country("dk", TADDateTime(2016, 1, 29), TADDateTime(2017, 2, 8))
        geo = result.geo

        self.assertTrue(geo)
        self.assertEqual(geo.country.id, "dk")
        self.assertEqual(geo.country.name, "Denmark")
        self.assertFalse(geo.state)

        self.assertTrue(result.periods)
        self.assertTrue(result.periods[0])

    def test_country_state_input(self):
        result = self.service.get_business_duration_for_country("us", TADDateTime(2018, 7, 22), TADDateTime(2018, 9, 12), state_iso="us-ny")
        geo = result.geo

        self.assertTrue(geo)
        self.assertEqual(geo.country.id, "us")
        self.assertEqual(geo.country.name, "United States")
        self.assertEqual(geo.state, "New York")

        self.assertTrue(result.periods)
        self.assertTrue(result.periods[0])

    def test_include(self):
        service = BusinessDurationService(access_key, secret_key)
        service.include = True
        result = service.get_business_duration_for_place(LocationId(22), TADDateTime(2020, 4, 5), TADDateTime(2020, 5, 2))

        period = result.periods[0]
        self.assertTrue(period)

        weekdays = period.weekdays
        self.assertTrue(weekdays)
        self.assertEqual(weekdays.type, BusinessFilterMethod.Included)

        holidays = period.holidays
        self.assertTrue(holidays)
        self.assertEqual(holidays.type, BusinessFilterMethod.Included)

    def test_filters(self):
        weekday_strs = ["mon", "tue", "wed", "thu", "fri"]
        weekend_strs = ["sat", "sun"]
        days = 50
        start_date = TADDateTime(2017, 9, 14)
        end_date = TADDateTime(2017, 11, 3)

        service = BusinessDurationService(access_key, secret_key)
        for f in BusinessDaysFilterType:
            service.include = f in (BusinessDaysFilterType.All,)
            service.filter = f
            result = service.get_business_duration_for_place(LocationId(49), start_date, end_date)
            weekdays = result.periods[0].weekdays
            fname = str(f)
            fnum = f.value

            if fname in weekday_strs + weekend_strs:
                attr = eval(f"weekdays.{fname}")
                self.assertEqual(attr, weekdays.count)
            elif fname == "all":
                self.assertEqual(weekdays.count, days)
            elif fname == "weekend":
                total = 0
                for d in weekend_strs:
                    total += eval(f"weekdays.{d}")
                self.assertEqual(total, weekdays.count)
            elif fname in ("holidays", "weekendholidays"):
                pass
            elif fname == "none":
                self.assertEqual(weekdays.count, 0)
            else:
                self.assertTrue(0, f"No tests for {f}")

    def test_include_last_date(self):
        start_date = TADDateTime(2016, 8, 12)
        end_date = TADDateTime(2016, 9, 7)
        
        service = BusinessDurationService(access_key, secret_key)
        result = service.get_business_duration_for_place(LocationId(50), start_date, end_date)

        service_include = BusinessDurationService(access_key, secret_key)
        service.include_last_date = True
        result_include = service.get_business_duration_for_place(LocationId(50), start_date, end_date)

        days = result.periods[0].calendar_days
        days_include = result_include.periods[0].calendar_days
        self.assertEqual(days, 26)
        self.assertEqual(days_include, 27)
        self.assertEqual(days + 1, days_include)

    def test_multiple_filters(self):
        start_date = TADDateTime(2016, 8, 12)
        end_date = TADDateTime(2016, 9, 7)

        service = BusinessDurationService(access_key, secret_key)
        service.filter = [BusinessDaysFilterType.Weekend, BusinessDaysFilterType.Holidays]

        result = service.get_business_duration_for_place(LocationId(22), start_date, end_date)
        self.assertEqual(result.geo.name, "Auckland")


if __name__ == "__main__":
    unittest.main()

