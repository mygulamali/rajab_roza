import nose
from usno_data import USNO_Data

class TestUSNO_Data:
    def setup(self):
        self.lat = 51.0 + 32.0/60.0

    def test_angle_components(self):
        (direction, degrees, minutes) = USNO_Data.angle_components(self.lat)
        assert direction == 1
        assert degrees == 51
        assert minutes == 32
