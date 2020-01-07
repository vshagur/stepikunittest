import unittest


class UnittestExecutor:
    def __init__(self, traceback, failfast):
        self._test_suite = unittest.TestSuite()
        self._test_loader = unittest.TestLoader()
        self.tests_result = unittest.TestResult()
        self.tests_result.tb_locals = traceback
        self.tests_result.failfast = failfast

    def add_tests(self, test_classes_list):
        for test_class in test_classes_list:
            tests = self._test_loader.loadTestsFromTestCase(test_class)
            self._test_suite.addTest(tests)

    def __call__(self):
        self._test_suite.run(self.tests_result)
        return self.tests_result
