import mock

from nose.tools import assert_equals
from weathersimulator.weather import WeatherCondition


def test_weather_condition_condition_is_rainy():
    with mock.patch.multiple('weathersimulator.weather.WeatherCondition', humidity=70, deviation=0.9) as mock_humidity:
        wc1 = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=20)
        assert_equals(wc1.condition, 'Rainy')


def test_weather_condition_condition_is_snowy():
    with mock.patch.multiple('weathersimulator.weather.WeatherCondition', humidity=85, deviation=1.157) as mock_humidity:
        wc1 = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=5)
        assert_equals(wc1.condition, 'Snowy')


def test_weather_condition_condition_is_sunny():
    with mock.patch.multiple('weathersimulator.weather.WeatherCondition', humidity=99, deviation=0.8) as mock_humidity:
        wc1 = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=32)
        assert_equals(wc1.condition, 'Sunny')