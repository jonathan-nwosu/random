#import API Keys
from dotenv import load_dotenv
import os
load_dotenv()
tavily_key = os.getenv('TAVILY_API_KEY')
langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
langsmith_tracing = os.getenv('LANGSMITH_TRACING')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')


# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


# Create the agent
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229", anthropic_api_key=anthropic_api_key)
search = TavilySearchResults(max_results=2,api_key=tavily_key)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im Jon! and i live in London")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live? Wrong answers only")]}, config
):
    print(chunk)
    print("----")
