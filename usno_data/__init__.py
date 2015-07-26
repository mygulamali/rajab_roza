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
