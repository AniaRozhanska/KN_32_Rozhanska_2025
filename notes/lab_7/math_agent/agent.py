import math
from google.adk.models import GoogleLLM # Додаємо цей імпорт
from google.adk.agents.llm_agent import Agent

# 1. Спершу налаштовуємо модель, щоб вимкнути Vertex AI
llm = GoogleLLM(
    model_name="gemini-1.5-flash", # Використовуємо реальну назву моделі
    use_vertexai=False             # Це вимикає помилку з Credentials
)

# 2. Функції (інструменти)
def calculate_rectangle_area(width: float, height: float) -> float:
    """Обчислює площу прямокутника."""
    return width * height

def calculate_circle_area(radius: float) -> float:
    """Обчислює площу кола."""
    return math.pi * radius ** 2

def calculate_cube_volume(side: float) -> float:
    """Обчислює об'єм куба."""
    return side ** 3

def calculate_cylinder_volume(radius: float, height: float) -> float:
    """
    Обчислює об'єм циліндра.
    Формула: V = pi * r^2 * h
    """
    return math.pi * (radius ** 2) * height

# 3. Створюємо математичного агента
root_agent = Agent(
    model=llm, # ПЕРЕДАЄМО ОБ'ЄКТ llm, а не рядок
    name='math_agent',
    description="Виконує математичні обчислення геометричних фігур.",
    instruction="""
    Ти експертний математичний асистент, який допомагає з обчисленнями.
    Використовуй ці інструменти для розрахунків.
    Відповідай українською мовою та пояснюй хід обчислень.
    """,
    tools=[
        calculate_rectangle_area,
        calculate_circle_area,
        calculate_cube_volume,
        calculate_cylinder_volume
    ],
)