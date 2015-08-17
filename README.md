# Rajab Roza

## Synopsis

The `get_data.py` Python script obtains the Sunrise and Sunset times from [the
USNO website][usno] and determines the minimum and maximum *roza* (fasting)
durations during [Rajab][rajab] for a specified location and range of Hijri
years.

The `plot_data.py` Python script plots the data from the previous script and
highlights the consecutive 10-year period for which these durations are minimal.

## Setup

`pip install -f requirements.txt`

## Usage

`python get_data.py`
`python plot_data.py`

## Testing

`nosetests`

## License

This software is released under the terms and conditions of [The MIT
License][license].  Please see the LICENSE.txt file for more details.

[rajab]: https://en.wikipedia.org/wiki/Rajab "Rajab"
[license]: http://www.opensource.org/licenses/mit-license.php "The MIT License"
[usno]: http://aa.usno.navy.mil/data/docs/RS_OneYear.php "Sun or Moon Rise/Set Table for One Year"
