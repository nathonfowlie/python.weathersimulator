# Python Weather Simulator
This is a simple weather simulator that can be used to generate believable weather data for a number of Australian 
locations, as defined in ```data/locations.json```.

For the purposes of the simulator, air pressure is assumed to be static. This allows for humidity fluctuations to be
calculated based on changes to air temperature, in accordance to Boyles Law.

>**Boyles Law**: At constant temperature, the product of the volume and pressure of a given amount of gas is 
>constant.
>
>ref: https://en.wikipedia.org/wiki/Boyle%27s_law

Currently the simulator supports 20 locations which are listed below. Additional locations can be inserted by following
the instructions provided further on in this document.

* Adelaide
* Alice Springs
* Brisbane
* Broome
* Cairns
* Canberra
* Darwin
* Dubbo
* Geelong
* Gold Coast
* Hobart
* Kadina
* Kalgoorlie
* Melbourne
* Mildura
* Orange
* Perth
* Sydney
* Townsville
* Whyalla

The simulator expects to be provided a JSON data file, which defines GPS co-ordinates and acceptable minimum/maximum 
temperature for one or more locations (with an optional location name, such as 'Sydney', 'London' or 'New York').

Based off this data it will generate a random temperature within the given range, and calculate approximate 
air pressure, humidity and weather conditions.

The generated weather data is returned to the caller in the following text format: 
```csv
|Name|Position|Time|Conditions|Temperature|Pressure|Relative Humidity|
```

|Field|Type|Description|Example|
|-----|----|-----------|-------|
|Name|string|Human-friendly location name.|'Sydney', 'New York', 'London'|
|Position|string|Comma-seperated geo-graphical co-ordinates - latitude, longitude and elevation in metres.|-33.28397,149.10018,868|
|Time|ISO8601 date/time|Locations local time, expressed in ISO8601 format.|2017-11-25T21:52:19.866418Z10:00|
|Conditions|string|Weather conditions at the given location.|'Sunny', 'Rainy', 'Snowy'|
|Temperature|number|Temperature in degrees celsius.|36.0, 2.0|
|Pressure|number|Air pressure in hPa.|1145, 796, 1312|
|Relative Humidity|number|Relative humidity expressed as a percentage.|45, 100, 20|

## Requirements
Python 3.6 or higher is required, in addition to the following pip packages:
* Arrow 0.11.0
* Pytz 2017.3
* TimeZoneFinder 2.1.2
* Colorama 0.3.9
* JsonSchema 2.6.0
* Argparse
* PEP8
* Nose
* 

## Installation
```
git clone https://github.com/nathonfowlie/python.weathersimulator.git weathersimulator
cd weathersimulator
make install

```


## Known Issues
This module currently doesn't install correctly due to an issue with the ```schemas``` folder. The folder appears to be
included in the Egg, but it doesn't seem to get deployed at installation time. This causes the utility to crash as it
can't find a critical file needed to validate the location data file.

For the time being generate_weather.py will need to be executed from within the git checkout directory.


## Usage
./generate_weather.py

**Adding new locations**   
Additional locations can be added by editing ```data/locations.json```. This is a relatively simple JSON file which 
describes the name, geo-graphical co-ordinates, elevation, and monthly min/max temperature records for each location.

The metric system should be used to define elevation and temperature data (use Metres and Celsius).

```json
[
    {
        "name": "Sydney",
        "latitude": -33.8688197,
        "longitude": 151.2092955,
        "elevation": 40,
        "temps": {
            "min": [ 10.6, 9.6, 9.3, 7.0, 4.4, 2.1, 2.2, 2.7, 4.9, 5.7, 7.7, 9.1 ],
            "max": [ 45.8, 42.1, 39.8, 34.2, 30.0, 26.9, 25.9, 31.3, 34.6, 38.2, 41.8, 42.2 ]
        }
    },
    {
        "name": "Melbourne",
        "latitude": 28.0836269,
        "longitude": -80.6081089,
        "elevation": 25,
        "temps": {
            "min": [ 5.5, 4.5, 2.8, 1.5, -1.1, -2.2, -2.8, -2.1, -0.5, 0.1, 2.5, 4.4 ],
            "max": [ 45.6, 46.4, 41.7, 34.9, 28.7, 22.4, 23.1, 26.5, 31.4, 36.9, 40.9, 43.7 ]
        }
    },
]
```


## Future Improvements
**Improve algorithm used to generate wet bulb temperatures**   
The simulator uses  

If the difference between the dry and wet bulb temperatures is too great, it will cause a negative actual vapour 
pressure. To my current understanding, this would never occur in natural weather patterns but it can occur in the 
simulator 

The dew point formula assumes vapour pressures will always be a positive value 

The algorithm used to calculate dewpoint falls apart when the difference between dry and wet bulb
temperature is too great. For the purposes of the simulator a maximum difference of 10 degrees is enforced. 
  
**Dynamically retrieve location data**   
At the moment, ```./data/locations.json``` has to be hand crafted. This isn't ideal, as manually adding data is tedious
and would quickly become unmaintainable as the number of locations increases.

Ideally, the simulator would take a list of locations as user input, and dynamically populate the data file based on
information retrieved from weather APIs.

Basic GPS and elevation data can be retrieved from the Google Maps API, however there's no free, public API available to
obtain min/max monthly temperature records. Records are published to https://weatherzone.com.au, but they aren't 
presented in a way that is easily consumed by third party applications. A HTML parse would extract this information, but
it would be quite fragile as it would require modification each time WeatherZone modify their site layout or add/remove
content.
 