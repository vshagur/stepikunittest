import pytest

import stepikunittest as SU


@pytest.mark.parametrize('statistics', (True, False))
@pytest.mark.parametrize('title', (True, False))
@pytest.mark.parametrize('description', (True, False))
@pytest.mark.parametrize('msg_limit', (1, 4, 5, 6))
def test_create_unittest_report_creator(statistics, title, description, msg_limit):
    msg_templates = SU.MSG_TEMPLATES
    obj = SU.UnittestReportCreator(
        statistics, title, description, msg_limit, msg_templates)
    assert obj.statistics == statistics
    assert obj.title == title
    assert obj.description == description
    assert obj.msg_limit == msg_limit
    assert obj.msg_templates == msg_templates


def test_method_create_statistics_msg(result_tests):
    obj = SU.UnittestReportCreator(True, True, True, 5, SU.MSG_TEMPLATES)
    expected = SU.MSG_TEMPLATES.statistics.format('8', '4', '2', '2')
    stat_line = obj.create_statistics_msg(result_tests)
    assert stat_line == expected


def test_method_create_statistics_msg_all_tests_passed(result_tests_all_tests_passed):
    obj = SU.UnittestReportCreator(True, True, True, 5, SU.MSG_TEMPLATES)
    expected = SU.MSG_TEMPLATES.statistics.format('2', '2', '0', '0')
    stat_line = obj.create_statistics_msg(result_tests_all_tests_passed)
    assert stat_line == expected


def test_method_create_statistics_msg_failfast_true(result_tests_failfast_true):
    obj = SU.UnittestReportCreator(True, True, True, 5, SU.MSG_TEMPLATES)
    expected = SU.MSG_TEMPLATES.statistics.format('3', '2', '0', '1')
    stat_line = obj.create_statistics_msg(result_tests_failfast_true)
    assert stat_line == expected


@pytest.mark.parametrize('statistics', (True, False))
def test_method_create_report_all_tests_passed(result_tests_all_tests_passed, statistics):
    obj = SU.UnittestReportCreator(statistics, True, True, 5, SU.MSG_TEMPLATES)
    feedback = obj.create_report(result_tests_all_tests_passed)
    stat_line = SU.MSG_TEMPLATES.statistics.format('2', '2', '0', '0')

    if statistics:
        assert stat_line in feedback
    else:
        assert stat_line not in feedback

    assert SU.MSG_TEMPLATES.correct in feedback


@pytest.mark.parametrize('description', (True, False))
@pytest.mark.parametrize('title', (True, False))
@pytest.mark.parametrize('statistics', (True, False))
def test_method_create_report_error_case(result_tests, statistics, title, description):
    obj = SU.UnittestReportCreator(statistics, title, description, 5, SU.MSG_TEMPLATES)
    feedback = obj.create_report(result_tests)
    # check statistics line
    stat_line = SU.MSG_TEMPLATES.statistics.format('8', '4', '2', '2')

    if statistics:
        assert stat_line in feedback
    else:
        assert stat_line not in feedback

    # check title line
    title_line = SU.MSG_TEMPLATES.error.format('test_7')

    if title:
        assert title_line in feedback
    else:
        assert title_line not in feedback

    # check description line
    description_line = SU.MSG_TEMPLATES.description.format('TestAllCases, test_7')

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
def test_method_create_report_fail_case(result_tests_fail, statistics, title,
                                        description):
    obj = SU.UnittestReportCreator(statistics, title, description, 5, SU.MSG_TEMPLATES)
    feedback = obj.create_report(result_tests_fail)
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
