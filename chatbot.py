#Level 1 - EASY: LLM-Only Smart Assistant Using Google Gemini API

import google.generativeai as genai
import os
from datetime import datetime

class SmartChatbot:
    def __init__(self):
        # Configure Gemini API key
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        self.model = genai.GenerativeModel("gemini-2.5-flash")

        self.system_prompt = """You are a helpful assistant that ALWAYS follows these rules:

1. THINK STEP-BY-STEP for every response
2. Structure your output with clear numbered steps
3. For math calculations, you MUST refuse and suggest using a calculator tool instead
4. Always be precise and educational

Format your responses like this:
Step 1: [First step of reasoning]
Step 2: [Second step of reasoning]
...
Final Answer: [Your conclusion]

IMPORTANT: If the user asks for math calculations (addition, multiplication, division, subtraction), 
you must refuse and say "I cannot perform calculations. Please use a calculator tool for accurate results."
"""

    def get_response(self, user_input):
        try:
            response = self.model.generate_content(
                f"{self.system_prompt}\nUser: {user_input}"
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def log_interaction(self, user_input, bot_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("level1_interactions.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"User: {user_input}\n")
            f.write(f"Bot: {bot_response}\n")
            f.write("-" * 50 + "\n")

    def run(self):
        print("Smart Assistant Level 1 - LLM Only (Gemini API)")
        print("Type 'quit' to exit\n")
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if not user_input:
                continue
                
            print("Bot: Thinking...")
            response = self.get_response(user_input)
            print(f"Bot: {response}\n")
            
            self.log_interaction(user_input, response)

if __name__ == "__main__":
    if not os.getenv('GEMINI_API_KEY'):
        print("Please set GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your-api-key-here'")
        exit(1)
    
    chatbot = SmartChatbot()
    chatbot.run()
