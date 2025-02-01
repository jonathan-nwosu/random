from openai import OpenAI
import os
from typing import List, Dict

class PerplexityResearcher:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        self.client = OpenAI(
            api_key=self.api_key, 
            base_url="https://api.perplexity.ai"
        )

    def create_prompt(self, topic: str) -> List[Dict[str, str]]:
        """Create the message prompt for the API."""
        return [
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
                    f"Give me 5 interesting facts with stats about {topic}. "
                    "With the 3 interesting stats make sure to include the sources"
                ),
            },
        ]

    def get_research(self, topic: str, stream: bool = True) -> str:
        """Get research results from Perplexity API."""
        messages = self.create_prompt(topic)
        
        if stream:
            return self._stream_response(messages)
        return self._get_complete_response(messages)

    def _stream_response(self, messages: List[Dict[str, str]]) -> str:
        """Handle streaming response from API."""
        response_stream = self.client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
            stream=True,
        )
        
        # Collect the streamed content
        content = []
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                content_piece = chunk.choices[0].delta.content
                content.append(content_piece)
                print(content_piece, end="")  # Keep the streaming output
        
        return "".join(content)

    def _get_complete_response(self, messages: List[Dict[str, str]]) -> str:
        """Handle non-streaming response from API."""
        response = self.client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
        )
        return response.choices[0].message.content

def main():
    try:
        researcher = PerplexityResearcher()
        topic = input("What topic would you like to know interesting facts about? ")
        researcher.get_research(topic)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()