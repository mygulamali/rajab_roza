#!/usr/bin/env python

import matplotlib.pyplot as pyplot

from rajab_roza import RajabRoza

filename = "data/london-durations.yml"
years = range(1430, 1461)

def duration_in_hours(duration):
    return duration.total_seconds()/3600.0

if __name__ == '__main__':
    rajab_roza = RajabRoza.load_from_yaml(filename)
    start_index = years[0] - rajab_roza.start_year
    data_index_range = range(start_index, start_index + len(years))

    min_durations = [
        duration_in_hours(rajab_roza.durations[i][0])
        for i in data_index_range
    ]
    max_durations = [
        duration_in_hours(rajab_roza.durations[i][1])
        for i in data_index_range
    ]

    pyplot.vlines(years, min_durations, max_durations, color='#006600', linewidth=10)
    pyplot.grid()
    pyplot.title("Duration of Rajab Roza in London")
    pyplot.xlabel("Hijri year")
    pyplot.ylabel("Duration (Hours)")
    pyplot.savefig("data/london-durations.png", bbox_inches="tight")
