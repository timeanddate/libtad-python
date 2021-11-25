MICROINSEC = 100000
SEC = 1
SECINMIN = 60
SECINHOUR = SECINMIN * 60
SECINDAY = SECINHOUR * 24


class TADTimeSpan:
    '''
    A class used to store timespans.
    
    ...

    Methods
    -------
    get_in_microseconds()
        Used to get timespan in microseconds.
    get_in_seconds()
        Used to get timespan in seconds.
    get_in_minutes()
        Used to get timespan in minutes.
    get_in_hours()
        Used to get timespan in hours.
    get_in_days()
        Used to get timespan in days.
    add(days, hours, minutes, seconds, microseconds)
        Adds a given timespan.
    '''

    def __init__(self,
                 days: int = 0,
                 hours: int = 0,
                 minutes: int = 0,
                 seconds: int = 0,
                 microseconds: int = 0):
        '''
        Parameters
        ----------
        days : str
            Days.
        hours : str
            Hours.
        minutes : str
            Minutes.
        seconds : str
            Seconds.
        microseconds : str
            Microseconds.
        '''

        self.__seconds: int = seconds
        self.__seconds += minutes * SECINMIN
        self.__seconds += hours * SECINHOUR
        self.__seconds += days * SECINDAY
        self.__microseconds: int = microseconds
    
    def get_in_microseconds(self) -> int:
        return self.__microseconds + self.__seconds * MICROINSEC

    def get_in_seconds(self) -> int:
        return self.__seconds

    def get_in_minutes(self) -> int:
        return self.__seconds // SECINMIN

    def get_in_hours(self) -> int:
        return self.__seconds // SECINHOUR

    def get_in_days(self) -> int:
        return self.__seconds // SECINDAY

    def add(self,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
            microseconds: int = 0) -> None: 

        self.__seconds += seconds
        self.__seconds += minutes * SECINMIN
        self.__seconds += hours * SECINHOUR
        self.__seconds += days * SECINDAY
        self.__microseconds += microseconds

    def _parse_and_add(self, offset: str) -> None:
        if not offset:
            raise ValueError("Cannot parse TimeSpan string")

        if "-" in offset:
            offset_prefix = -1
            offset = offset[1:]
        else:
            if "+" in offset:
                offset = offset[1:]
            offset_prefix = 1

        try:
            offset_list = [int(num) * offset_prefix for num in offset.split(":")]
            if len(offset_list) == 2:
                offset_list.append(0)
            if len(offset_list) != 3:
                raise ValueError
        except ValueError:
            raise ValueError("Cannot parse TimeSpan string")

        self.add(hours=offset_list[0], minutes=offset_list[1], seconds=offset_list[2])

    @staticmethod
    def _parse(offset: str) -> "TADTimeSpan":
        time_span = TADTimeSpan()
        time_span._parse_and_add(offset)
        return time_span

