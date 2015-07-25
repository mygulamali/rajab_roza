import nose
from hijri_date import HijriDate

class TestHijriDate:
    def setup(self):
        self.date = HijriDate() # 20/04/1432H = 25/03/2011AD

    def test_kabisa_year(self):
        assert not self.date.is_kabisa()
        assert self.date.is_kabisa(1431)
