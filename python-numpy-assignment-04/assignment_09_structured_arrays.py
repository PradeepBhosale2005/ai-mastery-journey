"""
Assignment 9: Structured Arrays

1. Create a structured array with fields name, age, and weight.
   Add data and sort the array by age.
2. Create a structured array with fields x and y.
   Add data and compute the Euclidean distance between each pair of points.
"""

import numpy as np


def sort_people_by_age():
    """Create a structured array of people and sort it by age."""
    people_dtype = [("name", "U20"), ("age", "i4"), ("weight", "f4")]
    people = np.array(
        [
            ("Pradeep", 25, 70.5),
            ("Rahul", 21, 68.0),
            ("Sneha", 28, 55.5),
            ("Amit", 23, 72.2),
        ],
        dtype=people_dtype,
    )

    sorted_people = np.sort(people, order="age")
    return people, sorted_people


def calculate_point_distances():
    """Create structured points and compute pairwise Euclidean distances."""
    point_dtype = [("x", "i4"), ("y", "i4")]
    points = np.array([(0, 0), (3, 4), (6, 8)], dtype=point_dtype)

    coordinates = np.column_stack((points["x"], points["y"]))
    differences = coordinates[:, np.newaxis, :] - coordinates[np.newaxis, :, :]
    distances = np.sqrt(np.sum(differences ** 2, axis=2))

    return points, distances


if __name__ == "__main__":
    people, sorted_people = sort_people_by_age()
    print("People structured array:")
    print(people)
    print("People sorted by age:")
    print(sorted_people)

    points, distances = calculate_point_distances()
    print("\nPoints structured array:")
    print(points)
    print("Pairwise Euclidean distances:")
    print(distances)
