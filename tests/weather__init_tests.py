from nose.tools import assert_equals, assert_raises
from weathersimulator.weather import WeatherCondition

def test_WeatherCondition_init():
    wc1 = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=345, temperature=15)
    assert_equals(wc1.name, 'MyCity')
    assert_equals(wc1.latitude, -32.4566)
    assert_equals(wc1.longitude, 158.246912)
    assert_equals(wc1.elevation, 345)
    assert_equals(wc1.temperature, 15)

    wc2 = WeatherCondition(latitude=-32.4566, longitude=158.246912, elevation=345, temperature=15)
    assert_equals(wc2.name, None)


def test_WeatherCondition_init_missing_parameter_throws_TypeError():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', longitude=158.246912, elevation=345, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=-32.4566, elevation=345, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=-32.4566, longitude=158.246912, elevation=1234)


def test_WeatherCondition_init_name_must_be_string():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name=234, latitude=-32.4566, longitude=158.246912, elevation=345, temperature=15)


def test_WeatherCondition_init_temperature_must_be_float_or_integer():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=64, longitude=158.246912, elevation=345, temperature='15')

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=23, longitude=2, elevation=345, temperature=None)


def test_WeatherCondition_init_elevation_must_be_float_or_integer():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=64, longitude=158.246912, elevation='345', temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=23, longitude=2, elevation=None, temperature=15)


def test_WeatherCondition_init_latitude_must_be_float():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude='39', longitude=158.246912, elevation=345, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=None, longitude=158.246912, elevation=345, temperature=15)


def test_WeatherCondition_init_latitude_is_range_bound():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=-91, longitude=158.246912, elevation=345, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=90.000215, longitude=158.246912, elevation=345, temperature=15)


def test_WeatherCondition_init_longitude_must_be_float():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=23, longitude=None, elevation=345, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=23, longitude='158.246912', elevation=345, temperature=15)


def test_WeatherCondition_init_longitude_is_range_bound():
    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=23.534536, longitude=1208.23, elevation=345, temperature=15)

    with assert_raises(TypeError, ) as te:
        wc = WeatherCondition(name='MyCity', latitude=90.000215, longitude=-190.0001, elevation=345, temperature=15)



