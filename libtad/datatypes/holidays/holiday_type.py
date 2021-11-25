from typing import Union, Tuple
from enum import Flag

class HolidayType(Flag):
    '''
        An enum class with simple bitflags so the user can easily put together a set of types
        which should be included or excluded in the retrieval of holidays.
    '''

    All = 1
    Default = 1 << 1
    DefaultForCountry = 1 << 2
    Observances = 1 << 3
    Federal = 1 << 4
    FederalLocal = 1 << 5
    Local = 1 << 6
    Flagdays = 1 << 7
    LocalObservances = 1 << 8
    ImportantObservances = 1 << 9
    CommonObservances = 1 << 10
    OtherObservances = 1 << 11
    Weekdays = 1 << 12
    Buddhism = 1 << 13
    Hebrew = 1 << 14
    Hinduism = 1 << 15
    Muslim = 1 << 16
    Orthodox = 1 << 17
    Seasons = 1 << 18
    TimezoneEvents = 1 << 19
    UnitedNations = 1 << 20
    WorldWideObservances = 1 << 21
    Christian = 1 << 22
    Defacto = 1 << 23
    Religious = 1 << 24
    Halfday = 1 << 25
    Optional = 1 << 26
    Otherreligion = 1 << 27
    Sport = 1 << 28
    Fun = 1 << 29

    @staticmethod
    def resolve(holiday_type: Union[int, str, "HolidayType"]) -> Tuple[int, str, "HolidayType"]:
        tup: Tuple[Tuple[int, str, HolidayType], ...] = (
                    (1, "all", HolidayType.All),
                    (1 << 1, "default", HolidayType.Default),
                    (1 << 2, "countrydefault", HolidayType.DefaultForCountry),
                    (1 << 3, "obs", HolidayType.Observances),
                    (1 << 4, "federal", HolidayType.Federal),
                    (1 << 5, "federallocal", HolidayType.FederalLocal),
                    (1 << 6, "local", HolidayType.Local),
                    (1 << 7, "flagday", HolidayType.Flagdays),
                    (1 << 8, "local2", HolidayType.LocalObservances),
                    (1 << 9, "obs1", HolidayType.ImportantObservances),
                    (1 << 10, "obs2", HolidayType.CommonObservances),
                    (1 << 11, "obs3", HolidayType.OtherObservances),
                    (1 << 12, "weekday", HolidayType.Weekdays),
                    (1 << 13, "buddhism", HolidayType.Buddhism),
                    (1 << 14, "hebrew", HolidayType.Hebrew),
                    (1 << 15, "hinduism", HolidayType.Hinduism),
                    (1 << 16, "muslim", HolidayType.Muslim),
                    (1 << 17, "orthodox", HolidayType.Orthodox),
                    (1 << 18, "seasons", HolidayType.Seasons),
                    (1 << 19, "tz", HolidayType.TimezoneEvents),
                    (1 << 20, "un", HolidayType.UnitedNations),
                    (1 << 21, "world", HolidayType.WorldWideObservances),
                    (1 << 22, "christian", HolidayType.Christian),
                    (1 << 23, "defacto", HolidayType.Defacto),
                    (1 << 24, "religious", HolidayType.Religious),
                    (1 << 25, "halfday", HolidayType.Halfday),
                    (1 << 26, "optional", HolidayType.Optional),
                    (1 << 27, "otherreligion", HolidayType.Otherreligion),
                    (1 << 28, "sport", HolidayType.Sport),
                    (1 << 29, "fun", HolidayType.Fun)
                    )

        if type(holiday_type) is int:
            index = 0
        elif type(holiday_type) is str:
            index = 1
        elif type(holiday_type) is HolidayType:
            index = 2
        else:
            return None

        for hol_entry in tup:
            if holiday_type == hol_entry[index]:
                return hol_entry

