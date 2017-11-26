from nose.tools import assert_equals
import pycodestyle
import glob


def test_pycodestyle_compliance():
    files_to_check = []

    for filename in glob.iglob('../weathersimulator/*.py', recursive=True):
        files_to_check.append(filename)

    codestyle = pycodestyle.StyleGuide(config_file='setup.cfg')
    result = codestyle.check_files(files_to_check)

    assert_equals(result.total_errors, 0, "Found code style errors (and warnings).")