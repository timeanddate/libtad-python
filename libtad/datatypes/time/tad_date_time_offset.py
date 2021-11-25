from .tad_date_time import TADDateTime
from .tad_time_span import TADTimeSpan

class TADDateTimeOffset:
    """
    A class used to store datetime with offsets.
    
    ...

    Attributes
    ----------
    date_time : TADDateTime
        Storage of time and date.
    time_span : TADTimeSpan
        Offset.
    """

    def __init__(self, date_time: TADDateTime, time_span: TADTimeSpan):
        self.date_time: TADDateTime = date_time
        self.time_span: TADTimeSpan = time_span

    @staticmethod
    def _parse(fmtstr: str) -> "TADDateTimeOffset":
        strlist = fmtstr.split("T")
        if len(strlist) != 2:
            raise ValueError("Cannot parse DateTimeOffset string")

        offset_prefix = None
        if "-" in strlist[1]:
            offset_prefix = "-"
        elif "+" in strlist[1]:
            offset_prefix = "+"

        if offset_prefix:
            last = strlist[1].split(offset_prefix)
            if len(last) != 2:
                raise ValueError("Cannot parse DateTimeOffset string")
            strlist = [strlist[0], last[0], last[1]]

        try:
            datetime = TADDateTime._parse("T".join(strlist[:2]))
            offset_list = [int(num) * int(offset_prefix + "1") for num in strlist[2].split(":")] if offset_prefix else [0, 0]
            if len(offset_list) != 2:
                raise ValueError
        except ValueError:
            raise ValueError("Cannot parse DateTimeOffset string")

        timespan = TADTimeSpan(hours=offset_list[0], minutes=offset_list[1])
        return TADDateTimeOffset(datetime, timespan)

