import pytest

import stepikunittest as SU


@pytest.mark.parametrize('statistics', (True, False))
def test_grade_all_tests_passed(unittest_classes, statistics, ):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    feedback = SU.grade(TestAllTestPassed, statistics=statistics)
    stat_line = SU.MSG_TEMPLATES.statistics.format('2', '2', '0', '0')

    if statistics:
        assert stat_line in feedback
    else:
        assert stat_line not in feedback

    assert SU.MSG_TEMPLATES.correct in feedback
