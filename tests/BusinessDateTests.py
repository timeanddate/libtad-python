import sys
from pathlib import Path


from libtad.business_date_service import BusinessDateService
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.places import LocationId
from libtad.datatypes.business import BusinessFilterMethod, BusinessDaysFilterType, BusinessDaysOperatorType
from configparser import ConfigParser
import unittest

config = ConfigParser()
config.read("tests/config.ini")
access_key = config["tad"]["accessKey"]
secret_key = config["tad"]["secretKey"]

class TestBusinessDateApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBusinessDateApi, self).__init__(*args, **kwargs)
        self.service = BusinessDateService(access_key, secret_key)
        self.result = self.service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), 50)

    def test_geo(self):
        geo = self.result.geo

        self.assertTrue(geo)
        self.assertEqual(geo.name, "Auckland")
        self.assertEqual(geo.state, "Auckland")
        self.assertTrue(geo.country)
        self.assertEqual(geo.country.id, "nz")
        self.assertEqual(geo.country.name, "New Zealand")
        self.assertTrue(geo.coordinates)
        self.assertEqual(round(geo.coordinates.latitude), round(-36.848610))
        self.assertEqual(round(geo.coordinates.longitude), round(174.762497))

    def test_period(self):
        period = self.result.periods[0]

        self.assertTrue(period)
        self.assertEqual(period.included_days, 50)
        self.assertEqual(period.calendar_days, 74)
        self.assertEqual(period.skipped_days, 24)

        sd = period.start_date
        sd_dt = sd.datetime
        self.assertEqual(sd.iso, "2020-04-05")
        self.assertEqual(sd_dt.year, 2020)
        self.assertEqual(sd_dt.month, 4)
        self.assertEqual(sd_dt.day, 5)

        ed = period.end_date
        ed_dt = ed.datetime
        self.assertEqual(ed.iso, "2020-06-18")
        self.assertEqual(ed_dt.year, 2020)
        self.assertEqual(ed_dt.month, 6)
        self.assertEqual(ed_dt.day, 18)

    def test_weekdays(self):
        weekdays = self.result.periods[0].weekdays

        self.assertTrue(weekdays)
        self.assertEqual(weekdays.type, BusinessFilterMethod.Excluded)
        self.assertEqual(weekdays.count, 20)
        self.assertEqual(weekdays.mon, 0)
        self.assertEqual(weekdays.tue, 0)
        self.assertEqual(weekdays.wed, 0)
        self.assertEqual(weekdays.thu, 0)
        self.assertEqual(weekdays.fri, 0)
        self.assertEqual(weekdays.sat, 10)
        self.assertEqual(weekdays.sun, 10)

    def test_holidays(self):
        holidays = self.result.periods[0].holidays

        self.assertTrue(holidays)

        holcount = holidays.count
        self.assertEqual(holidays.type, BusinessFilterMethod.Excluded)
        self.assertEqual(holcount, 4)
        
        hollist = holidays.list
        self.assertTrue(hollist)
        self.assertEqual(len(hollist), holcount)

        hol0 = hollist[0]
        self.assertTrue(hol0)
        self.assertEqual(hol0.id, 1528)
        self.assertEqual(hol0.uid, "0005f800000007e4")
        self.assertEqual(hol0.urlid, "new-zealand/good-friday")
        self.assertTrue(hol0.url)

        self.assertTrue(hol0.name)
        self.assertTrue("en" in hol0.name)
        self.assertEqual(len(hol0.name), 1)
        self.assertEqual(hol0.name["en"], "Good Friday")

        self.assertTrue(hol0.date)
        self.assertEqual(hol0.date.iso, "2020-04-10")

        hol0_dt = hol0.date.datetime
        self.assertTrue(hol0_dt)
        self.assertEqual(hol0_dt.year, 2020)
        self.assertEqual(hol0_dt.month, 4)
        self.assertEqual(hol0_dt.day, 10)

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

    def test_multiple_days(self):
        days = [10, 15, 40]
        result = self.service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), days)
        periods = result.periods

        self.assertIsInstance(periods, list)
        self.assertEqual(len(periods), len(days))
        for i, period in enumerate(periods):
            self.assertEqual(period.included_days, days[i])

    def test_country_input(self):
        result = self.service.get_business_date_for_country("no", TADDateTime(2018, 7, 22), 12)
        geo = result.geo

        self.assertTrue(geo)
        self.assertEqual(geo.country.id, "no")
        self.assertEqual(geo.country.name, "Norway")
        self.assertFalse(geo.state)

        self.assertTrue(result.periods)
        self.assertTrue(result.periods[0])

    def test_country_state_input(self):
        result = self.service.get_business_date_for_country("us", TADDateTime(2018, 7, 22), 12, state_iso="us-ny")
        geo = result.geo

        self.assertTrue(geo)
        self.assertEqual(geo.country.id, "us")
        self.assertEqual(geo.country.name, "United States")
        self.assertEqual(geo.state, "New York")

        self.assertTrue(result.periods)
        self.assertTrue(result.periods[0])

    def test_include(self):
        service = BusinessDateService(access_key, secret_key)
        service.include = True
        result = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), 20)

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

        service = BusinessDateService(access_key, secret_key)
        for f in BusinessDaysFilterType:
            service.include = f in (BusinessDaysFilterType.All,)
            service.filter = f
            result = service.get_business_date_for_place(LocationId(49), TADDateTime(2017, 9, 14), days)
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

    def test_operators(self):
        days = [10, 25, 50]
        service = BusinessDateService(access_key, secret_key)

        service.operator = BusinessDaysOperatorType.Add
        resultAdd = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), days)
        for period in resultAdd.periods:
            sd = period.start_date.datetime
            ed = period.end_date.datetime
            self.assertLessEqual(sd, ed)
        
        service.operator = BusinessDaysOperatorType.Subtract
        resultSub = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), days)
        for period in resultSub.periods:
            sd = period.start_date.datetime
            ed = period.end_date.datetime
            self.assertGreaterEqual(sd, ed)

    def test_repeat(self):
        days = 10
        service = BusinessDateService(access_key, secret_key)
        service.repeat = 3
        result_single = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), days)
        result_list_single = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), [days])

        for result in (result_single, result_list_single):
            periods = result.periods
            self.assertIsInstance(periods, list)
            self.assertEqual(len(periods), service.repeat)
            for period in periods:
                self.included_days = days
        
    def test_repeat_list_multiple(self):
        days = [10, 20]
        service = BusinessDateService(access_key, secret_key)
        service.repeat = 3
        result = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), days)
        
        periods = result.periods
        self.assertIsInstance(periods, list)
        self.assertEqual(len(periods), len(days))
        for i, period in enumerate(periods):
            self.included_days = days[i]

    def test_multiple_filters(self):
        days = 50
        service = BusinessDateService(access_key, secret_key)
        service.filter = [BusinessDaysFilterType.Weekend, BusinessDaysFilterType.Holidays]
        result = service.get_business_date_for_place(LocationId(22), TADDateTime(2020, 4, 5), days)
        self.assertEqual(result.geo.name, "Auckland")


if __name__ == "__main__":
    unittest.main()

