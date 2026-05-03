from google import genai
from dotenv import load_dotenv
from rag import get_context
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_doors(user_text: str, emotions: list) -> str:
    emotions_str = ", ".join(emotions)
    context = get_context(user_text)

    prompt = f"""
    You are a poetic interpreter living in 1973 America — the era of Vietnam War,
    Bob Dylan, and the counterculture movement. But you also know that grief is timeless.

    Use the following historical context to deepen and ground your response:
    ---
    {context}
    ---

    A person wrote: "{user_text}"
    Their dominant emotions are: {emotions_str}

    Based on these emotions, match them to exactly 4 symbolic "doors":
    1. Billy the Kid's Door — the outlaw escaping everything
    2. The Vietnam Soldier's Door — returning to a world that moved on
    3. Dylan's Door — the artist turning his back on the system
    4. The Survivor's Door — February 6, 2023, Türkiye. The door that opened without warning. Not a choice, not a farewell — just rubble where home used to be. For those who grieve without reason, who lost without warning.

    For each door:
    - Write a title (e.g. "Billy the Kid's Door")
    - Write 2-3 sentences explaining why this person is knocking on this door, drawing on the historical context provided
    - Write a short 4-line Dylan-style poem for this door

    Format your response exactly like this for each door:
    DOOR: [title]
    REASON: [explanation]
    POEM:
    [4 lines]
    ---
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    test_emotions = ["sadness", "fear", "anticipation"]
    test_text = "I am leaving my country to start a new life abroad"
    result = generate_doors(test_text, test_emotions)
    print(result)