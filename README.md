LinkedIn Post Generator with AI Research
A Python-based tool that automatically generates professional LinkedIn posts by combining AI research and formatting capabilities.
Features

AI-powered research using Perplexity AI
Professional post formatting with Claude
Automated post structure with emojis
Secure API handling

Setup

Install dependencies:

bashCopypip install openai anthropic python-dotenv

Create .env file:

CopyPERPLEXITY_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
Usage
Run:
bashCopypython main.py
Follow the prompts to enter your topic and receive a formatted LinkedIn post.
Structure

PerplexityResearcher: Handles research via Perplexity AI
LinkedInPostFormatter: Formats posts using Claude

Requirements

Python 3.8+
Perplexity AI API key
Anthropic API key

Troubleshooting

Check API keys in .env
Verify internet connection
Ensure all dependencies are installed
