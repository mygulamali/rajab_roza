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
    def extract_times(year, data):
        sunrises = [[], [], [], [], [], [], [], [], [], [], [], []]
        sunsets = [[], [], [], [], [], [], [], [], [], [], [], []]

        lines = data.split("\n")[18:(18 + 31)]
        for line in lines:
            times = line.split()
            if len(times) == 23:
                [times.insert(i, None) for i in [3, 4]]
            elif len(times) == 15:
                [times.insert(i, None) for i in [3, 4, 7, 8, 11, 12, 17, 18, 21, 22]]

            day = int(times[0])
            for month in range(12):
                sunrises[month].append(
                    USNO_Data.as_datetime(year, month + 1, day, times[2*month + 1])
                )
                sunsets[month].append(
                    USNO_Data.as_datetime(year, month + 1, day, times[2*(month + 1)])
                )

        return (sunrises, sunsets)

    def get_data(self, year):
        self.year = year
        data = self.session.post(USNO_Data.USNO_URL, data=self.parameters())
        (self.sunrises, self.sunsets) = USNO_Data.extract_times(self.year, data.text)

    def sunrise(self, month, day):
        return self.sunrises[month - 1][day - 1]

    def sunset(self, month, day):
        return self.sunsets[month - 1][day - 1]
