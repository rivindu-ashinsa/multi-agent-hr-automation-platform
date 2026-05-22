from fastapi import FastAPI

from app.api.routes import router

from app.core.database import init_db


app = FastAPI()

init_db()

app.include_router(router)


# import os

# from groq import Groq

# client = Groq(
#     api_key=os.environ.get("grok_api"),
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "what's the capital of France",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
#     max_tokens=300
# )

# print(chat_completion.choices[0].message.content)