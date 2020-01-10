# -*- coding: utf-8 -*-
"""
Attributes
----------
MSG_TEMPLATES : collections.collections
    Container for default message templates. Fields:
    correct
        The text of the message on the successful completion of the tests.
    statistics
        Template for a string with test statistics. Template for a string with test
        statistics. The template should contain fields: total, passed, failed, errors.
    failed
        Template for a string with information falling test. The template should contain
        field: name of the test.
    error
        Template for a string with information about test errors. The template should
        contain field: name of the test.
    description
        Template for a string describing the test. The template should
        contain field: test description.
"""

import unittest
from collections import namedtuple

MessageTemplates = namedtuple(
    'MessageTemplates',
    ['correct', 'statistics', 'failed', 'error', 'description' ])

MSG_TEMPLATES = MessageTemplates(
    'All tests passed!\n',
    '\nTest results. Ran: {}. Passed: {}. Failed: {}. Errors: {}.\n',
    'Failed test: {}.\n',
    'Test error: {}.\n',
    '{}\n',
)


class UnittestExecutor:
    """Class wrap to get test results.

    Attributes
    ----------
    _test_suite : unittest.TestSuit
    _test_loader : unittest.TestLoader
    tests_result : unittest.TestResult
    """

    def __init__(self, traceback, failfast):
        """Creates an instance of the UnittestExecutor.

        Parameters
        ----------
        traceback : bool
        failfast : bool
        """
        self._test_suite = unittest.TestSuite()
        self._test_loader = unittest.TestLoader()
        self.tests_result = unittest.TestResult()
        self.tests_result.tb_locals = traceback
        self.tests_result.failfast = failfast

    def add_tests(self, *test_classes):
        """A method for adding test classes to a test suite.

        Parameters
        ----------
        *test_classes :
        """
        for test_class in test_classes:
            tests = self._test_loader.loadTestsFromTestCase(test_class)
            self._test_suite.addTest(tests)

    def execute(self):
        """The method starts running tests. Returns the value of the tests_result
        attribute.

        Returns
        -------
        tests_result : unittest.TestResult
            The result of the tests.
        """
        self._test_suite.run(self.tests_result)
        return self.tests_result


class UnittestReportCreator:
    """The class provides a tool for creating a test report message."""

    def __init__(self, statistics, title, description, msg_limit, msg_templates):
        """Creates an instance of the UnittestReportCreator.

        Parameters
        ----------
        statistics : bool
            The flag of the presence of the statistics line. If false, the statistics
            line will not be added to the test result message (default: True).
        title : bool
            The flag of the presence of the line with information falling/errors teste.
            If false, the title will not be added to the test result message (default: True).
        description : bool
            Flag for the presence of a line with a description of the test. If false,
            the description line will not be added to the test result message (default: True).
        msg_limit : int
            The maximum allowable number of failed tests, information about which is
            displayed in the test results message.
        msg_templates : collections.namedtuple
            Named tuple with message templates.
        """

        self.statistics = statistics
        self.title = title
        self.description = description
        self.msg_limit = msg_limit
        self.msg_templates = msg_templates

    def create_statistics_msg(self, tests_result):
        """Returns a string with statistics about the test results. It contains
        information about the number of tests: total, passed, failed, errors.

        Parameters
        ----------
        tests_result : unittest.TestResult
            The result of the test.

        Returns
        -------
        str
            A string of statistics.
        """

        total = tests_result.testsRun
        errors = len(tests_result.errors)
        failed = len(tests_result.failures)

        if errors == 0 and failed == 0:
            return self.msg_templates.statistics.format(total, total, failed, errors)

        if tests_result.failfast:
            passed = total - 1
            failed = 1 - errors
        else:
            passed = total - failed - errors

        return self.msg_templates.statistics.format(total, passed, failed, errors)

    def create_report(self, tests_result):
        """Returns a string with a test report message.

        Parameters
        ----------
        tests_result : unittest.TestResult
            The result of the test.

        Returns
        -------
        str
            Test report message.
        """

        report = ''

        if self.statistics:
            report += self.create_statistics_msg(tests_result)

        if tests_result.wasSuccessful() and not tests_result.errors:
            return report + self.msg_templates.correct

        if tests_result.errors:
            test_cases = tests_result.errors
            title_template = self.msg_templates.error
        else:
            test_cases = tests_result.failures
            title_template = self.msg_templates.failed

        for test_case, traceback in test_cases:

            if self.title:
                test_name = test_case.id().split('.').pop()
                report += title_template.format(test_name)

            if self.description:
                report += self.msg_templates.description.format(
                    test_case.shortDescription())

            if tests_result.tb_locals:
                report += traceback

            if self.msg_limit <= 1:
                return report

            self.msg_limit -= 1

        return report


def grade(*test_classes, failfast=True, statistics=True, title=True,
          description=True, traceback=True, msg_limit=5, msg_templates=MSG_TEMPLATES,
          executor_type=UnittestExecutor, reporter_type=UnittestReportCreator):
    """

    Notes.
    -----
    The parameters: title, description, traceback determine what information will
    be added to the report. The maximum number of messages about failed tests is
    limited by of the msg_limit attribute. If the test result is positive, the value
    the value of the correct_msg attribute is returned. If there were errors in
    the test results, information about them is added to the report. Otherwise,
    information about the failed tests is added to the report.

    Parameters
    ----------
    *test_classes : unittest.TestCase
    failfast : bool
    traceback : bool
    statistics : bool
        The flag of the presence of the statistics line. If false, the statistics
        line will not be added to the test result message (default: True).
    title : bool
        The flag of the presence of the line with information falling/errors teste.
        If false, the title will not be added to the test result message (default: True).
    description : bool
        Flag for the presence of a line with a description of the test. If false,
        the description line will not be added to the test result message (default: True).
    msg_limit : int
        The maximum allowable number of failed tests, information about which is
        displayed in the test results message.
    executor_type
        Class of test runner (default - UnittestExecutor).
    reporter_type
        Test report creator class (default - UnittestReportCreator).
    """

    executor = executor_type(traceback, failfast)
    executor.add_tests(*test_classes)
    reporter = reporter_type(statistics, title, description, msg_limit, msg_templates)
    tests_result = executor.execute()
    return reporter.create_report(tests_result)
