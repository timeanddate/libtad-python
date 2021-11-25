from typing import Tuple, Union
from enum import Flag

class AstronomyEventClass(Flag):
    """
    An enum class containing astronomical events

    ...

    Attributes
    ----------
    All : AstronomyEventClass
        Combination of all known classes.
    DayLength : AstronomyEventClass
        Day length.
    Meridian : AstronomyEventClass
        Meridian (Noon, highest point) and Anti-Meridian (lowest point) events.
    Phase : AstronomyEventClass
        Moon phase events. Additionally to the phase events (only occurring on
        four days per lunar month), an additional attribute for the current moon
        phase is reported for every day.
    SetRise : AstronomyEventClass
        Set and rise events. Event times take atmospheric refraction into account.   
    AllTwilights : AstronomyEventClass
        Combination of all 3 twilight classes.        
    CivilTwilight : AstronomyEventClass
        Civil twilight (-6°).
    NauticalTwilight : AstronomyEventClass
        Nautical twilight (-12°).
    AstronomicalTwilight : AstronomyEventClass
        Astronomical twilight (-18°).
    Current : AstronomyEventClass
        The current phase for the place requested. Additional attributes for 
        illumination (moon), azimuth, distance. 
        
    """

    All = 1
    DayLength = 1 << 1
    Meridian = 1 << 2
    Phase = 1 << 3
    SetRise = 1 << 4
    AllTwilights = 1 << 5
    CivilTwilight = 1 << 6
    NauticalTwilight = 1 << 7
    AstronomicalTwilight = 1 << 8
    Current = 1 << 9

    @staticmethod
    def resolve(astro_type: Union[int, str, "AstronomyEventClass"]) -> Tuple[int, str, "AstronomyEventClass"]:
        tup: Tuple[Tuple[int, str, AstronomyEventClass], ...] = (
            (1, "all", AstronomyEventClass.All),
            (1 << 1, "daylength", AstronomyEventClass.DayLength),
            (1 << 2, "meridian", AstronomyEventClass.Meridian),
            (1 << 3, "phase", AstronomyEventClass.Phase),
            (1 << 4, "setrise", AstronomyEventClass.SetRise),
            (1 << 5, "twilight", AstronomyEventClass.AllTwilights),
            (1 << 6, "twilight6", AstronomyEventClass.CivilTwilight),
            (1 << 7, "twilight12", AstronomyEventClass.NauticalTwilight),
            (1 << 8, "twilight18", AstronomyEventClass.AstronomicalTwilight),
            (1 << 9, "current", AstronomyEventClass.Current)
            )

        if type(astro_type) is int:
            index = 0
        elif type(astro_type) is str:
            index = 1
        elif type(astro_type) is AstronomyEventClass:
            index = 2
        else:
            return None

        for astro_entry in tup:
            if astro_type == astro_entry[index]:
                return astro_entry

