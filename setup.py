from setuptools import setup, find_packages

setup(
    name='WeatherSimulator',
    use_scm_version=True,
    packages=find_packages(),
    scripts=['generate_weather.py'],
    author='Nathon Fowlie',
    author_email='nathon.fowlie@gmail.com',
    description='Simple weather simulator',
    license='MIT',
    url='https://github.com/nathonfowlie/python.weathersimulator',
    setup_requires=['setuptools_scm'],
    tests_require=['mock', 'pycodestyle', 'nose', 'coverage'],
    include_package_data=True,
    package_data={
        'weathersimulator': ['schemas/*.json']
    },
    test_suite='nose.collector'
)

