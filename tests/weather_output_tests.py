import math
import re
from nose.tools import assert_in, assert_true
from weathersimulator.weather import WeatherCondition


def test_weather_output_values_are_correct():
    wc = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=20)
    wc.calculate()

    output = str(wc)

    assert_in(wc.name, output)
    assert_in(str(wc.temperature), output)
    assert_in(str(wc.humidity), output)

    pretty_pressure = str(math.ceil(wc.pressure/100))
    assert_in(pretty_pressure, output)

    assert_in(wc.condition, output)

    pretty_datetime = wc.datetime.isoformat().replace('+','Z')
    assert_in(pretty_datetime, output)

    assert_in(str(wc.longitude), output)

    assert_in(str(wc.latitude), output)

    assert_in(str(wc.elevation), output)


def test_weather_output_format_is_correct():
    wc = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=20)
    wc.calculate()

    output = str(wc)

    # Darwin|-12.46113,130.84185,31|1970-12-31T09:30:00Z09:30|Sunny|25.5|980|83
    expected = "\s*|\d+,\d+,\d+|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\d{2}:\d{2}|\s+|\d+|\d+|\d+"
    assert_true(re.match(expected, output, re.IGNORECASE))
