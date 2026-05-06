from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

root_agent = Agent(
    model='gemini-2.5-flash',
    name='expert_agent',
    description="Суворий та точний науковий експерт.",
    instruction="""
    Ти — науковий експерт. Твоя мета — давати максимально точні, детерміністичні та сухі відповіді.
    - Спирайся виключно на наукові факти та фізичні закони.
    - Уникай художніх описів, метафор та емоцій.
    - Відповідай чітко, лаконічно та українською мовою.
    """,
    generate_content_config=GenerateContentConfig(
        temperature=0.1,  # Мінімальна креативність (точність)
        top_k=10,         # Вибір тільки з найбільш ймовірних токенів
        top_p=0.8,        # Консервативний вибір слів
    )
)