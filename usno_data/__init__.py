class USNO_Data:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

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
            "FFX": 2,
            "xxy": year,
            "tabtyb": 0, # table of sunrise/sunset times
            "place": "",
            # longitude
            "xx0": lng_direction, # west = -1, east = 1
            "xx1": lng_degrees,
            "xx2": lng_minutes,
            # latitude
            "yy0": lat_direction, # south = -1, north = 1
            "yy1": lat_degrees,
            "yy2": lat_minutes,
            # timezone
            "zz0": 1, # west = -1, east = 1
            "zz1": 0, # UTC
            "ZZZ": "END"
        }
