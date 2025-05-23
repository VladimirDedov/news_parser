import openai
from dotenv import load_dotenv
import os
import requests

from openai import api_key

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Придумай анекдот про кота и программиста"}
    ]
)

print(response.model_dump_json())
