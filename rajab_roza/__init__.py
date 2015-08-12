from datetime import timedelta
import yaml

from hijri_date import HijriDate
from usno_data import USNO_Data

class RajabRoza:
    def __init__(self, lat, lng, start_year, end_year):
        self.lat = lat
        self.lng = lng
        self.start_year = start_year
        self.end_year = end_year
        self.usno_data = USNO_Data(lat, lng)

    def get_roza_durations_for_year(self, hijri_year):
        durations = (timedelta.max, timedelta.min)

        start_date = HijriDate(hijri_year, 7, 1).to_gregorian()
        self.usno_data.get_data(start_date.year)
        for day in range(0, 30):
            date = start_date + timedelta(day)
            if date.year != start_date.year:
                self.usno_data.get_data(date.year)

            sunrise = self.usno_data.sunrise(date.month, date.day)
            sunset = self.usno_data.sunset(date.month, date.day)

            duration = sunset - sunrise
            durations = (
                min(durations[0], duration), max(durations[1], duration)
            )

        return durations

    def get_roza_durations(self):
        self.durations = [
            self.get_roza_durations_for_year(year)
            for year in range(self.start_year, self.end_year + 1)
        ]

    def save_to_yaml(self, filename):
        stream = open(filename, 'w')
        yaml.safe_dump({
            'lat': self.lat,
            'lng': self.lng,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'durations': [
                [duration[0].total_seconds(), duration[1].total_seconds()]
                for duration in self.durations
            ]
        }, stream, allow_unicode=True)
        stream.close()

    @staticmethod
    def load_from_yaml(filename):
        stream = open(filename, 'r')
        data = yaml.load(stream)
        stream.close()

        rajab_roza = RajabRoza(
            data['lat'], data['lng'], data['start_year'], data['end_year']
        )
        rajab_roza.durations = [
            (timedelta(seconds=duration[0]), timedelta(seconds=duration[1]))
            for duration in data['durations']
        ]

        return rajab_roza
