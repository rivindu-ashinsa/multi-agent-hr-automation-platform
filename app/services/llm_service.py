from groq import Groq

from app.core.config import (
    GROQ_API_KEY
)

client = Groq(
    api_key=GROQ_API_KEY,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "what's the capital of France",
        }
    ],
    model="llama-3.3-70b-versatile",
    max_tokens=300
)


def generate_response(prompt: str):

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

        temperature=0.3
    )

    return (
        completion
        .choices[0]
        .message
        .content
    )

print(generate_response("What is the capital of France?"))