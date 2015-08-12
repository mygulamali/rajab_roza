#!/usr/bin/env python

from rajab_roza import RajabRoza

lat = 51.0 + 32.0/60.0
lng = -22.0/60.0
start_year = 1435
end_year = 1436
filename = "1435-1436.yml"

if __name__ == '__main__':
    rajab_roza = RajabRoza(lat, lng, start_year, end_year)
    rajab_roza.get_roza_durations()
    rajab_roza.save_to_yaml(filename)
