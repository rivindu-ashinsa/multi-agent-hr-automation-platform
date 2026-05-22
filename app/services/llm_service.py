from groq import Groq

from app.core.config import (
    GROQ_API_KEY
)

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def _fallback_response(prompt: str) -> str:
    if not GROQ_API_KEY:
        return (
            "I am unable to respond right now because the LLM API key is not configured. "
            "Please set GROQ_API_KEY and try again."
        )

    return (
        "I could not complete that request right now. "
        "Please try again in a moment or rephrase your message."
    )


def generate_response(prompt: str):
    if client is None:
        return _fallback_response(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an HR assistant."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,
            max_tokens=300,
        )

        content = completion.choices[0].message.content
        return content or _fallback_response(prompt)
    except Exception:
        return _fallback_response(prompt)

# print(generate_response("What is the capital of France?"))