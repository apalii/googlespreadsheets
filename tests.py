import unittest

from calculations.statistics import moving_average


class TestMovingAverageCalculations(unittest.TestCase):

    def test_proper_calculation_with_subset_size_1(self):
        self.assertEqual(list(moving_average([1, 2, 3, 4, 5, 6], 1)), [1, 2, 3, 4, 5, 6])

    def test_proper_calculation_with_subset_size_2(self):
        self.assertEqual(list(moving_average([1, 2, 3, 4, 5, 6], 2)), [1.5, 2.5, 3.5, 4.5, 5.5])

    def test_proper_calculation_with_subset_size_6(self):
        self.assertEqual(list(moving_average([1, 2, 3, 4, 5, 6], 6)), [3.5])


class TestInputData(unittest.TestCase):

    def test_data_size_less_subset_size(self):
        """Test exception and error message: data < subset_size
        """
        with self.assertRaises(ValueError) as context:
            list(moving_average([1, 2, 3, 4, 5, 6], 7))

        self.assertTrue('subset_size must be smaller' in str(context.exception))

    def test_subset_size_less_one(self):
        """Test exception and error message: subset_size < 1
        """
        with self.assertRaises(ValueError) as context:
            list(moving_average([1, 2, 3, 4, 5, 6], 0))

        self.assertTrue('subset_size must be 1 or larger' in str(context.exception))

    def test_subset_size_is_not_int(self):
        with self.assertRaisesRegex(TypeError, 'subset_size must be integer'):
            list(moving_average([1, 2, 3, 4, 5, 6], "2"))
