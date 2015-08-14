#!/usr/bin/env python

from rajab_roza import RajabRoza

lat = 51.0 + 32.0/60.0
lng = -22.0/60.0
start_year = 1400
end_year = 1500
filename = "data/london-durations.yml"

if __name__ == '__main__':
    rajab_roza = RajabRoza(lat, lng, start_year, end_year)
    rajab_roza.get_roza_durations()
    rajab_roza.save_to_yaml(filename)
