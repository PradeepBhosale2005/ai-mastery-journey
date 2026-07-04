import math
import unittest

from oop_assignment import Circle, HighSchoolStudent, Rectangle, Student


class TestOOPAssignment(unittest.TestCase):
    def test_student_display_info(self):
        student = Student("Pradeep", 25, "A")
        self.assertEqual(student.display_info(), "Name: Pradeep, Age: 25, Grade: A")

    def test_student_age_getter_and_setter(self):
        student = Student("Pradeep", 25, "A")
        student.set_age(26)
        self.assertEqual(student.get_age(), 26)

    def test_student_invalid_age(self):
        with self.assertRaises(ValueError):
            Student("Pradeep", 0, "A")

    def test_high_school_student_display_info(self):
        student = HighSchoolStudent("Rahul", 16, "A+", 11)
        self.assertEqual(
            student.display_info(),
            "Name: Rahul, Age: 16, Grade: A+, Grade Level: 11",
        )

    def test_circle_area(self):
        circle = Circle(5)
        self.assertAlmostEqual(circle.calculate_area(), math.pi * 25)

    def test_rectangle_area(self):
        rectangle = Rectangle(10, 4)
        self.assertEqual(rectangle.calculate_area(), 40)


if __name__ == "__main__":
    unittest.main()
