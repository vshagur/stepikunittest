import pytest

import stepikunittest as SU


@pytest.mark.parametrize('statistics', (True, False))
def test_grade_all_tests_passed(unittest_classes, statistics):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    feedback = SU.grade(TestAllTestPassed, statistics=statistics)
    stat_line = SU.MSG_TEMPLATES.statistics.format('2', '2', '0', '0')

    if statistics:
        assert stat_line in feedback
    else:
        assert stat_line not in feedback

    assert SU.MSG_TEMPLATES.correct in feedback


@pytest.mark.parametrize('description', (True, False))
@pytest.mark.parametrize('title', (True, False))
@pytest.mark.parametrize('statistics', (True, False))
def test_grade_errors(unittest_classes, statistics, title, description):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    feedback = SU.grade(
        TestError, statistics=statistics, title=title, description=description)

    # check statistics line
    stat_line = SU.MSG_TEMPLATES.statistics.format('1', '0', '0', '1')

    if statistics:
        assert stat_line in feedback
    else:
        assert stat_line not in feedback

    # check title line
    title_line = SU.MSG_TEMPLATES.error.format('test_3')

    if title:
        assert title_line in feedback
    else:
        assert title_line not in feedback

    # check description line
    description_line = SU.MSG_TEMPLATES.description.format('TestError, test_3')

    if description:
        assert description_line in feedback
    else:
        assert description_line not in feedback

    # check traceback
    traceback = 'Traceback (most recent call last)'

    assert traceback in feedback


@pytest.mark.parametrize('description', (True, False))
@pytest.mark.parametrize('title', (True, False))
@pytest.mark.parametrize('statistics', (True, False))
def test_grade_fails(unittest_classes, statistics, title, description):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    feedback = SU.grade(
        TestFail, statistics=statistics, title=title, description=description)

    # check statistics line
    stat_line = SU.MSG_TEMPLATES.statistics.format('1', '0', '1', '0')

    if statistics:
        assert stat_line in feedback
    else:
        assert stat_line not in feedback

    # check title line
    title_line = SU.MSG_TEMPLATES.failed.format('test_4')

    if title:
        assert title_line in feedback
    else:
        assert title_line not in feedback

    # check description line
    description_line = SU.MSG_TEMPLATES.description.format('TestFail, test_4')

    if description:
        assert description_line in feedback
    else:
        assert description_line not in feedback

    # check traceback
    traceback = 'Traceback (most recent call last)'

    assert traceback in feedback
