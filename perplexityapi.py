from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

#logic of market research agent
# 1/ get user input to understand what topic to research
# 2/ Use perplexity API to find some interesting facts 
# 3/ Use Claude API to modify the structure 
# 4/ Ask user if the post is good or not if user approves store post in DB
# 5/ Ask the user when to schedule post 

perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')

user_topic = input("What topic would you like to know interesting facts about? ")

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
            f"Give me 5 interesting facts with stats about {user_topic}. With the 3 interesting stats make sure to include the sources"
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


