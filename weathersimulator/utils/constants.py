"""
Constants that are used by the weather simulator utility.
"""

# https://en.wikipedia.org/wiki/U.S._Standard_Atmosphere
# height:           Metres,
# static_pressure:  Pascals,
# standard_temp:    Kelvin,
# lapse_rate:       Kelvin per Metre
ATMOSPHERIC_LAYER = [
    {
        'name': 'Troposphere', 'height': 0,
        'static_pressure': 101325.00,
        'standard_temp': 288.15,
        'lapse_rate': -0.0065
    },
    {
        'name': 'Tropopause',
        'height': 11000,
        'static_pressure': 22632.10,
        'standard_temp': 216.65,
        'lapse_rate': 0.0
    },
    {
        'name': 'Stratosphere',
        'height': 20000,
        'static_pressure': 5474.89,
        'standard_temp': 216.65,
        'lapse_rate': 0.001
    },
    {
        'name': 'Stratopause',
        'height': 32000,
        'static_pressure': 868.02,
        'standard_temp': 228.65,
        'lapse_rate': 0.0028
    },
    {
        'name': 'Mesosphere',
        'height': 47000,
        'static_pressure': 110.91,
        'standard_temp': 270.65,
        'lapse_rate': 0.0
    },
    {
        'name': 'Mesopause',
        'height': 51000,
        'static_pressure': 66.94,
        'standard_temp': 270.65,
        'lapse_rate': -0.0028
    },
    {
        'name': 'Thermosphere',
        'height': 71000,
        'static_pressure': 3.96,
        'standard_temp': 214.65,
        'lapse_rate': -0.002
    }
]

GRAVITY = 9.80665
EARTH_AIR_MOLAR_MASS = 0.0289644
UNIVERSAL_GAS_CONSTANT = 8.3144598
