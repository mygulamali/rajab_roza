from betamax import Betamax
import nose
import requests
from usno_data import USNO_Data

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'

class TestUSNO_Data:
    def setup(self):
        self.lat = 51.0 + 32.0/60.0
        self.lng = -22.0/60.0
        self.year = 2015
        self.usno_data = USNO_Data(self.lat, self.lng)
        self.recorder = Betamax(self.usno_data.session, default_cassette_options={
            'record_mode': 'new_episodes',
            'match_requests_on': ['method', 'uri', 'headers'],
            'preserve_exact_body_bytes': True
        })

    def test_angle_components(self):
        (direction, degrees, minutes) = USNO_Data.angle_components(self.lat)
        assert direction == 1
        assert degrees == 51
        assert minutes == 32

    def test_parameters(self):
        expected_parameters = {
            "FFX": "2",
            "xxy": "2015",
            "type": "0",
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

    def test_get_data(self):
        with self.recorder.use_cassette('get_data'):
            self.usno_data.get_data(self.year)
            assert self.usno_data.data is not None
