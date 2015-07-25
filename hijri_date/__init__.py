from hijri_date.constants import *

class HijriDate(object):
    def __init__(self, year=1432, month=4, date=20):
        self.year = year
        self.month = month
        self.date = date

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
