import enum


class Rank(enum.Enum):
    NO_RANK = "Без разряда"
    THREE_JUN = "3 юн."
    TWO_JUN = "2 юн."
    ONE_JUN = "1 юн."
    THREE_MID = "3 взр."
    TWO_MID = "2 взр."
    ONE_MID = "1 взр."


class Group(enum.Enum):
    MAN_YOUTH = "мальчики 2007-2008 (14,15 лет)"
    WOMAN_YOUTH = "девочки 2007-2008"
    MAN_TEEN = "мальчики 2009-2012 (10-13 лет)"
    WOMAN_TEEN = "девочки 2009-2012"
    MAN_SUPERTEEN = "мальчики 2013-2015 (7-9 лет)"
    WOMAN_SUPERTEEN = "девочки 2013-2015"
    MAN_MICRO = "мальчики  2016-2017 (5 -6 лет)"
    WOMAN_MICRO = "девочки  2016-2017 (5 -6 лет)"


class Color(enum.Enum):
    ORANGE = "orange"
    BLACK = "black"
    WHITE = "white"


class OffsetType(enum.Enum):
    FIRST = "first"
    NEXT = "next"
    SPECIFIC = "specific"
    PREV = "prev"
    LAST = "last"
