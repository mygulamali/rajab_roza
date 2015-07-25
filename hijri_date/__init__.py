from datetime import date as GregorianDate
from math import floor
from hijri_date.constants import *

class HijriDate(object):
    def __init__(self, year=1432, month=4, date=20):
        self.year = year
        self.month = month
        self.date = date

    def __eq__(self, other):
        return (self.year == other.year) and (self.month == other.month) and (self.date == other.date)

    def is_kabisa(self, year=None):
        if year == None:
            year = self.year
        for i in KABISA_YEAR_REMAINDERS:
            if (year % 30 == i):
                return True
        return False

    def days_in_month(self, month=None, year=None):
        if month == None:
            month = self.month
        if year == None:
            year = self.year

        if (month == 12 and self.is_kabisa(year)) or (month % 2 == 1):
            return 30
        return 29

    def day_of_year(self):
        if self.month == 1:
            return self.date
        return DAYS_IN_YEAR[self.month - 2] + self.date

    def to_jd(self):
        y30 = floor(self.year / 30.0)
        if (self.year % 30 == 0):
            return 1948084 + y30*10631 + self.day_of_year()
        return sum(map(int, [
            1948084,
            y30*10631,
            DAYS_IN_30_YEARS[self.year - y30*30 - 1],
            self.day_of_year()
        ]))

    @staticmethod
    def from_jd(julian_day_number=1948084):
        left = int(julian_day_number - 1948084)
        y30 = floor(left / 10631.0)
        left -= y30*10631
        i = 0

        while left > DAYS_IN_30_YEARS[i]:
            i += 1
        year = int(y30*30.0 + i)

        if i>0:
            left -= DAYS_IN_30_YEARS[i - 1]
        i = 0

        while left > DAYS_IN_YEAR[i]:
            i += 1
        month = int(i + 1)

        if i>0:
            day = int(left - DAYS_IN_YEAR[i - 1])
        else:
            day = int(left)

        return HijriDate(year, month, day)

    def to_gregorian(self):
        a = self.to_jd() + 32044
        b = (4*a + 3)//146097
        c = a - (146097*b)//4
        d = (4*c + 3)//1461
        e = c - (1461*d)//4
        m = (5*e + 2)//153

        day = int(e + 1 - (153*m + 2)//5)
        month = int(m + 3 - 12*(m//10))
        year = int(100*b + d - 4800 + m/10)

        return GregorianDate(year, month, day)
