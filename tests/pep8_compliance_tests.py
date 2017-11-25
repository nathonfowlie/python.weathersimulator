from nose.tools import assert_equals
import pep8
import glob


def test_pep8_compliance():
    files_to_check = []

    for filename in glob.iglob('../weathersimulator/*.py', recursive=True):
        files_to_check.append(filename)

    pep8style = pep8.StyleGuide()
    result = pep8style.check_files(files_to_check)

    assert_equals(result.total_errors, 0, "Found code style errors (and warnings).")