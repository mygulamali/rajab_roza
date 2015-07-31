from datetime import datetime
import requests

class USNO_Data:
    USNO_URL = "http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl"

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        self.year = None
        self.sunrises = None
        self.sunsets = None
        self.session = requests.Session()

    @staticmethod
    def angle_components(angle):
        direction = -1 if (angle < 0.0) else 1
        degrees = int(angle)
        minutes = round((angle - degrees)*60)
        return (direction, abs(degrees), abs(minutes))

    def parameters(self):
        (lat_direction, lat_degrees, lat_minutes) = USNO_Data.angle_components(self.lat)
        (lng_direction, lng_degrees, lng_minutes) = USNO_Data.angle_components(self.lng)

        return {
            "FFX": "2",
            "xxy": str(self.year),
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

    @staticmethod
    def day_of_year(year, month, day):
        return datetime(year, month, day).timetuple().tm_yday

    @staticmethod
    def extract_times(year, data):
        days_in_year = USNO_Data.day_of_year(year, 12, 31)
        sunrises = [None for i in range(days_in_year)]
        sunsets = [None for i in range(days_in_year)]

        lines = data.split("\n")[18:(18 + 31)]
        for line in lines:
            times = line.split()
            day = int(times[0])
            for month in range(12):
                try:
                    actual_month = month + 1
                    day_of_year = USNO_Data.day_of_year(year, actual_month, day) - 1
                    sunrises[day_of_year] = USNO_Data.as_datetime(year, actual_month, day, times[2*month + 1])
                    sunsets[day_of_year] = USNO_Data.as_datetime(year, actual_month, day, times[2*actual_month])
                except:
                    next

        return (sunrises, sunsets)

    def get_data(self, year):
        self.year = year
        data = self.session.post(USNO_Data.USNO_URL, data=self.parameters())
        (self.sunrises, self.sunsets) = USNO_Data.extract_times(self.year, data.text)

    def sunrise(self, month, day):
        day_of_year = USNO_Data.day_of_year(self.year, month, day)
        return self.sunrises[day_of_year - 1]

    def sunset(self, month, day):
        day_of_year = USNO_Data.day_of_year(self.year, month, day)
        return self.sunsets[day_of_year - 1]
