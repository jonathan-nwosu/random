from openai import OpenAI
import os
from typing import List, Dict
from dotenv import load_dotenv
from anthropic import Anthropic

class LinkedInPostFormatter:
    """
    Handles the formatting of research content into LinkedIn-ready posts using Claude.
    
    Attributes:
        anthropic: Anthropic client instance for interacting with Claude API
    """

    def __init__(self):
        load_dotenv()
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def format_post(self, research_content: str, topic: str) -> str:
        """Format research content into a LinkedIn post using Claude."""
        prompt = f"""Format this research about {topic} into a LinkedIn post with exactly this structure:
        
        [Title] This headline should draw the reader in but avoid using anything that sounds hyperbolic. The title does need to be gripping though. 
        The title should pull readers in and grab attention in a sea of posts online. Don't use words like revolutionise. 

        [Two opening lines about the topic. These should be non obvious, slightly contrarian takes that are insighful yet not mainstream ideas...] 
        
        👉 [Point 1]
        👉 [Point 2]
        👉 [Point 3]
        👉 [Point 4]
        👉 [Point 5]
        
        [Two closing lines] The closing lines should be insightful and draw on insights from the points made above. Again the reader must feel as 
        as though they've learnt something. Don't just have a conclusion write something that is thought provoking and challenges convetnional wisdom.
        It needs to be interesting and sharable. 
        
        Use exactly 4-5 emojis total throughout the post (including title). Place the emojis naturally within the text.
        Return the post as plain text with proper line breaks.
        Do not include any text formatting symbols, just the plain text and emojis.The reader should leave feeling like they've taken in some valuable insights and information.

        Here's the research:
        {research_content}"""

        message = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text.strip()

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
        self.formatter = LinkedInPostFormatter()

    def create_prompt(self, topic: str) -> List[Dict[str, str]]:
        """Create the message prompt for the API."""
        return [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant that provides "
                    "detailed, factual research with statistics and sources."
                ),
            },
            {   
                "role": "user",
                "content": (
                    f"Give me 5 interesting facts with stats about {topic}. "
                    "Include sources for any statistical claims. Focus on recent "
                    "and impactful data that would be engaging for a professional audience."
                ),
            },
        ]

    def get_research(self, topic: str, stream: bool = True) -> str:
        """Get research results from Perplexity API and format as LinkedIn post."""
        messages = self.create_prompt(topic)
        
        if stream:
            research_content = self._stream_response(messages)
        else:
            research_content = self._get_complete_response(messages)
        
        formatted_post = self.formatter.format_post(research_content, topic)
        return formatted_post

    def _stream_response(self, messages: List[Dict[str, str]]) -> str:
        """Handle streaming response from API."""
        response_stream = self.client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
            stream=True,
        )
        
        content = []
        print("Gathering research...")
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                content_piece = chunk.choices[0].delta.content
                content.append(content_piece)
        
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
        topic = input("What topic would you like to create a LinkedIn post about? ")
        print("\nResearching and formatting your LinkedIn post...")
        formatted_post = researcher.get_research(topic)
        print("\nYour LinkedIn Post:\n")
        print(formatted_post)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()