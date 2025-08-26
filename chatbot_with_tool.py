#Level 2 - MEDIUM: LLM + Basic Tool Use (Gemini Version)

import os
import re
import json
from datetime import datetime
import google.generativeai as genai
from calculator_tool import CalculatorTool

class ChatbotWithTool:
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.calculator = CalculatorTool()
        self.system_prompt = (
            """You are a helpful assistant with access to a calculator tool.
            RULES:
            1. If the user asks a math calculation, you MUST use the calculator tool
            2. For non-math questions, answer directly with step-by-step reasoning
            3. Always structure your output clearly
            4. If the query contains MULTIPLE different types of tasks (like math + general knowledge), 
            say "I can only handle one type of task at a time. Please ask me one question at a time."

            Math keywords to detect: add, plus, +, subtract, minus, -, multiply, times, *, divide, ÷, /, calculate, what is X + Y, etc.

            Format responses:
            - For math: "I'll use the calculator tool to solve this."
            - For other questions: Use step-by-step reasoning
            """
        )

    #To detect math query for passing to calculator tool
    def detect_math_query(self, text: str) -> bool:
        math_patterns = [
            r"\d+\s*[\+\-\*/xX÷]\s*\d+",
            r"\b(add|plus|subtract|minus|multiply|times|divide|calculate)\b",
        ]
        return any(re.search(p, text.lower()) for p in math_patterns)

    def has_multiple_task_types(self, query: str) -> bool:
        return (
            self.detect_math_query(query)
            and any(w in query.lower() for w in ["capital", "why", "explain"])
            and "and" in query.lower()
        )

    def get_llm_response(self, user_input: str) -> str:
        response = self.model.generate_content(f"{self.system_prompt}\nUser: {user_input}")
        return response.text.strip()
    
    #To process the query to use calculator tool
    def process_query(self, user_input: str) -> str:
        if self.has_multiple_task_types(user_input):
            return "I can only handle one type of task at a time. Please ask a single question."
        if self.detect_math_query(user_input):
            result = self.calculator.calculate(user_input)
            if result["success"]:
                return f"I'll use the calculator tool.\nResult: {result['result']}"
            return f"Calculator error: {result['error']}"
        return self.get_llm_response(user_input)

    def log_interaction(self, user_input: str, bot_response: str, used_tool: bool = False):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": ts,
            "user_input": user_input,
            "bot_response": bot_response,
            "tool_used": "calculator" if used_tool else None,
        }
        with open("level2_interactions.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{ts}]\n")
            f.write(f"User: {user_input}\n")
            f.write(f"Bot: {bot_response}\n")
            f.write("-" * 50 + "\n")

    def run(self):
        print("Smart Assistant Level 2 - Gemini Version")
        print("Type 'quit' to exit\n")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"quit", "exit"}:
                break
            if not user_input:
                continue
            print("Bot: Processing...")
            response = self.process_query(user_input)
            used_tool = self.detect_math_query(user_input)
            print(f"Bot: {response}\n")
            self.log_interaction(user_input, response, used_tool)

if __name__ == "__main__":
    try:
        bot = ChatbotWithTool()
    except ValueError as e:
        print(f"{e}")
        exit(1)
    bot.run()
