from enum import Flag

class AstronomyObjectType(Flag):
    """
    An enum class with simple bitflags so the user can easily put together
    a set of types which should be included or excluded in the retrieval 
    of holidays.

    ...

    Attributes
    ----------
    Sun : AstronomyObjectType
        The sun.        
    Moon : AstronomyObjectType
        The moon.
    Mercury : AstronomyObjectType
        Mercury.
    Venus : AstronomyObjectType
        Venus.
    Mars : AstronomyObjectType
        Mars.
    Jupiter : AstronomyObjectType
        Jupiter.
    Saturn : AstronomyObjectType
        Saturn.
    Uranus : AstronomyObjectType
        Uranus.
    Neptune : AstronomyObjectType
        Neptune.
    Pluto : AstronomyObjectType
        Pluto.
    """

    Sun = 1
    Moon = 1 << 1
    Mercury = 1 << 2
    Venus = 1 << 3
    Mars = 1 << 4
    Jupiter = 1 << 5
    Saturn = 1 << 6
    Uranus = 1 << 7
    Neptune = 1 << 8
    Pluto = 1 << 9

