import unittest
import pytest

@pytest.fixture()
def classes_for_tests():
    class TestOne(unittest.TestCase):
        def test_1(self):
            self.assertEqual(1, 0)

        def test_2(self):
            self.assertEqual(3, 3)

    class TestTwo(unittest.TestCase):
        def test_3(self):
            raise TypeError

    return TestOne, TestTwo

@pytest.fixture()
def result_tests(classes_for_tests):
    result = unittest.TestResult()
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()

    for test_class in classes_for_tests:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTest(tests)

    test_suite.run(result)
    return result
