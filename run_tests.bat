 nosetests --with-xunit --all-modules --traverse-namespace --with-coverage --cover-package=weathersimulator --cover-inclusive
 python -m coverage xml --include=../weathersimulator*
 pylint -f parseable weathersimulator | tee pylint.out