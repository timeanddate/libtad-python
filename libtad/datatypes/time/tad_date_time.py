class TADDateTime:
    '''
    A class used to store date and time.

    ...

    Attributes
    ----------
    year : int
        Year.
    month : int
        Month.
    day : int
        Day.
    hour : int
        Hour.
    minute : int
        Minute.
    second : int
        Second.
    microsecond : int
        Microsecond.
    '''

    def __init__(self,
                 year:          int = 0,
                 month:         int = 1,
                 day:           int = 1,
                 hour:          int = 0,
                 minute:        int = 0,
                 second:        int = 0,
                 microsecond:   int = 0):
        '''
        Parameters
        ----------
        year : int
            Year.
        month : int
            Month.
        day : int
            Day.
        hour : int
            Hour.
        minute : int
            Minute.
        second : int
            Second.
        microsecond : int
            Microsecond.
        '''

        self.__year:        int = 0
        self.__month:       int = 1
        self.__day:         int = 1
        self.__hour:        int = 0
        self.__minute:      int = 0
        self.__second:      int = 0
        self.__microsecond: int = 0
        
        self.year:          int = year
        self.month:         int = month
        self.day:           int = day
        self.hour:          int = hour
        self.minute:        int = minute
        self.second:        int = second
        self.microsecond:   int = microsecond
        
    @property
    def year(self):
        return self.__year
    
    @year.setter
    def year(self, value: int):
        self.__year = value

    @property
    def month(self):
        return self.__month
    
    @month.setter
    def month(self, value: int):
        start = 1
        end = 12
        if start <= value <= end:
            self.__month = value
        else:
            raise ValueError(f"Month must be an integer between {start} and {end}")
                
    @property
    def day(self):
        return self.__day
    
    @day.setter
    def day(self, value: int):
        start = 1
        end = 31
        if start <= value <= end:
            self.__day = value
        else:
            raise ValueError(f"Day must be an integer between {start} and {end}")
                
    @property
    def hour(self):
        return self.__hour
    
    @hour.setter
    def hour(self, value: int):
        start = 0
        end = 24
        if start <= value <= end:
            self.__hour = value
        else:
            raise ValueError(f"Hour must be an integer between {start} and {end}")
                
    @property
    def minute(self):
        return self.__minute
    
    @minute.setter
    def minute(self, value: int):
        start = 0
        end = 59
        if start <= value <= end:
            self.__minute = value
        else:
            raise ValueError(f"Minute must be an integer between {start} and {end}")

    @property
    def second(self):
        return self.__second
    
    @second.setter
    def second(self, value: int):
        start = 0
        end = 60
        if start <= value <= end:
            self.__second = value
        else:
            raise ValueError(f"Second must be an integer between {start} and {end}")

    @property
    def microsecond(self):
        return self.__microsecond
    
    @microsecond.setter
    def microsecond(self, value: int):
        start = 0
        end = 99999
        if start <= value <= end:
            self.__microsecond = value
        else:
            raise ValueError(f"Microsecond must be an integer between {start} and {end}")

    @staticmethod
    def _parse(fmtstr: str) -> "TADDateTime":
        include_time = "T" in fmtstr

        if include_time:
            strlist = fmtstr.split("T")
            if len(strlist) != 2:
                raise ValueError("Cannot parse DateTime string")
            for char in "+-Z":
                strlist[1] = strlist[1].split(char)[0]
        else:
            strlist = [fmtstr]

        try:
            date_list = [int(num) for num in strlist[0].split("-")]
            time_list = [int(num) for num in strlist[1].split(":")] if include_time else [0] * 3
        except ValueError:
            raise ValueError("Cannot parse DateTime string")

        if len(date_list) != 3 or len(time_list) != 3:
            raise ValueError("Cannot parse DateTime string")

        datetime = TADDateTime(year=date_list[0], month=date_list[1], day=date_list[2], hour=time_list[0], minute=time_list[1], second=time_list[2])
        return datetime

    def _get_day_precision_str(self):
        return f"{str(self.__year).zfill(4)}-{str(self.__month).zfill(2)}-{str(self.__day).zfill(2)}"

    def _get_second_precision_str(self):
        return f"{self._get_day_precision_str()}T{str(self.__hour).zfill(2)}:{str(self.__minute).zfill(2)}:{str(self.__second).zfill(2)}"

    def __eq__(self, value):
        if self.__year == value.__year \
                and self.__month == value.month \
                and self.__day == value.day \
                and self.__hour == value.hour \
                and self.__day == value.day \
                and self.__second == value.second \
                and self.__microsecond == value.microsecond:
            return True
        return False

    def __ne__(self, value):
        return not self.__eq__(value)

    def __lt__(self, value):
        for t in ("year", "month", "day", "hour", "day", "second", "microsecond"):
            self_t = getattr(self, t)
            value_t = getattr(value, t)
            if self_t < value_t:
                return True
            elif self_t > value_t:
                return False
        return False 
    
    def __le__(self, value):
        return self.__lt__(value) or self.__eq__(value)

    def __gt__(self, value):
        return not self.__le__(value)

    def __ge__(self, value):
        return not self.__lt__(value)

    def __str__(self):
        return self._get_second_precision_str()

