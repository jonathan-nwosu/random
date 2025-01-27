from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {   
        "role": "user",
        "content": (
            "Give me 3 interesting facts with stats about AI in comliance. With the 3 interesting stats make sure to include the sources"
        ),
    },
]

client = OpenAI(api_key=perplexity_api_key, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
)

# chat completion with streaming
response_stream = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
    stream=True,
)

for chunk in response_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


