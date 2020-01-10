import unittest

import pytest


@pytest.fixture()
def unittest_classes():
    class TestAllTestPassed(unittest.TestCase):
        def test_1(self):
            """TestAllTestPassed, test_1"""
            self.assertEqual(1, 1)

        def test_2(self):
            """TestAllTestPassed, test_2"""
            self.assertEqual(3, 3)

    class TestError(unittest.TestCase):
        def test_3(self):
            """TestError, test_3"""
            raise TypeError

    class TestFail(unittest.TestCase):
        def test_4(self):
            """TestFail, test_4"""
            self.assertEqual(3, 0)

    class TestAllCases(unittest.TestCase):
        def test_5(self):
            """TestAllCases, test_5"""
            self.assertEqual(1, 1)

        def test_6(self):
            """TestAllCases, test_6"""
            self.assertEqual(3, 3)

        def test_7(self):
            """TestAllCases, test_7"""
            raise TypeError

        def test_8(self):
            """TestAllCases, test_8"""
            self.assertEqual(3, 0)

    return TestAllTestPassed, TestError, TestFail, TestAllCases


@pytest.fixture()
def result_tests(unittest_classes):
    result = unittest.TestResult()
    result.tb_locals = True
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()

    for test_class in unittest_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTest(tests)

    test_suite.run(result)
    return result


@pytest.fixture()
def result_tests_failfast_true(unittest_classes):
    result = unittest.TestResult()
    result.failfast = True
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()

    for test_class in unittest_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTest(tests)

    test_suite.run(result)
    return result


@pytest.fixture()
def result_tests_all_tests_passed(unittest_classes):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    result = unittest.TestResult()
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    tests = test_loader.loadTestsFromTestCase(TestAllTestPassed)
    test_suite.addTest(tests)
    test_suite.run(result)
    return result


@pytest.fixture()
def result_tests_fail(unittest_classes):
    TestAllTestPassed, TestError, TestFail, TestAllCases = unittest_classes
    result = unittest.TestResult()
    result.tb_locals = True
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    tests = test_loader.loadTestsFromTestCase(TestFail)
    test_suite.addTest(tests)
    test_suite.run(result)
    return result
