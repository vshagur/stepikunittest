# -*- coding: utf-8 -*-

class UnittestReportCreator:
    """The class provides a tool for creating a test report message.

    Attributes
    ----------
    correct_msg : str
        The text of the message on the successful completion of the tests.
    statistics_msg : str
        Template for a string with test statistics. Template for a string with test
        statistics. The template should contain fields: total, passed, failed, errors.
    failed_msg : str
        Template for a string with information falling test. The template should contain
        field: name of the test.
    error_msg : str
        Template for a string with information about test errors. The template should
        contain field: name of the test.
    description_msg : str
        Template for a string describing the test. The template should
        contain field: test description.

    """

    correct_msg = 'All tests passed!\n'
    statistics_msg = '\nTest results. Run: {}. Passed: {}. Failed: {}. Errors: {}.\n'
    failed_msg = 'Failed test: {}.\n'
    error_msg = 'Test error: {}.\n'
    description_msg = '{}\n'

    def __init__(self, statistics, title, description, msg_limit):
        """Creates an instance of the UnittestFormatter class.

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

        """
        self.statistics = statistics
        self.title = title
        self.description = description
        self.msg_limit = msg_limit

    def _create_message(self, tests_result):
        """Returns a string with a report of failed tests or errors.

        Note.
        -----
        The attributes
        title, description, traceback determine what information will be added to
        the report. The maximum number of messages about failed tests is limited by
        of the msg_limit attribute. If the test result is positive, the value
        the value of the correct_msg attribute is returned. If there were errors in
        the test results, information about them is added to the report. Otherwise,
        information about the failed tests is added to the report.

        Parameters
        ----------
        tests_result : unittest.TestResult
            The result of the test.

        Returns
        -------
        str
            A string of reports of failed tests or errors.
        """
        message = ''

        if tests_result.errors:
            test_cases = tests_result.errors
            title_template = self.error_msg
        else:
            test_cases = tests_result.failures
            title_template = self.failed_msg

        for test_case, traceback in test_cases:

            test_name = test_case.id().split('.').pop()
            title = title_template.format(test_name) if self.title else ''

            if self.description:
                description = self.description_msg.format(
                    test_case.shortDescription())
            else:
                description = ''

            traceback = traceback if tests_result.tb_locals else ''
            message += (title + description + traceback)

            if self.msg_limit <= 1:
                return message

            self.msg_limit -= 1

        return message

    def _get_stats_line(self, tests_result):
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
            return self.statistics_msg.format(total, total, failed, errors)

        if tests_result.failfast:
            passed = total - 1
            failed = 1 - errors
        else:
            passed = total - failed

        return self.statistics_msg.format(total, passed, failed, errors)

    def __call__(self, tests_result):
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
        stats_line = self._get_stats_line(tests_result) if self.statistics else ''

        if tests_result.wasSuccessful() and not tests_result.errors:
            return stats_line + self.correct_msg

        return stats_line + self._create_message(tests_result)


print(help(UnittestFormatter))
