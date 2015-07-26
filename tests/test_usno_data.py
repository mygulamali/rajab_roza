import nose
from usno_data import USNO_Data

def assert_approximate(expected_value, observed_value, tolerance=1.0e-12):
    assert abs(expected_value - observed_value) < tolerance

class TestUSNO_Data:
    def setup(self):
        self.lat = 51.0 + 32.0/60.0

    def test_angle_components(self):
        (degrees, minutes) = USNO_Data.angle_components(self.lat)
        assert_approximate(51, degrees)
        assert_approximate(32, minutes)
