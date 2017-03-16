import unittest

from calculations.statistics import moving_average


class TestMovingAverage(unittest.TestCase):
    def test_proper_calculation_with_subset_size_1(self):
        self.assertEqual(list(moving_average([1, 2, 3, 4, 5, 6], 1)), [1, 2, 3, 4, 5, 6])

    def test_proper_calculation_with_subset_size_2(self):
        self.assertEqual(list(moving_average([1, 2, 3, 4, 5, 6], 2)), [1.5, 2.5, 3.5, 4.5, 5.5])

    def test_proper_calculation_with_subset_size_6(self):
        self.assertEqual(list(moving_average([1, 2, 3, 4, 5, 6], 6)), [3.5])

    def test_incorrect_subset_size(self):
        """ValueError should be raised
        """
        with self.assertRaises(ValueError):
            moving_average([1, 2, 3, 4, 5, 6], 7)

    def test_incorrect_subset_size_error_message(self):
        """Error message should be equal :
        """
        with self.assertRaises(ValueError) as context:
            moving_average([1, 2, 3, 4, 5, 6], 7)

        self.assertTrue('subset_size must be smaller' in str(context.exception))
