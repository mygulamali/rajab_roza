import nose
from hijri_date import HijriDate

class TestHijriDate:
    def setup(self):
        self.date = HijriDate() # 20/04/1432H = 25/03/2011AD

    def test_equality(self):
        assert HijriDate() == self.date

    def test_kabisa_year(self):
        assert not self.date.is_kabisa()
        assert self.date.is_kabisa(1431)

    def test_days_in_month(self):
        assert self.date.days_in_month() == 29
        assert self.date.days_in_month(12) == 29
        assert self.date.days_in_month(12, 1431) == 30

    def test_day_of_year(self):
        assert self.date.day_of_year() == 109
        assert HijriDate(1432, 1, 10).day_of_year() == 10
        assert HijriDate(1431, 12, 30).day_of_year() == 355
        assert HijriDate(1432, 12, 29).day_of_year() == 354

    def test_conversion_to_jd(self):
        assert self.date.to_jd() == 2455646

    def test_conversion_from_jd(self):
        assert HijriDate.from_jd(2455646) == self.date
