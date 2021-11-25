from enum import Enum

class BusinessDaysFilterType(Enum):
    """
    An enum class containing business.PeriodTypeday filters.

    ...

    Attributes
    ----------
    Mon : BusinessDaysFilterType
        Monday.
    Tue : BusinessDaysFilterType
        Tuesday.
    Wed : BusinessDaysFilterType
        Wednesday.
    Thu : BusinessDaysFilterType
        Thursday.
    Fri : BusinessDaysFilterType
        Friday.
    Sat : BusinessDaysFilterType
        Saturday.
    Sun : BusinessDaysFilterType
        Sunday.
    All : BusinessDaysFilterType
        All days.
    Weekend : BusinessDaysFilterType
        Weekend.
    Holidays : BusinessDaysFilterType
        Holidays.
    Weekendholidays : BusinessDaysFilterType
        Weekend and holidays.
    Nothing : BusinessDaysFilterType
        No days.
    """

    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7
    All = 8
    Weekend = 9
    Holidays = 10
    Weekendholidays = 11
    Nothing = 12

    def __str__(self):
        if self == BusinessDaysFilterType.Nothing:
            return "none"
        else:
            return self.name.lower()

