import inspect
import unittest

import pytest

import stepikunittest as SU


@pytest.mark.parametrize('traceback', (True, False))
@pytest.mark.parametrize('failfast', (True, False))
def test_create_unitest_executor(traceback, failfast):
    obj = SU.UnittestExecutor(traceback, failfast)
    assert hasattr(obj, '_test_suite')
    assert hasattr(obj, '_test_loader')
    assert hasattr(obj, 'tests_result')
    assert isinstance(obj._test_suite, unittest.TestSuite)
    assert isinstance(obj._test_loader, unittest.TestLoader)
    assert isinstance(obj.tests_result, unittest.TestResult)
    assert obj.tests_result.failfast == failfast
    assert obj.tests_result.tb_locals == traceback
    assert hasattr(obj, 'execute')
    assert inspect.ismethod(obj.execute)
    assert hasattr(obj, 'add_tests')
    assert inspect.ismethod(obj.add_tests)
    assert obj._test_suite.countTestCases() == 0


def test_method_add_tests(unittest_classes):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    obj = SU.UnittestExecutor(True, True)
    obj.add_tests(TestAllTestPassed, TestError, TestFail, TestAllCases)
    assert obj._test_suite.countTestCases() == 8


def test_method_execute(unittest_classes):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    obj = SU.UnittestExecutor(True, False)
    obj.add_tests(TestAllTestPassed, TestError, TestFail, TestAllCases)
    result = obj.execute()
    assert isinstance(result, unittest.TestResult)
    assert len(result.failures) == 2
    assert len(result.errors) == 2
    assert result.testsRun == 8
