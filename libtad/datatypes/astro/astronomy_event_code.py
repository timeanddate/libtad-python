from enum import Flag

class AstronomyEventCode(Flag):
    """
    An enum class containing astronomy events.

    ...

    Attributes
    ----------
    AstronomicalTwilightStarts : AstronomyEventCode
        Astronomical twilight (-18°) start.
    NauticalTwilightStarts : AstronomyEventCode
        Nautical twilight (-12°) start.
    CivilTwilightStarts : AstronomyEventCode
        Civil twilight (-6°) start.
    Rise : AstronomyEventCode
        Astronomy object rising.
    Meridian : AstronomyEventCode
        Meridian passing (noon).
    AntiMeridian : AstronomyEventCode
        Antimeridian passing (midnight).
    Set : AstronomyEventCode
        Astronomy object setting.
    CivilTwilightEnds : AstronomyEventCode
        Civil twilight (-6°) end.
    NauticalTwilightEnds : AstronomyEventCode
        Nautical twilight (-12°) end.
    AstronomicalTwilightEnds : AstronomyEventCode
        Astronomical twilight (-18°) end.
    NewMoon : AstronomyEventCode
        New moon.
    FirstQuarter : AstronomyEventCode
        Moon in first quarter.
    FullMoon : AstronomyEventCode
        Full moon.
    ThirdQuarter : AstronomyEventCode
        Moon in third quarter.
    """

    AstronomicalTwilightStarts = 1,
    NauticalTwilightStarts = 1 << 1,
    CivilTwilightStarts = 1 << 2,
    Rise = 1 << 3,
    Meridian = 1 << 4,
    AntiMeridian = 1 << 5,
    Set = 1 << 6,
    CivilTwilightEnds = 1 << 7,
    NauticalTwilightEnds = 1 << 8,
    AstronomicalTwilightEnds = 1 << 9,
    NewMoon = 1 << 10,
    FirstQuarter = 1 << 11,
    FullMoon = 1 << 12,
    ThirdQuarter = 1 << 13

    @staticmethod
    def resolve(event_code: str) -> "AstronomyEventCode":
        if event_code == "twi18_start":
            return AstronomyEventCode.AstronomicalTwilightStarts
        elif event_code == "twi12_start":
            return AstronomyEventCode.NauticalTwilightStarts
        elif event_code == "twi6_start":
            return AstronomyEventCode.CivilTwilightStarts
        elif event_code == "rise":
            return AstronomyEventCode.Rise
        elif event_code == "meridian":
            return AstronomyEventCode.Meridian
        elif event_code == "antimeridian":
            return AstronomyEventCode.AntiMeridian
        elif event_code == "set":
            return AstronomyEventCode.Set
        elif event_code == "twi6_end":
            return AstronomyEventCode.CivilTwilightEnds
        elif event_code == "twi12_end":
            return AstronomyEventCode.NauticalTwilightEnds
        elif event_code == "twi18_end":
            return AstronomyEventCode.AstronomicalTwilightEnds
        elif event_code == "newmoon":
            return AstronomyEventCode.NewMoon
        elif event_code == "firstquarter":
            return AstronomyEventCode.FirstQuarter
        elif event_code == "fullmoon":
            return AstronomyEventCode.FullMoon
        elif event_code == "thirdquarter":
            return AstronomyEventCode.ThirdQuarter
        else:
            raise ValueError("event_code does not conform to enum AstronomyEventCode")

