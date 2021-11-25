from enum import Enum

class BusinessDaysOperatorType(Enum):
    """
    An enum class containing business.PeriodTypedays operators.

    ...

    Attributes
    ----------
    Add : BusinessDaysOperatorType
        Add.
    Subtract : BusinessDaysOperatorType
        Subtract.
    """

    Add = 1
    Subtract = 2

