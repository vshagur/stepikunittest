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
