class HijriDate(object):
    def __init__(self, year=1432, month=4, date=20):
        self.year = year
        self.month = month
        self.date = date

    def is_kabisa(self, year=None):
        if year == None:
            year = self.year
        for i in [2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29]:
            if (year % 30 == i):
                return True
        return False
