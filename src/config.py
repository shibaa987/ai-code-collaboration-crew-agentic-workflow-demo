import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_llm():
    """Return LLM based on available environment"""

    # if os.getenv("OPENAI_API_KEY"):
    #     return LLM(
    #         model="gpt-4o-mini",
    #         temperature=0.2
    #     )
    if os.getenv("AIRCS_AI_API_KEY"):
        return LLM(
            # model="groq/llama-3.1-8b-instant",
            model=os.getenv("AI_MODEL"),
            api_key=os.getenv("AIRCS_AI_API_KEY"),
            base_url=os.getenv("AIRCS_AI_API_URL")
        )
    else:
        return LLM(
            model="ollama/llama3:8b",
            base_url="http://localhost:11434",
            temperature=0.2
        )
