# Time And Date Python API
![pypi](https://img.shields.io/pypi/v/libtad)

Use our API Services to tap into timeanddate.com's databases and integrate our data into your applications

## Service Reference

- [astronomy – Get Information About Astronomical Objects](https://dev.timeanddate.com/docs/astro/).
- [astrodata – Calculate data on Astronomical Objects on Specific Times](https://dev.timeanddate.com/docs/astro/).
- [businessdate – Calculate business date from a given number of days](https://dev.timeanddate.com/docs/calculator/).
- [businessduration – Calculate business days in a specified date range](https://dev.timeanddate.com/docs/calculator/).
- [converttime – Convert Time Between Time Zones](https://dev.timeanddate.com/docs/time/).
- [dstlist – Retrieve Daylight Saving Time Information](https://dev.timeanddate.com/docs/time/).
- [holidays – Retrieve List of Holidays](https://dev.timeanddate.com/docs/holidays/).
- [places – Retrieve List of Available Places](https://dev.timeanddate.com/docs/places).
- [timeservice – Retrieve Current Time for Place](https://dev.timeanddate.com/docs/time/).

## Requirements

- Python 3.6

## Installation

```
pip3 install libtad
```

## Usage

```py
from libtad import AstronomyService
from libtad.datatypes.places import Coordinates, LocationId
from libtad.datatypes.time import TADDateTime
from libtad.datatypes.astro import AstronomyEventClass, AstronomyObjectType

# Specify the location, and the dates you are querying for
coordinates = Coordinates(59.743, 10.204)
place = LocationId(coordinates)
date = TADDateTime(2020, 11, 26)

# To perform the query, you will need your access key and secret key
service = AstronomyService("accessKey", "secretKey")

# Select which astronomical events you are interested in
service.types = AstronomyEventClass.Meridian | AstronomyEventClass.Phase

# Retrieve astronomical information for specified astronomy object at a given time and place
astro_info = service.get_astronomical_info(AstronomyObjectType.Moon, place, date)
```

## Credits

TadApi is owned and maintained by the [Time and Date AS](https://www.timeanddate.com). You can visit our API Reference at [timeanddate.com](https://dev.timeanddate.com/docs/toc) for project updates and releases.

## Author

[Time and Date](https://www.timeanddate.com)
