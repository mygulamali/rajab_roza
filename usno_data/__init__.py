class USNO_Data:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    @staticmethod
    def angle_components(angle):
        degrees = int(angle)
        minutes = (angle - degrees)*60.0
        return (degrees, minutes)
