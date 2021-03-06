from betamax import Betamax
import nose
import requests
from rajab_roza.usno_data import USNO_Data

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes'

class TestUSNO_Data:
    def setup(self):
        self.lat = 51.0 + 32.0/60.0
        self.lng = -22.0/60.0
        self.year = 2015
        self.usno_data = USNO_Data(self.lat, self.lng)
        self.recorder = Betamax(self.usno_data.session, default_cassette_options={
            'record_mode': 'once',
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
        self.usno_data.year = 2015
        assert self.usno_data.parameters() == expected_parameters

    def test_as_datetime(self):
        date = USNO_Data.as_datetime(self.year, 2, 22, '2153')
        assert date.year == self.year
        assert date.month == 2
        assert date.day == 22
        assert date.hour == 21
        assert date.minute == 53
        assert date.second == 0
        assert date.utcoffset() is None

    def test_day_of_year(self):
        assert USNO_Data.day_of_year(2015, 2, 22) == 53
        assert USNO_Data.day_of_year(2016, 4, 1) == 92

    def test_get_data(self):
        with self.recorder.use_cassette('get_data'):
            self.usno_data.get_data(self.year)
            assert self.usno_data.sunrises[-1] == USNO_Data.as_datetime(self.year, 12, 31, '0807')
            assert self.usno_data.sunsets[-1] == USNO_Data.as_datetime(self.year, 12, 31, '1601')

    def test_sunrise(self):
        with self.recorder.use_cassette('get_sunrise'):
            self.usno_data.get_data(self.year)
            sunrise = self.usno_data.sunrise(2, 22)
            assert sunrise.hour == 7
            assert sunrise.minute == 2

    def test_sunset(self):
        with self.recorder.use_cassette('get_sunset'):
            self.usno_data.get_data(self.year)
            sunset = self.usno_data.sunset(2, 22)
            assert sunset.hour == 17
            assert sunset.minute == 29
