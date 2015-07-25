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

    def jd(self):
        y30 = floor(self.year / 30.0)
        if (self.year % 30 == 0):
            return 1948084 + y30*10631 + self.day_of_year()
        return sum(map(int, [
            1948084,
            y30*10631,
            DAYS_IN_30_YEARS[self.year - y30*30 - 1],
            self.day_of_year()
        ]))
