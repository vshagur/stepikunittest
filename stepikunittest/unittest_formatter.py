class UnittestFormatter:
    correct_msg = 'All tests passed!\n'
    statistics_msg = '\nTest results. Run: {}. Passed: {}. Failed: {}. Errors: {}.\n'
    failed_msg = 'Failed test: {}.\n'
    error_msg = 'Test error: {}.\n'
    description_msg = '{}\n'

    def __init__(self, statistics, title, description, msg_limit):
        self.msg_limit = msg_limit
        self.statistics = statistics
        self.title = title
        self.description = description

    def _get_stats_line(self, tests_result):

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

    def _create_message(self, tests_result):
        message = ''

        if tests_result.errors:
            test_cases = tests_result.errors
            title_template = self.error_msg
        else:
            test_cases = tests_result.failures
            title_template = self.failed_msg

        for test_case_obj, traceback in test_cases:

            test_name = test_case_obj.id().split('.').pop()
            title = title_template.format(test_name) if self.title else ''

            if self.description:
                description = self.description_msg.format(
                    test_case_obj.shortDescription())
            else:
                description = ''

            traceback = traceback if tests_result.tb_locals else ''
            message += (title + description + traceback)

            if tests_result.failfast or self.msg_limit <= 1:
                return message

            self.msg_limit -= 1

        return message

    def __call__(self, tests_result):
        stats_line = self._get_stats_line(tests_result) if self.statistics else ''

        if tests_result.wasSuccessful() and not tests_result.errors:
            return stats_line + self.correct_msg

        return stats_line + self._create_message(tests_result)
