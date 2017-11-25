import json
import random
import math
import arrow
import pytz
from timezonefinder import TimezoneFinder
from utils import WeatherCondition

with open("data/locations.json") as location_file:
    location_records = json.load(location_file)

    for location in location_records:
        # Generate a random date
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng = location['longitude'], lat=location['latitude'])
        tz = pytz.timezone(timezone_str)
        current_date = arrow.now(tz)

        # Create a new weather condition for the found record
        weather_condition = WeatherCondition()
        weather_condition.name = location['name']
        weather_condition.latitude = location['latitude']
        weather_condition.longitude = location['longitude']
        weather_condition.elevation = location['elevation']
        weather_condition.datetime = current_date

        # Pressure needs to be converted to millibars for the formuala to calculate humidity
        pressure_in_mb = weather_condition.pressure * 0.01

        weather_condition.temperature = random.uniform(location['temps']['min'][0], location['temps']['max'][0])

        # FIXME: An artificial limit of 10 degrees variation between dry and wet bulb temperatures has been used to prevent
        # negative actual vapour pressure values (does not occur in nature).
        #
        # This script will throw a math domain exception if a negative value (impossible situation) is encountered. A better
        # algorithm would be to calculate the min/max achievable wet bulb temperature for the given dry bulb temperature,
        # and generate a random number that falls within the calculated range.
        #
        # The table at https://www.eduplace.com/science/hmxs/es/pdf/5rs_3_2-3.pdf used to validate the correctness of
        # the humidity results stops at a 10 degrees difference (there may be some variation in results due to rounding.
        wetbulb_temp = random.uniform(location['temps']['min'][0], weather_condition.temperature)

        # https: // en.wikipedia.org / wiki / Barometric_formula
        # https://maps.googleapis.com/maps/api/geocode/json?address=Sydney
        # http://www.weatherzone.com.au/climate/station.jsp?lt=site&lc=70351
        # http://www.1728.org/relhum.htm
        # http://maxwellsci.com/print/rjaset/v6-2984-2987.pdf
        # https://en.wikipedia.org/wiki/Vapour_pressure_of_water (Buck equation).
        # https://en.wikipedia.org/wiki/Arden_Buck_equation
        # https://cals.arizona.edu/azmet/dewpoint.html
        # Atmospheric pressure in PA, need to convert to millibars for humidity calculations
        # https: // www.engineeringtoolbox.com / humidity - ratio - air - d_686.html

        # saturation vapour pressure for dry bulb
        Es = 6.108 * (math.exp((17.27 * weather_condition.temperature) / (237.3 + weather_condition.temperature)))

        # saturation vapour pressure for wet bulb
        Ew = 6.108 * (math.exp((17.27 * wetbulb_temp) / (237.3 + wetbulb_temp)))

        # actual vapour pressure
        E = Ew - (0.00066 * (1 + 0.00115 * wetbulb_temp) * (weather_condition.temperature - wetbulb_temp) * pressure_in_mb)

        # humidity
        RH = math.ceil(100 * (E / Es))

        if RH < 0:
            RH = 0

        if RH > 100:
            RH = 100

        weather_condition.temperature = round(weather_condition.temperature,1)
        weather_condition.humidity = math.ceil(RH)


        print(weather_condition)
