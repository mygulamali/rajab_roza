#!/usr/bin/env python

import matplotlib.pyplot as pyplot

from rajab_roza import RajabRoza

filename = "data/london-durations.yml"

def duration_in_hours(duration):
    return duration.total_seconds()/3600.0

if __name__ == '__main__':
    rajab_roza = RajabRoza.load_from_yaml(filename)
    years = range(rajab_roza.start_year, rajab_roza.end_year + 1)
    min_durations = [
        duration_in_hours(rajab_roza.durations[i][0])
        for i in range(len(years))
    ]
    max_durations = [
        duration_in_hours(rajab_roza.durations[i][1])
        for i in range(len(years))
    ]

    pyplot.fill_between(years, min_durations, max_durations)
    pyplot.grid()
    pyplot.title("Duration of Rajab Roza in London")
    pyplot.xlabel("Hijri year")
    pyplot.ylabel("Duration (Hours)")
    pyplot.savefig("data/london-durations.png", bbox_inches="tight")
