from enum import Enum

class BusinessFilterMethod(Enum):
    """
    An enum class containing methods for filtering in business.PeriodTypeapis.

    ...

    Attributes
    ----------
    Included : BusinessFilterMethod
        Included.
    Excluded : BusinessFilterMethod
        Excluded.
    """

    Included = 1
    Excluded = 2

