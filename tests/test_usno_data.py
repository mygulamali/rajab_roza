import nose
from usno_data import USNO_Data

class TestUSNO_Data:
    def setup(self):
        self.lat = 51.0 + 32.0/60.0
        self.lng = -22.0/60.0
        self.year = 2015
        self.usno_data = USNO_Data(self.lat, self.lng)

    def test_angle_components(self):
        (direction, degrees, minutes) = USNO_Data.angle_components(self.lat)
        assert direction == 1
        assert degrees == 51
        assert minutes == 32

    def test_parameters(self):
        expected_parameters = {
            "FFX": "2",
            "xxy": "2015",
            "tabtyb": "0",
            "place": "",
            "xx0": "-1",
            "xx1": "0",
            "xx2": "22",
            "yy0": "1",
            "yy1": "51",
            "yy2": "32",
            "zz0": "1",
            "zz1": "0",
            "ZZZ": "END"
        }
        assert self.usno_data.parameters(self.year) == expected_parameters
