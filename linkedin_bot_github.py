# linkedin_bot_github.py - Optimized for GitHub Actions
import re
import random
import os
from datetime import datetime
from openai import OpenAI
from typing import Optional

class GitHubLinkedInBot:
    def __init__(self):
        """Initialize with API key from environment variable"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        
        # Expanded topic pool for variety
        self.topics = [
            "MASTERCHEF AUSTRALIA",
            "morning coffee rituals",
            "weekend productivity hacks",
            "remote work funny moments",
            "networking fails and wins",
            "Monday motivation myths",
            "office lunch drama",
            "elevator pitch disasters",
            "work from home pets",
            "meeting mute button fails",
            "career change stories",
            "LinkedIn connection etiquette",
            "interview weird questions",
            "workplace technology fails",
            "team building activities gone wrong",
            "procrastination as an art form",
            "email signature psychology",
            "virtual background mishaps",
            "workplace coffee politics",
            "Friday afternoon energy crashes",
            "startup life reality vs expectation",
            "corporate buzzword bingo",
            "work-life balance myths",
            "the psychology of deadlines",
            "office plant parenthood"
        ]
        
        self.tones = ["funny", "sarcastic", "enthusiastic", "witty", "relatable", "observational"]
    
    def get_chat_response(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """Get response from OpenAI API with error handling"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.8
            )
            content = response.choices[0].message.content.strip()
            # Remove markdown formatting
            cleaned_content = re.sub(r"\*\*(.*?)\*\*", r"\1", content)
            return cleaned_content
        except Exception as e:
            return f"API Error: {str(e)}"
    
    def generate_linkedin_post(self, topic: str, tone: str) -> str:
        """Generate a LinkedIn post"""
        prompt = f"""
        Write a LinkedIn post about {topic}.
        Tone: {tone}
        Requirements:
        - Engaging hook in first line
        - Better audience engagement
        - Call to action at the end
        - Use emojis sparingly but effectively
        - Keep it under 300 words
        - Make it relatable and shareable
        - Include relevant hashtags at the end
        """
        return self.get_chat_response(prompt)
    
    def get_random_topic_and_tone(self):
        """Pick random topic and tone"""
        # Use date as seed for consistency in same day
        random.seed(datetime.now().strftime('%Y%m%d'))
        topic = random.choice(self.topics)
        tone = random.choice(self.tones)
        return topic, tone
    
    def generate_and_save_post(self):
        """Generate today's post and save it"""
        try:
            topic, tone = self.get_random_topic_and_tone()
            
            print("=" * 60)
            print(f"🌅 DAILY LINKEDIN POST - {datetime.now().strftime('%B %d, %Y')}")
            print("=" * 60)
            print(f"📝 Topic: {topic}")
            print(f"🎭 Tone: {tone}")
            print("-" * 60)
            
            post = self.generate_linkedin_post(topic, tone)
            print(post)
            print("\n" + "=" * 60)
            
            # Save to file
            self.save_post_to_file(topic, tone, post)
            
            # Also create a latest.txt for easy access
            with open("latest_post.txt", "w", encoding="utf-8") as f:
                f.write(post)
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def save_post_to_file(self, topic: str, tone: str, post: str):
        """Save post with timestamp"""
        try:
            # Create directory
            os.makedirs("linkedin_posts", exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"linkedin_posts/post_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')}\n")
                f.write(f"Topic: {topic}\n")
                f.write(f"Tone: {tone}\n")
                f.write("-" * 50 + "\n\n")
                f.write(post)
            
            print(f"💾 Post saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️ Could not save: {e}")

def main():
    """Main function for GitHub Actions"""
    print("🤖 Starting LinkedIn Post Generation...")
    
    bot = GitHubLinkedInBot()
    success = bot.generate_and_save_post()
    
    if success:
        print("✅ Daily post generated successfully!")
    else:
        print("❌ Failed to generate post")
        exit(1)

if __name__ == "__main__":
    main()
