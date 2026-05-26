from abc import ABC, abstractmethod
from typing import List

from google.adk import Agent
from google.adk.tools import FunctionTool


class Person(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @abstractmethod
    def get_role(self) -> str:
        pass


class Student(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        self.__grades: List[float] = []

    def get_role(self) -> str:
        return "Student"

    def add_grade(self, grade: float) -> None:
        if not (0 <= grade <= 100):
            raise ValueError("Оцінка повинна бути від 0 до 100")
        self.__grades.append(grade)

    def average(self) -> float:
        if not self.__grades:
            return 0.0
        return sum(self.__grades) / len(self.__grades)

    def min_grade(self) -> float:
        if not self.__grades:
            return 0.0
        return min(self.__grades)

    def max_grade(self) -> float:
        if not self.__grades:
            return 0.0
        return max(self.__grades)


class Teacher(Person):
    def __init__(self, name: str, age: int, subject: str):
        super().__init__(name, age)
        self.subject = subject

    def get_role(self) -> str:
        return "Teacher"

    def evaluate(self, student: Student, grade: float) -> None:
        student.add_grade(grade)


def calculate_grade(name: str, scores: list) -> dict:
    student = Student(name, age=18)
    for score in scores:
        student.add_grade(float(score))

    avg = student.average()
    if avg >= 90:
        letter_grade = "A"
    elif avg >= 75:
        letter_grade = "B"
    elif avg >= 60:
        letter_grade = "C"
    else:
        letter_grade = "F"

    return {
        "student": student.name,
        "average": round(avg, 2),
        "min": student.min_grade(),
        "max": student.max_grade(),
        "letter_grade": letter_grade,
    }


root_agent = Agent(
    name="EducationalAssistant",
    description="Освітній агент для аналізу оцінок студентів.",
    instruction=(
        "Ви — освітній асистент. Коли користувач надає ім'я студента та набір оцінок, "
        "використайте інструмент calculate_grade для точного розрахунку."
    ),
    tools=[FunctionTool(func=calculate_grade)],
)


if __name__ == "__main__":
    example = calculate_grade("Олена", [88, 74, 91, 100, 67])
    print(example)
