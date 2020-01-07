from stepikunittest.unittest_executor import UnittestExecutor
from stepikunittest.report_creator import UnittestReportCreator


class TestExecutor:
    def __init__(self, test_classes_list=None, failfast=True, statistics=True,
                 title=True, description=True, traceback=True, msg_limit=5):
        self._executor = UnittestExecutor(traceback, failfast)
        self._executor.add_tests(test_classes_list or [])
        self._reporter = UnittestReportCreator(statistics, title, description, msg_limit)

    def __call__(self):
        return self._reporter(self._executor())
