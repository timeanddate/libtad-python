from enum import Flag

class DSTSpecialType(Flag):
    """
        Indicates if the region does not observe DST at all, or is on DST all year long.
    """

    NoDaylightSavingTime = 1
    DaylightSavingTimeAllYear = 1 << 1

    @staticmethod
    def resolve(type_code: str) -> "DSTSpecialType":
        if type_code == "nodst":
            return DSTSpecialType.NoDaylightSavingTime
        elif type_code == "allyear":
            return DSTSpecialType.DaylightSavingTimeAllYear
        else:
            raise ValueError("type_code does not conform to enum DSTSpecialType")

