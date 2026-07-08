"""
Run all NumPy assignment files from one script.
"""

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


def show(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":
    show("Assignment 1: Array Creation and Manipulation")
    print(replace_third_column())
    print(replace_diagonal_with_zero())

    show("Assignment 2: Array Indexing and Slicing")
    array, sub_array = extract_subarray()
    print(array)
    print(sub_array)
    random_array, border = extract_border_elements()
    print(random_array)
    print(border)

    show("Assignment 3: Array Operations")
    print(element_wise_operations())
    print(row_column_sums())

    show("Assignment 4: Statistical Operations")
    print(calculate_statistics())
    print(normalize_array())

    show("Assignment 5: Broadcasting")
    print(add_array_to_each_row())
    print(subtract_array_from_each_column())

    show("Assignment 6: Linear Algebra")
    print(matrix_properties())
    print(matrix_multiplication())

    show("Assignment 7: Advanced Array Manipulation")
    print(reshape_array_examples())
    print(flatten_and_reshape())

    show("Assignment 8: Fancy Indexing and Boolean Indexing")
    print(extract_corner_elements())
    print(cap_values_greater_than_ten())

    show("Assignment 9: Structured Arrays")
    print(sort_people_by_age())
    print(calculate_point_distances())

    show("Assignment 10: Masked Arrays")
    print(mask_values_greater_than_ten())
    print(replace_diagonal_with_unmasked_mean())
