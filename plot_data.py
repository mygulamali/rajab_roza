#!/usr/bin/env python

import matplotlib.pyplot as pyplot
from numpy import argsort, sort

from rajab_roza import RajabRoza

filename = "data/london-durations.yml"
years = range(1430, 1461)

def duration_in_hours(duration):
    return duration.total_seconds()/3600.0

def minimal_duration_years(years, durations, amount=10):
    sorted_durations = argsort(durations)
    minimal_years = [years[i] for i in sorted_durations[:amount]]
    return sort(minimal_years)

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
    avg_durations = [
        0.5*(min_durations[i] + max_durations[i])
        for i in range(len(years))
    ]

    min_duration_years = minimal_duration_years(years, avg_durations)

    pyplot.vlines(years, min_durations, max_durations, color='#006600', linewidth=10)
    pyplot.axvspan(min_duration_years[0] - 0.5, min_duration_years[-1] + 0.5, facecolor='#006600', edgecolor='none', alpha=0.25)
    pyplot.grid()
    pyplot.title("Duration of Rajab Roza in London")
    pyplot.xlabel("Hijri year")
    pyplot.ylabel("Duration (Hours)")
    pyplot.savefig("data/london-durations.png", bbox_inches="tight")
