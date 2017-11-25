import arrow
from utils.constants import ATMOSPHERIC_LAYER, GRAVITY, UNIVERSAL_GAS_CONSTANT, EARTH_AIR_MOLAR_MASS
from random import random, uniform
import math


class WeatherCondition(object):
    #wetbulb_temp = round(random.uniform(drybulb_temp - 9, drybulb_temp), 2)

    def __init__(self, name='', latitude=0, longitude=0, elevation=0, datetime=arrow.now(), temperature=15):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.datetime = datetime
        self.temperature = temperature

        self.__pressure = None  # We'll calculate air pressure later on
        self.__deviation = 1.0  # Don't randomize current air pressure

        self.__calculate_pressure()

    @property
    def elevation(self):
        return self._elevation


    @elevation.setter
    def elevation(self , elevation):
        self._elevation = elevation


    @property
    def condition(self):
        # In relation to snow, when the humidity is high pressure is high and temperature is low snow is formed.
        # When the humidity is high, pressure is constant and temperature is high the snow melts.
        if self.humidity >= 80 and self.__deviation >= 1.1 and self.temperature <= 10:
            return 'Snowy'
        # Additional temperature limit of 25 degrees added as it doesn't make sense for it to be 32 degress and rainy..
        elif self.humidity > 60 and self.__deviation < 1.0 and self.temperature < 25:
            return 'Rainy'
        else:
            return 'Sunny'


    def __calculate_pressure(self):
        self.__deviation = uniform(0.8, 1.2)
        self.__pressure = 101325.0

        for i in range(0, 7):
            static_pressure = ATMOSPHERIC_LAYER[i]['static_pressure']
            standard_temp = ATMOSPHERIC_LAYER[i]['standard_temp']
            lapse_rate = ATMOSPHERIC_LAYER[i]['lapse_rate']
            min_height = ATMOSPHERIC_LAYER[i]['height']

            if min_height <= self.elevation <= ATMOSPHERIC_LAYER[i + 1]['height']:
                x = standard_temp / (standard_temp + lapse_rate * (self.elevation - min_height))
                y = (GRAVITY * EARTH_AIR_MOLAR_MASS) / (UNIVERSAL_GAS_CONSTANT * lapse_rate)
                self.__pressure = static_pressure * math.pow(x, y)

                # Allow air pressure to fluctuate +/- 20%. This will cause humidity to increase/decreaase and impact
                # whether it is sunny, snowy or rainy
                self.__pressure *= self.__deviation


    @property
    def pressure(self):
        return self.__pressure


    @property
    def humidity(self):
        return self._humidity


    @humidity.setter
    def humidity(self, humidity=50):
        self._humidity = humidity


    def __str__(self):
        geo_location = '{0},{1},{2}'.format(self.latitude, self.longitude, self.elevation)

        output = "{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(self.name, geo_location, self.datetime.isoformat().replace('+', 'Z'), self.condition,
                                                      round(self.temperature, 1), math.ceil(self.pressure), math.ceil(self.humidity))

        return output
