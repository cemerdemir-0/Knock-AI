from google import genai
from dotenv import load_dotenv
from rag import get_context
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_doors(user_text, emotions):
    emotions_str = ", ".join(emotions)
    historical_context = get_context(user_text, k=3)

    prompt = (
        "You are a poetic interpreter living in 1973 America — the era of Vietnam War,\n"
        "Bob Dylan, and the counterculture movement. But you also know that grief is timeless.\n\n"
        f'A person wrote: "{user_text}"\n'
        f"Their dominant emotions are: {emotions_str}\n\n"
        "Here is some relevant historical context from 1973 and beyond that resonates with their words:\n"
        "---\n"
        f"{historical_context}\n"
        "---\n"
        "Use this historical context to deepen and ground your interpretations. Let the real voices\n"
        "from these eras speak through your writing. Do not copy the context directly — let it\n"
        "inform the tone, imagery, and emotional truth of what you write.\n\n"
        "Based on these emotions and this historical context, match the person to exactly 4 symbolic doors:\n"
        "1. Billy the Kid's Door — the outlaw escaping everything, the frontier myth, no way back\n"
        "2. The Vietnam Soldier's Door — returning to a world that moved on, carrying what cannot be named\n"
        "3. Dylan's Door — the artist turning his back on the system, the refusal to be what others need\n"
        "4. The Survivor's Door — February 6, 2023, Turkiye. The door that opened without warning.\n\n"
        "For each door:\n"
        "- Write a title (e.g. Billy the Kid's Door)\n"
        "- Write 2-3 sentences explaining why this person is knocking on this door\n"
        "- Write a short 4-line Dylan-style poem for this door\n\n"
        "Format your response exactly like this for each door:\n"
        "DOOR: [title]\n"
        "REASON: [explanation]\n"
        "POEM:\n"
        "[4 lines]\n"
        "---\n"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    return response.text


def generate_custom_door(user_text, emotions, door_concept):
    """Kullanicinin kendi tanimladigi esige ozel bir kapi ismi ve siir uretir."""
    emotions_str = ", ".join(emotions)
    historical_context = get_context(door_concept, k=2)

    prompt = (
        "You are a poetic interpreter living in 1973 America — the era of Bob Dylan,\n"
        "Vietnam, and the counterculture. But you understand that grief and transition are timeless.\n\n"
        f'A person wrote about their life: "{user_text}"\n'
        f"Their dominant emotions are: {emotions_str}\n"
        f'They described their own threshold as: "{door_concept}"\n\n'
        "Historical echoes that resonate with their words:\n"
        "---\n"
        f"{historical_context}\n"
        "---\n\n"
        "Create a unique, deeply personal symbolic door for this specific person.\n"
        "This door should NOT be one of the four archetypal doors (Billy, Vietnam, Dylan, Survivor).\n"
        "Give it a poetic, original name that captures their exact situation.\n"
        "Write 2-3 sentences about why this is their door.\n"
        "Write a 4-line Dylan-style poem that speaks directly to their threshold.\n\n"
        "Format your response exactly like this:\n"
        "DOOR: [unique door name]\n"
        "REASON: [explanation]\n"
        "POEM:\n"
        "[4 lines]\n"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    return response.text


if __name__ == "__main__":
    test_emotions = ["sadness", "fear", "anticipation"]
    test_text = "I am leaving my country to start a new life abroad"
    result = generate_doors(test_text, test_emotions)
    print(result)
