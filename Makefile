LOCATION_DATA := data/locations.json
VIRTUALENV := env/scripts/activate
MIN_TEST_COVERAGE := 50
START_DATE := '01/01/1970'
END_DATE := '31/01/1970'
VERSION='0.1.0'

default: lint

clean:
	$(info ********** Removing temporary build directories **********)
	rm -rf env
	rm -f *.pyd *.pyc *.pyo *.bak *$$py.class
	rm -rf build dist *.egg-info __pycache__
	rm -f .coverage .coverate.* coverage.xml
	rm -f MANIFEST

	rm -rf doc/_build/*

lint: _virtualenv
	$(info ********** Linting solution **********)

	# Don't fail on warnings, usage or convention errors
	pylint -f parseable weathersimulator; if [ $$? -eq 4 ] || [ $$? -eq 8 ] || [ $$? -eq 16 ] || [ $$? -eq 32 ] ; then exit 0 ; fi

test: _virtualenv
	$(info ********** Running Nose & Coverage Tests **********)
	python setup.py nosetests --with-coverage --cover-min-percentage=$(MIN_TEST_COVERAGE)

build: _virtualenv
	$(info ********* Building WeatherSimulator **********)
	pip install .
	python setup.py egg_info -Db "" sdist bdist_egg

install:
	python setup.py install

develop: _virtualenv
	$(info ********** Installing Development version **********)
	pip install -e .
	python setup.py develop

publish: _virtualenv
	$(info ********** Publishing WeatherSimulator **********)
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags
	# Publish to artifact repository

run:
	python ./generate_weather.py -f $(LOCATION_DATA) -s $(START_DATE) -e $(END_DATE)

_virtualenv:
	$(info ********** Configuring virtual environment and installing dependencies **********)
	virtualenv env
	. $(VIRTUALENV)
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install -r requirements.txt

.PHONY: clean lint test develop run build publish
