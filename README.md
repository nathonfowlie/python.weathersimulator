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





## Installation
This module currently doesn't install correctly due to an issue with the ```schemas``` folder. The folder appears to be
included in the Egg, but it doesn't seem to get deployed at installation time. This causes the utility to crash as it
can't find a critical file needed to validate the location data file.

As a work-around, generate_weather.py can be executed from within the git checkout directory after doing a manual 
install. Note I only had a windows machine to do this exercise on, the Makefile works on the MinGW version of make, but 
I haven't been able to do testing on Mac/Linux:

```commandline
git clone https://github.com/nathonfowlie/python.weathersimulator.git weathersimulator
cd weathersimulator
make lint
make test
make build
make install
```





## Usage
```
./generate_weather.py -f ~/foo/locations.json -s '01/09/2018' -e '18/09/2018'
``` 

where **-f** is the absolute or relative path to the JSON file containing location data, and **-s/-e** define the date 
range that data will be generated for. Refer to ```./generate_weather.py --help``` for the full list of available
commands. 


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
**Fix the JSON schema bug**   
Fix the packaging error that's preventing the module from being able to execute from outside of the git checkout 
directory.


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

**Temperature/Air Pressure/Humidity should be influenced by previous days weather**
The simulator allows for a 35 degree day, followed by a 14 degree day. It also completely ignores the time of day. 
Results would be significantly more accurate if the time of day was considered, with temperature following a bell
curve as the day progresses. The minimum and maximum possible temperature ranges should also be affected by the previous
days temperature, so that it's not 5 degrees on 01/01/1970 23:59, then suddenly 42 degrees on 02/01/1970 at 00:01.


# Thoughts/Rationale
My original intentions where to leverage public web apis to dynamically retrieve location information on demand and 
store it in local cache. I had to give up on this idea as I was unable to find any web services that provided all of the
data I needed to build the simulator. The Google Maps API was able to provide elevation and GPS co-ordinates (as well as
resolve GPS co-ordinates to the name of a city), but it didn't contain the min/max temperature records for locations,
broken by by month.

https://weatherzone.com.au provides the temperature data that I needed, however it's not presented in a way that is
easily consumable. I could have written a HTML parser to extract the data, but it would have been too fragile to be of
any use. Any change to the site layout or content would result in the weather simulator being unable to retrieve 
temperature information.

As a fallback, I decided to manually build a 'cache' of location information. If/when an API becomes available then the
simulator can be updated to populate this cache from the new web service. 


1. Determine the standard air pressure at each location by applying the Barometric formula, which is based on the US 
Standard Atmosphere (1976() model. Temperature and humidity have a correlation to air pressure, so this gave me a 
starting point.
2. For the given location, I generated a random temperature that was within the range of the min and max temperatures on
record for that location (ref: https://bom.gov.au). This simplified the model as it removed the need to add any kind of 
weighting to account for the fact that temperatures are higher in summer than in winter.
3. I found two formulas that could be used to calculate relative humidity. The first required me to know the dewpoint,
and the second recquired a wet bulb temperature. I decided to go with the dry/wet bulb calculation as it was
significantly simpler. With this equation, humidity is directly related to the difference between dry bulb (air) 
temperature and web bulb temperature, where wet bulb temperature never exceeds dry bulb. I generated a second
random temperature within <air temperature- 9> and <air temperature>. I chose 9 as the arbitary limit as the table I was
using to verify the accuracy of my results only covered a temperature difference of 10 degrees 
(https://www.eduplace.com/science/hmxs/es/pdf/5rs_3_2-3.pdf). The formula also does not work where the difference is 
greater than 10 degrees (very unlikely to happen in the natural world).
4. At this point I realised that the generated data was a little bit off because air pressure was static and didn't 
change according to fluctuations in temperature or humidity. To fix this, I modified the air pressure calculations to
allow pressure to increase or decrease by 20% on any given day. This resulted in much more believable metrics. I would
have preferred a variation not based on gutt instinct, but I was begginning to run out of time to complete this exercise. 
5. Next I calculate humidity based off a combination of dry and wet bulb temperature and the Ideal Gas equation.
6. To calculate condition (sunny, rainy, snowy), I had to make a best guess based on personal experience as there are
too many factors that could influence whether it will be 25 degrees and Sunny, or 25 degrees and Raining. 
    * If the temperature is low, humidity is high and air pressure is low, it's more likely to snow.
    * If the temperature is above freezing point, humidity is high and pressure is slightly below average, there is a 
      chance of rain.
    * If neither of the above circumstances are met, then I assume it's a sunny day. 


**Caveats**   
The formulas that I used don't work/become inaccurate once you're more than 11km above sea level. I decided this was 
acceptable given we aren't trying to calculate weather conditions for a trans-continential flight :)

I also decided to use the Buck equation over Goff-Gratch as it's a much simpler equation and I was burning too much time
trying to implement Goff-Gratch in code. There's a slight accuracy trade-off, but the exercise stated data only has to
be believed (not accurate), so I figure it was a good trade-off between speed and accuracy.

One thing that I found quite difficult in building the utility was the lack of domain expertise (what the heck is a wet 
bulb?), and the large number of mis-leading online articles that contained bad formulas or incorrect constants. This
made it quite hard to verify the accuracy of my own calculations as I didn't have a reliable reference point.

I was hoping to also build a small Docker container for this (Alpine as it is very small and light-weight), but I ran
out of time. All of the logic for calculating weather patterns is contained within 
```WeatherGenerator.weather.WeatherCondition```. This would allow the game to generate weather data on the fly by
consuming the package, rather than relying on a two-step process where data first has to be created, and then imported
into the game.





## References
The following resources were used to create the formulas used for air pressure and humidity.

* https://en.wikipedia.org/wiki/Barometric_formula
* https://maps.googleapis.com/maps/api/geocode/json?address=Sydney
* http://www.weatherzone.com.au/climate/station.jsp?lt=site&lc=70351
* http://www.1728.org/relhum.htm
* http://maxwellsci.com/print/rjaset/v6-2984-2987.pdf
* https://en.wikipedia.org/wiki/Vapour_pressure_of_water
* https://en.wikipedia.org/wiki/Arden_Buck_equation
* https://cals.arizona.edu/azmet/dewpoint.html
* https://www.engineeringtoolbox.com/humidity-ratio-air-d_686.html