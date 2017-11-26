"""
Main module for the weather simulator. This module contains the
WeatherCondition class which can be leveraged to auto-generate
believable weather data for a specific location at a specific
date and time.
"""
from random import uniform
import numbers
import math
import arrow
import six

from weathersimulator.utils.constants import ATMOSPHERIC_LAYER, EARTH_AIR_MOLAR_MASS, GRAVITY, UNIVERSAL_GAS_CONSTANT,\
    CALIBRATION_TEMPERATURE


# The following resources were used to create the formulas used for air
# pressure and humidity
# https: // en.wikipedia.org / wiki / Barometric_formula
# https://maps.googleapis.com/maps/api/geocode/json?address=Sydney
# http://www.weatherzone.com.au/climate/station.jsp?lt=site&lc=70351
# http://www.1728.org/relhum.htm
# http://maxwellsci.com/print/rjaset/v6-2984-2987.pdf
# https://en.wikipedia.org/wiki/Vapour_pressure_of_water (Buck equation).
# https://en.wikipedia.org/wiki/Arden_Buck_equation
# https://cals.arizona.edu/azmet/dewpoint.html
# https://www.engineeringtoolbox.com/humidity-ratio-air-d_686.html
class WeatherCondition(object):  # pylint: disable=R0902
    """
    This class represents weather information for a single location, at a
    specific point in time. After initialising a class instance,
    WeatherCondition.calculate() should be called to calculate temperature,
    humidity, air pressure and weather conditions.

    Example:
        wc = WeatherCondition(latitude=51.807222, longitude=0.021389,
                              elevation=46, temperature=15)
        wc.name = 'Greenwich'
        wc.datetime = datetime=datetime.now()
        wc.calculate()

        # Print an estimated air pressure in Greenwich for the given
        # temperature and date.
        print(wc.pressure)

        # Print an estimated air pressure in Greenwich for the given
        # temperature and date.
        print(wc.humidity)

        if wc.condition == 'Sunny':
            foo()

        print(wc) # Print the string representation of the weather condition.
    """
    __WETBULB_MAX_DEVIATION = 8

    def __init__(self, latitude, longitude, elevation, temperature, datetime=None, name=None):  # pylint: disable=R0913
        """
        Instantiates a new instance of the WeatherCondition class, which can
        be used to generate believable weather data for any given date.

        :param name: Optional name of the location.
        :param latitude: The locations latitude. Must be numeric, between -90 and 90 degrees.
        :param longitude: The locations latitude. Must be numeric, between -180 and 180 degress.
        :param elevation: The elevation in metres.
        :param temperature: The temperature in degrees celsius.
        :param datetime: The local date and time that the weather condition is for. Must be in ISO8601 format.
        """
        # Initialising attributes here to keep pylint happy. They are initialised properly during the calls to their
        # respective properties defined a few lines below...
        self.__name = None
        self.__humidity = None
        self.__elevation = None
        self.__latitude = None
        self.__longitude = None
        self.__temperature = None
        self.__min_temperature = None
        self.__wetbulb_temp = None

        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.temperature = temperature

        self.__calculate_pressure()

        self.datetime = datetime if datetime else arrow.now()

    @property
    def deviation(self):
        """
        Gets the percentage deviation from standard air pressure for the locations altitude.

        :return: The amount that the current locations air pressure varies from it's standard air pressure at the given
            altitude.
        """
        return self.__deviation

    @property
    def condition(self):
        """
        Gets the current weather conditions based on air pressure, temperature and humidity.

        :return: Returns one of three possible string values - Sunny, Rainy or Snowy.
        """
        # When the humidity is high, pressure is high and temperature is low snow is formed.
        if self.humidity >= 80 and self.deviation >= 1.1 and self.temperature <= 10:
            return 'Snowy'
        # Temperature limit of 25 degrees added as it doesn't make sense for it
        # to be 32 degress and rainy..
        elif self.humidity > 60 and self.deviation < 1.0 and self.temperature < 25:
            return 'Rainy'

        return 'Sunny'

    @property
    def elevation(self):
        """
        Gets the locations elevation (metres).

        :return: The elevation.
        """
        return self.__elevation

    @elevation.setter
    def elevation(self, elevation):
        """
        Sets the locations elevation.

        :param elevation: The elevation. This must be a numeric value.
        """
        if not isinstance(elevation, six.integer_types):
            raise TypeError('elevation must be numeric')

        self.__elevation = elevation

    @property
    def humidity(self):
        """
        Gets the relative humidity (percentage).

        :return: The humidity expressed as a percentage.
        """
        return math.ceil(self.__humidity)

    @property
    def latitude(self):
        """
        Gets the locations latitude.

        :return: The latitude.
        """
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude):
        """
        Sets the locations latitude.

        :param latitude: The latitude. Must be a numeric value between -90 and 90.
        """
        if not isinstance(latitude, float) or -90 < latitude > 90:
            raise TypeError('latitude must be a float between -90 and 90')

        self.__latitude = latitude

    @property
    def longitude(self):
        """
        Gets the locations longitude.

        :return: The longitude.
        """
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude):
        """
        Sets the locations longitude.

        :param longitude: The longitude. This must be a numeric value between -180 and 180.
        """
        if not isinstance(longitude, float) or -180 < longitude > 180:
            raise TypeError('longitude must be a float between -180 and 180')

        self.__longitude = longitude

    @property
    def min_temperature(self):
        """
        The minimum allowable temperature that can be generated for this location instance.

        :return: Temperature in degrees celsius
        """
        return self.__min_temperature

    @property
    def name(self):
        """
        Gets the human readable name of the location (Sydney, London etc).

        :return: The name of the location eg: city/town/region.
        """
        return self.__name

    @name.setter
    def name(self, name):
        """
        Sets the location name.

        :param name: The name to assign to the location.
        """
        if name and not isinstance(name, six.string_types):
            raise TypeError('name must be a non-empty string')

        self.__name = name

    @property
    def temperature(self):
        """
        Gets the locations temperature.

        :return: The temperature, in degress celsius.
        """
        return self.__temperature

    @temperature.setter
    def temperature(self, temperature):
        """
        Sets the locations temperature.

        :param temperature: The temperature, in degrees celsius.
        """
        if not isinstance(temperature, numbers.Real):
            raise TypeError('temperature must be numeric - {0}'.format(temperature))

        self.__temperature = temperature

    @property
    def wetbulb_temp(self):
        """
        Gets the Wet Bulb temperature used to calculate humidity.

        :return: The wet bulb temperature.
        """
        return self.__wetbulb_temp

    def calculate(self):
        """
        Calculates the air pressure, humidity and weather conditions based on elevation, location and historical
        temperature data.
        """
        self.__calculate_pressure()
        self.__calculate_humidity()

    def __calculate_pressure(self):
        """
        Calculates air pressure based on the current elevation, and randomly generated deviation which is calculated on
        object instantiation to make weather conditions more realistic by randomising air pressure, so that the
        temperature, humidity and conditions for any given WeatherCondition instance are always different.
        """
        # Allow air pressure to fluctuate +/- 20%. This will cause humidity to increase/decrease, impacting whether it
        # is sunny, snowy or rainy. In theory this should make the generated results more believable.
        self.__deviation = uniform(0.8, 1.2)

        pressure = 101325.0  # Default air pressure at sea level

        for i in range(0, 7):
            static_pressure = ATMOSPHERIC_LAYER[i]['static_pressure']
            std_temp = ATMOSPHERIC_LAYER[i]['standard_temp']
            lapse_rate = ATMOSPHERIC_LAYER[i]['lapse_rate']
            min_height = ATMOSPHERIC_LAYER[i]['height']

            next_height = ATMOSPHERIC_LAYER[i + 1]['height'] if i < 6 else min_height

            if min_height <= self.elevation <= next_height:
                height_diff = self.elevation - min_height
                g_v_m = GRAVITY * EARTH_AIR_MOLAR_MASS

                base = std_temp / (std_temp + lapse_rate * height_diff)
                exponent = g_v_m / (UNIVERSAL_GAS_CONSTANT * lapse_rate)

                pressure = static_pressure * math.pow(base, exponent)
                pressure *= self.deviation

        self.pressure = pressure

    def __calculate_humidity(self):
        """
        Calculates humidity given the current weather conditions (temperature, elevation etc).
        """
        # Formula requires air pressure to be in millibars, so have to convert from hPa
        pressure_in_mb = self.pressure * 0.01

        # FIXME: Improve wet bulb temperature calculation  # pylint: disable=W0511
        # An artificial limit of 9 degrees variation between dry and wet bulb temperatures has been used to prevent
        # negative actual vapour pressure values (does not occur in nature).
        #
        # A better algorithm would be to calculate the min/max achievable wet bulb temperature for the given dry bulb
        # temperature, and generate a random number that falls within the calculated range.
        #
        # Table at https://www.eduplace.com/science/hmxs/es/pdf/5rs_3_2-3.pdf used to validate the correctness of the
        # humidity results stops at a 10 degrees difference (there may be some variation in results due to rounding).
        self.__min_temperature = uniform(self.temperature - WeatherCondition.__WETBULB_MAX_DEVIATION, self.temperature)
        self.__wetbulb_temp = uniform(self.min_temperature, self.temperature)

        # saturation vapour pressure for dry bulb
        dry_temp_in_k = self.__celsius_to_kelvin(self.temperature)
        equation_1 = 17.27 * self.temperature
        sat_vap_pressure_dry = CALIBRATION_TEMPERATURE * (math.exp(equation_1 / dry_temp_in_k))

        # saturation vapour pressure for wet bulb
        wet_temp_in_k = self.__celsius_to_kelvin(self.wetbulb_temp)
        equation_2 = 17.27 * self.wetbulb_temp
        sat_vap_pressure_wet = CALIBRATION_TEMPERATURE * (math.exp(equation_2 / wet_temp_in_k))

        # actual vapour pressure
        temp_diff = self.temperature - self.wetbulb_temp
        equation_3 = (1 + 0.00115 * self.wetbulb_temp)
        vap_pressure = sat_vap_pressure_wet - (0.00066 * equation_3 * temp_diff * pressure_in_mb)

        # humidity
        humidity = 100 * (vap_pressure / sat_vap_pressure_dry)

        if humidity < 0:
            humidity = 0

        if humidity > 100:
            humidity = 100

        # Round up to nearest whole number, purely because I've never seen a fractional humidity figure on the news or
        # in any of the sources I used to determine how to calculate humidity/pressure.
        self.__humidity = humidity


    def __celsius_to_kelvin(self, temperature):
        """
        Converts degrees celsius to Kelvin.

        :param temperature: The temperature (celsius) to be converted to Kelvin.

        :return: The same temperature expressed in Kelvin
        """
        return temperature + 237.3


    def __str__(self):
        """
        Override the string representation of this class to simplify generating the flat file output.

        :return: Returns a string in flat-file format that contains the weather conditions for the location.
        """
        pretty_geoloc = f'{self.latitude},{self.longitude},{self.elevation}'

        pretty_temperature = round(self.temperature, 1)
        pretty_pressure = math.ceil(self.pressure / 100)
        pretty_humidity = math.ceil(self.humidity)
        pretty_datetime = self.datetime.isoformat().replace('+', 'Z')

        # sample output:
        # Broome|-17.95538,122.23922,12|1970-01-11T08:00:00Z08:00|Sunny|25.7|951|60
        output = f'{self.name}|{pretty_geoloc}|{pretty_datetime}|{self.condition}|{pretty_temperature}|' \
                 f'{pretty_pressure}|{pretty_humidity}'

        return output
