import mock

from nose.tools import assert_equal, assert_less
from weathersimulator.weather import WeatherCondition


def test_weather_temperature_generates_accurate_humidity():
    # See https://www.engineeringtoolbox.com/humidity-measurement-d_561.html for the dry vs wet bulb lookup table.
    with mock.patch.multiple('weathersimulator.weather.WeatherCondition', deviation=1.0, min_temperature=15,
                             wetbulb_temp=15):
        wc = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=0, temperature=15)
        wc.calculate()
        assert_equal(wc.humidity, 100)

        wc.min_temperature = wc.wetbulb_temp  = 14
        wc.calculate()
        assert_equal(wc.humidity, 90)

        wc.min_temperature = wc.wetbulb_temp = 13
        wc.calculate()
        assert_equal(wc.humidity, 80)

        wc.temperature = 33
        wc.min_temperature = wc.wetbulb_temp = 23
        wc.calculate()
        assert_equal(wc.humidity, 43)


def test_weather_temperature_affects_humidity():
    with mock.patch.multiple('weathersimulator.weather.WeatherCondition', deviation=1.0, min_temperature=20):
        wc1 = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=20)
        wc1.calculate()

        orig_humidity = wc1.humidity
        assert_equal(wc1.humidity, 100)

        wc1.min_temperature=15
        wc1.calculate()
        new_humidity = wc1.humidity

        assert_less(new_humidity, orig_humidity)
