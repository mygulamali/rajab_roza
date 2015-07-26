import nose
from usno_data import USNO_Data

def assert_approximate(expected_value, observed_value, tolerance=1.0e-12):
    assert abs(expected_value - observed_value) < tolerance

class TestUSNO_Data:
    def test_angle_components(self):
        (degrees, minutes) = USNO_Data.angle_components(51.0 + 32.0/60.0)
        assert_approximate(51, degrees)
        assert_approximate(32, minutes)
