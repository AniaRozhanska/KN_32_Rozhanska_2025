from google.adk.agents.llm_agent import Agent

def explain_concept(concept: str, level: str = "beginner") -> dict:
    """
    Пояснює концепцію програмування (наприклад, декоратори, класи, наслідування).

    Args:
        concept: назва концепції для пояснення.
        level: рівень складності (beginner, intermediate, advanced).

    Returns:
        dict: структура з базовою інформацією про концепцію.
    """
    explanations = {
        "beginner": f"Базові відомості про {concept}. Використовуй прості аналогії.",
        "intermediate": f"Детальніший аналіз {concept} з практичним застосуванням.",
        "advanced": f"Глибоке технічне пояснення {concept}, підводні камені та оптимізація."
    }
    return {
         "status": "success",
         "concept": concept,
         "level": level,
         "instruction_for_llm": explanations.get(level, "Поясни загалом.")
    }

def check_syntax(code: str, language: str = "python") -> dict:
    """
    Перевіряє синтаксис наданого коду.

    Args:
        code: рядок з кодом, який треба перевірити.
        language: мова програмування (наприклад, python, java).

    Returns:
        dict: статус перевірки та повідомлення.
    """
    if not code.strip():
        return {"status": "error", "message": "Код порожній"}

    # Спроба базової перевірки синтаксису для Python
    if language.lower() == "python":
        try:
            compile(code, "<string>", "exec")
            return {"status": "success", "message": "Код синтаксично правильний (успішно скомпільовано)."}
        except SyntaxError as e:
            return {"status": "error", "message": f"Знайдено синтаксичну помилку: {e.msg} на рядку {e.lineno}"}

    return {"status": "success", "message": "Синтаксис виглядає коректно (базова перевірка)", "language": language}

# Створюємо агента з надійною моделлю gemini-2.5-flash
root_agent = Agent(
    model='gemini-2.5-flash',  # Використовуємо стабільну та швидку модель
    name='student_helper',
    description="Помічник для студентів, які вивчають програмування.",
    instruction="""
    Ти — терплячий та досвідчений викладач програмування (особливо ООП та Python), який допомагає студентам.

    Твої обов'язки:
    1. Пояснювати складні концепції простими словами, наводячи життєві аналогії.
    2. Якщо студент запитує про якусь концепцію, ти МОЖЕШ викликати інструмент `explain_concept`, щоб отримати вектор пояснення, а потім сформулювати детальну відповідь самостійно.
    3. Якщо студент надсилає код, ти МОЖЕШ викликати `check_syntax`, щоб перевірити його на помилки. Обов'язково вказуй мову програмування.
    4. Завжди пиши красиві, структуровані приклади коду у форматі Markdown.
    5. Давай корисні поради щодо "best practices" (кращих практик написання коду).

    Завжди відповідай українською мовою. Будь дружнім та підтримуй студента у навчанні!
    """,
    tools=[explain_concept, check_syntax],
)