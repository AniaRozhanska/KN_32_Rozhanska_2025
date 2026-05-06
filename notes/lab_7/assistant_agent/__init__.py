from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

root_agent = Agent(
    model='gemini-2.5-flash',
    name='assistant_agent',
    description="Збалансований універсальний асистент.",
    instruction="""
    Ти — професійний і дружній асистент.
    - Допомагай користувачеві структурувати думки, планувати завдання та знаходити інформацію.
    - Твій тон має бути збалансованим: не занадто сухим, але й не художнім.
    - Використовуй списки та абзаци для структурування відповідей.
    - Відповідай українською мовою.
    """,
    generate_content_config=GenerateContentConfig(
        temperature=0.7,  # Золота середина
        top_k=25,         # Помірна різноманітність слів
        top_p=0.9,        # Збалансований вибір
    )
)