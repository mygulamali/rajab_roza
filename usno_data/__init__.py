from datetime import datetime
import requests

class USNO_Data:
    USNO_URL = "http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl"

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.data = None
        self.session = requests.Session()

    @staticmethod
    def angle_components(angle):
        direction = -1 if (angle < 0.0) else 1
        degrees = int(angle)
        minutes = round((angle - degrees)*60)
        return (direction, abs(degrees), abs(minutes))

    def parameters(self, year):
        (lat_direction, lat_degrees, lat_minutes) = USNO_Data.angle_components(self.lat)
        (lng_direction, lng_degrees, lng_minutes) = USNO_Data.angle_components(self.lng)

        return {
            "FFX": "2",
            "xxy": str(year),
            "type": "0", # table of sunrise/sunset times
            "place": "",
            # longitude
            "xx0": str(lng_direction), # west = -1, east = 1
            "xx1": str(lng_degrees),
            "xx2": str(lng_minutes),
            # latitude
            "yy0": str(lat_direction), # south = -1, north = 1
            "yy1": str(lat_degrees),
            "yy2": str(lat_minutes),
            # timezone
            "zz0": "1", # west = -1, east = 1
            "zz1": "0", # UTC
            "ZZZ": "END"
        }

    @staticmethod
    def as_datetime(year, month, day, time_string):
        if not time_string:
            return None
        datetime_string = "{0:04}-{1:02}-{2:02} {3} UTC".format(year, month, day, time_string)
        return datetime.strptime(datetime_string, "%Y-%m-%d %H%M %Z")

    def get_data(self, year):
        self.data = self.session.post(USNO_Data.USNO_URL, data=self.parameters(year))
