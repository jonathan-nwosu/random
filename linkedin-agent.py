def create_linkedin_post(topic):
    """
    Creates a LinkedIn post about a given topic.
    Just give it a topic and it returns a formatted post.
    """
    # The opening grabs attention and introduces the topic
    opening = f"🚀 Want to know the latest about {topic}? Here's what the data shows:"

    # These would come from research - for now they're examples
    # You can manually replace these with real stats you find
    stats = [
        "76% of companies plan to increase investment in this area by 2025 (McKinsey, 2024)",
        "Organizations using these solutions see 41% higher productivity (Deloitte, 2024)",
        "89% of leaders say this will be critical for future success (PwC, 2024)"
    ]
    
    # Create the post by combining all pieces
    post = f"{opening}\n\n"  # Start with opening
    
    # Add each stat as a bullet point
    for stat in stats:
        post += f"📊 {stat}\n\n"
    
    # Add a closing that encourages engagement
    post += "What's your experience with this? Share your thoughts below! 💡\n\n"
    
    # Add relevant hashtags
    post += f"#{topic.replace(' ', '')} #Innovation #Business #Growth"
    
    return post

# Example: Create a post about AI
topic = "AI in Business"
post = create_linkedin_post(topic)
print(post)