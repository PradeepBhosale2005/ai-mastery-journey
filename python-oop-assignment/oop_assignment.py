"""
Assignment: Object-Oriented Programming (OOP) Concepts in Python

This script covers:
1. Class creation
2. Inheritance
3. Encapsulation
4. Polymorphism
5. Abstraction
"""

from abc import ABC, abstractmethod
import math


class Student:
    """Represents a student with name, private age, and grade."""

    def __init__(self, name: str, age: int, grade: str) -> None:
        self.name = name
        self.__age = None
        self.grade = grade
        self.set_age(age)

    def set_age(self, age: int) -> None:
        """Set the student's age after validating it."""
        if not isinstance(age, int):
            raise TypeError("Age must be an integer.")
        if age <= 0:
            raise ValueError("Age must be greater than zero.")
        self.__age = age

    def get_age(self) -> int:
        """Return the student's private age."""
        return self.__age

    def display_info(self) -> str:
        """Return the student's information as a formatted string."""
        return f"Name: {self.name}, Age: {self.get_age()}, Grade: {self.grade}"


class HighSchoolStudent(Student):
    """Represents a high school student using inheritance from Student."""

    def __init__(self, name: str, age: int, grade: str, grade_level: int) -> None:
        super().__init__(name, age, grade)
        self.grade_level = grade_level

    def display_info(self) -> str:
        """Return high school student information including grade level."""
        return (
            f"Name: {self.name}, Age: {self.get_age()}, Grade: {self.grade}, "
            f"Grade Level: {self.grade_level}"
        )


def print_student_info(student: Student) -> None:
    """
    Demonstrates polymorphism.

    This function accepts either Student or HighSchoolStudent and calls the
    display_info() method. Python automatically uses the correct version of
    display_info() based on the object type.
    """
    print(student.display_info())


class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def calculate_area(self) -> float:
        """Calculate and return the area of the shape."""
        pass


class Circle(Shape):
    """Represents a circle."""

    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("Radius must be greater than zero.")
        self.radius = radius

    def calculate_area(self) -> float:
        """Return the area of the circle."""
        return math.pi * self.radius * self.radius


class Rectangle(Shape):
    """Represents a rectangle."""

    def __init__(self, length: float, width: float) -> None:
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be greater than zero.")
        self.length = length
        self.width = width

    def calculate_area(self) -> float:
        """Return the area of the rectangle."""
        return self.length * self.width


if __name__ == "__main__":
    print("OOP Assignment Demo")
    print("-------------------")

    # Class creation and encapsulation example
    student = Student("Pradeep", 25, "A")
    print_student_info(student)

    # Updating private age using setter method
    student.set_age(26)
    print("Updated age:", student.get_age())

    # Inheritance and method overriding example
    high_school_student = HighSchoolStudent("Rahul", 16, "A+", 11)
    print_student_info(high_school_student)

    # Abstraction examples
    circle = Circle(5)
    rectangle = Rectangle(10, 4)

    print("Circle area:", round(circle.calculate_area(), 2))
    print("Rectangle area:", rectangle.calculate_area())
