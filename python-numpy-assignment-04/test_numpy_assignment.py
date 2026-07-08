import unittest

import numpy as np

from assignment_01_array_creation import replace_diagonal_with_zero, replace_third_column
from assignment_02_indexing_slicing import extract_border_elements, extract_subarray
from assignment_03_array_operations import element_wise_operations, row_column_sums
from assignment_04_statistical_operations import calculate_statistics, normalize_array
from assignment_05_broadcasting import add_array_to_each_row, subtract_array_from_each_column
from assignment_06_linear_algebra import matrix_multiplication, matrix_properties
from assignment_07_advanced_array_manipulation import flatten_and_reshape, reshape_array_examples
from assignment_08_fancy_boolean_indexing import cap_values_greater_than_ten, extract_corner_elements
from assignment_09_structured_arrays import calculate_point_distances, sort_people_by_age
from assignment_10_masked_arrays import mask_values_greater_than_ten, replace_diagonal_with_unmasked_mean


class TestNumPyAssignment(unittest.TestCase):
    def test_assignment_01(self):
        array = replace_third_column()
        self.assertEqual(array.shape, (5, 5))
        self.assertTrue(np.all(array[:, 2] == 1))

        diagonal_array = replace_diagonal_with_zero()
        self.assertEqual(diagonal_array.shape, (4, 4))
        self.assertTrue(np.all(np.diag(diagonal_array) == 0))

    def test_assignment_02(self):
        array, sub_array = extract_subarray()
        expected = np.array([[14, 15, 16], [20, 21, 22], [26, 27, 28]])
        self.assertEqual(array.shape, (6, 6))
        self.assertTrue(np.array_equal(sub_array, expected))

        border_array, border = extract_border_elements()
        self.assertEqual(border_array.shape, (5, 5))
        self.assertEqual(len(border), 16)

    def test_assignment_03(self):
        a, b, add, sub, mul, div = element_wise_operations()
        self.assertTrue(np.array_equal(add, a + b))
        self.assertTrue(np.array_equal(sub, a - b))
        self.assertTrue(np.array_equal(mul, a * b))
        self.assertTrue(np.allclose(div, a / b))

        array, row_sums, column_sums = row_column_sums()
        self.assertTrue(np.array_equal(row_sums, np.sum(array, axis=1)))
        self.assertTrue(np.array_equal(column_sums, np.sum(array, axis=0)))

    def test_assignment_04(self):
        stats = calculate_statistics()
        self.assertEqual(stats["array"].shape, (5, 5))
        self.assertAlmostEqual(stats["mean"], np.mean(stats["array"]))
        self.assertAlmostEqual(stats["median"], np.median(stats["array"]))

        original, normalized = normalize_array()
        self.assertEqual(original.shape, (3, 3))
        self.assertAlmostEqual(float(np.mean(normalized)), 0.0)
        self.assertAlmostEqual(float(np.std(normalized)), 1.0)

    def test_assignment_05(self):
        matrix, row_values, result = add_array_to_each_row()
        self.assertTrue(np.array_equal(result, matrix + row_values))

        matrix, column_values, result = subtract_array_from_each_column()
        self.assertTrue(np.array_equal(result, matrix - column_values.reshape(4, 1)))

    def test_assignment_06(self):
        matrix, determinant, inverse, eigenvalues = matrix_properties()
        self.assertNotEqual(round(determinant, 8), 0)
        self.assertTrue(np.allclose(matrix @ inverse, np.eye(3)))
        self.assertEqual(len(eigenvalues), 3)

        matrix_one, matrix_two, product = matrix_multiplication()
        self.assertEqual(matrix_one.shape, (2, 3))
        self.assertEqual(matrix_two.shape, (3, 2))
        self.assertTrue(np.array_equal(product, matrix_one @ matrix_two))

    def test_assignment_07(self):
        original, one_by_nine, nine_by_one = reshape_array_examples()
        self.assertEqual(original.shape, (3, 3))
        self.assertEqual(one_by_nine.shape, (1, 9))
        self.assertEqual(nine_by_one.shape, (9, 1))

        array, flattened, reshaped = flatten_and_reshape()
        self.assertEqual(flattened.shape, (25,))
        self.assertTrue(np.array_equal(array, reshaped))

    def test_assignment_08(self):
        array, corners = extract_corner_elements()
        expected = np.array([array[0, 0], array[0, 4], array[4, 0], array[4, 4]])
        self.assertTrue(np.array_equal(corners, expected))

        original, updated = cap_values_greater_than_ten()
        self.assertTrue(np.all(updated <= 10))
        self.assertEqual(original.shape, updated.shape)

    def test_assignment_09(self):
        people, sorted_people = sort_people_by_age()
        sorted_ages = sorted_people["age"]
        self.assertTrue(np.all(sorted_ages[:-1] <= sorted_ages[1:]))

        points, distances = calculate_point_distances()
        self.assertEqual(distances.shape, (len(points), len(points)))
        self.assertTrue(np.allclose(np.diag(distances), 0))

    def test_assignment_10(self):
        array, masked_array, unmasked_sum = mask_values_greater_than_ten()
        self.assertEqual(unmasked_sum, array[array <= 10].sum())
        self.assertTrue(np.all(masked_array.mask == (array > 10)))

        array, masked_array, mean_value, filled_array = replace_diagonal_with_unmasked_mean()
        self.assertTrue(np.all(np.diag(masked_array.mask)))
        self.assertTrue(np.allclose(np.diag(filled_array), mean_value))


if __name__ == "__main__":
    unittest.main()
