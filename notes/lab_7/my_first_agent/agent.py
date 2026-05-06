import logging
# Налаштовуємо вивід усіх логів рівня DEBUG прямо в консоль
logging.basicConfig(level=logging.DEBUG)

from google.adk import llm  # Спробуємо через llms

model = llms.GoogleLLM(
    model_name="gemini-1.5-flash",
    use_vertexai=False,
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
# Визначаємо функцію-інструмент
def get_current_time(city: str) -> dict:
    """
    Повертає поточний час у вказаному місті.

    Args:
        city: назва міста

    Returns:
        dict: інформація про час у вказаному місті
    """
    # Це mock-реалізація для демонстрації
    import datetime
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return {
        "status": "success",
        "city": city,
        "time": current_time
    }
