from enum import Flag

class MoonPhase(Flag):
    """
    An enum class containing moon phase for the day.

    ...

    Attributes
    ----------
    NotRequested : MoonPhase
        The not requested moon phases.
    NewMoon : MoonPhase
        New moon.
    WaxingCrescent : MoonPhase
        Waxing crescent moon.
    FirstQuarter : MoonPhase
        Moon in first quarter.
    WaxingGibbous : MoonPhase
        Waxing gibbous moon.
    FullMoon : MoonPhase
        Full moon.
    WaningGibbous : MoonPhase
        Waning gibbous moon.
    ThirdQuarter : MoonPhase
        Moon in third quarter.
    WaningCrescent : MoonPhase
        Waning crescent moon.
    """

    NotRequested = 1,
    NewMoon = 1 << 1,
    WaxingCrescent = 1 << 2,
    FirstQuarter = 1 << 3,
    WaxingGibbous = 1 << 4,
    FullMoon = 1 << 5,
    WaningGibbous = 1 << 6,
    ThirdQuarter = 1 << 7,
    WaningCrescent = 1 << 8

    @staticmethod
    def _parse(moonphase: str) -> "MoonPhase":
        for phase in MoonPhase:
            if phase.name.lower() != moonphase.lower():
                continue
            return phase

