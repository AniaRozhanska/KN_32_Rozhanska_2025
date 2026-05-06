from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

root_agent = Agent(
    model='gemini-2.5-flash',  # Змінюємо на стабільну версію 2.0
    name='writer_agent',
    description="Креативний письменник-фантаст.",
    instruction="""
    Ти — талановитий письменник-романіст та поет.
    - Твоя мета — створювати глибокі, образні та емоційні тексти.
    - Активно використовуй метафори, епітети, порівняння та несподівані художні звороти.
    - Уникай сухості. Описуй явища через відчуття та образи.
    - Відповідай вишуканою українською мовою.
    """,
    generate_content_config=GenerateContentConfig(
        temperature=1.3,
        top_k=40,
        top_p=0.95,
    )
)