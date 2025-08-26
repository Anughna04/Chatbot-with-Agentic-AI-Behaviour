#Level 3 - HARD: Full Agentic AI with Multi-Step Tasks

import os
import re
from datetime import datetime
import google.generativeai as genai
from calculator_tool import CalculatorTool
from translator_tool import TranslatorTool

class FullAgent:
    def __init__(self):
        # Setup Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        # Initialize tools
        self.calculator = CalculatorTool()
        self.translator = TranslatorTool()
        self.conversation_memory = []
        self.system_prompt = ("""You are an advanced AI agent that can break down complex tasks into steps and use tools.
            AVAILABLE TOOLS:
            1. Calculator: For math operations (add, subtract, multiply, divide)
            2. Translator: For English to German translation
            3. Your knowledge: For general questions

            TASK ANALYSIS:
            - Analyze the user's query carefully
            - Identify if it requires multiple steps
            - Determine which tools are needed
            - Execute tasks in logical order
            - Maintain memory of previous steps

            RESPONSE FORMAT:
            For multi-step tasks:
            "I need to break this down into steps:
            Step 1: [Action and result]
            Step 2: [Action and result]
            ...
            Final answer: [Final answer]"

            For single tasks:
            "I'll [action description]
            Result: [result]"

            IMPORTANT: 
            - For math: Use calculator tool
            - For translation: Use translator tool  
            - For general knowledge: Use your knowledge
            - Always be precise and show your reasoning
            """)
    def is_multi_step(self, query: str) -> bool:
        #Check if query needs multiple steps
        query_lower = query.lower()

        if any(indicator in query_lower for indicator in ['and then', 'then ']):
            return True
        
        # Multiple math operations
        math_count = len(re.findall(r'\b(add|multiply|subtract|divide)\s+\d+\s+and\s+\d+', query_lower))
        if math_count > 1:
            return True
        
        # Different tool types needed
        has_translate = 'translate' in query_lower and 'german' in query_lower
        has_math = bool(re.search(r'\b(add|multiply|subtract|divide)\s+\d+\s+and\s+\d+', query_lower))
        has_knowledge = any(word in query_lower for word in ['capital', 'distance', 'tell me'])
        
        tools_needed = sum([has_translate, has_math, has_knowledge])
        return tools_needed > 1

    def split_query(self, query: str) -> list:
        #Split multi-step query into individual steps
        if "and then" in query.lower():
            return [part.strip() for part in re.split(r'\s+and\s+then\s+', query, flags=re.IGNORECASE)]
        elif "then " in query.lower():
            return [part.strip() for part in re.split(r'\s+then\s+', query, flags=re.IGNORECASE)]

        math_matches = list(re.finditer(r'\b(add|multiply|subtract|divide)\s+\d+\s+and\s+\d+', query, re.IGNORECASE))
        if len(math_matches) > 1:
            math_expressions = [match.group(0) for match in math_matches]
            return math_expressions
        
        # Mixed operations - separating translate and math,knowledge
        if 'translate' in query.lower():
            translate_match = re.search(r"translate\s+['\"][^'\"]*['\"].*?german", query, re.IGNORECASE)
            if translate_match:
                translate_part = translate_match.group(0)
                remaining = query.replace(translate_part, "").strip()
                remaining = re.sub(r'^(and\s+then\s+|,\s*|and\s+)', '', remaining, flags=re.IGNORECASE).strip()
                if remaining:
                    if query.find(translate_part) < query.find(remaining):
                        return [translate_part, remaining]
                    else:
                        return [remaining, translate_part]
        
        return [query]

    def process_step(self, step: str) -> str:
        #Process a single step and return result with comprehensive fallback
        step_lower = step.lower()
        
        if 'translate' in step_lower and 'german' in step_lower:
            quote_match = re.search(r"['\"]([^'\"]+)['\"]", step)
            if quote_match:
                text = quote_match.group(1)
                try:
                    result = self.translator.translate(text)
                    if result["success"]:
                        return f"Translated '{text}' to German: '{result['translation']}'"
                    else:
                        # Fallback: Use Gemini for translation
                        fallback_result = self.model.generate_content(f"Translate '{text}' to German. Give only the German translation:")
                        return f"Translated '{text}' to German: '{fallback_result.text.strip()}'"
                except Exception as e:
                    return f"Translation unavailable for '{text}' (Error: {str(e)})"
            else:
                return "Could not extract text to translate from your request"
        
        # Math operations with fallback
        if re.search(r'\b(add|multiply|subtract|divide)\s+\d+\s+and\s+\d+', step_lower):
            try:
                result = self.calculator.calculate(step)
                if result["success"]:
                    return f"Calculated {result['operation']}: {result['result']}"
                else:
                    fallback_result = self.model.generate_content(f"Calculate: {step}. Give only the numeric result:")
                    return f"Calculated result: {fallback_result.text.strip()}"
            except Exception as e:
                return f"Calculation unavailable (Error: {str(e)})"
        
        # Knowledge questions with fallback
        try:
            response = self.model.generate_content(f"Answer this question concisely: {step}")
            return f"Knowledge query: {response.text.strip()}"
        except Exception as e:
            if any(word in step_lower for word in ['capital', 'distance']):
                return f"Knowledge query unavailable (Error: {str(e)}). Please check your internet connection."
            else:
                return f"I cannot process this request right now (Error: {str(e)})"

    def create_final_answer(self, steps_results: list, original_query: str) -> str:
        #Create a consolidated final answer
        if len(steps_results) == 1:
            return steps_results[0]

        final_parts = []
        
        for result in steps_results:
            if "Translated" in result:
                match = re.search(r"'([^']+)'$", result)
                if match:
                    final_parts.append(f"German translation: {match.group(1)}")
            
            elif "Calculated" in result:
                match = re.search(r": ([\d.]+)$", result)
                if match:
                    final_parts.append(f"Calculation result: {match.group(1)}")
            
            elif "Knowledge query:" in result:
                answer = result.replace("Knowledge query: ", "")
                final_parts.append(f"Answer: {answer}")
        
        return " | ".join(final_parts)

    def process_query(self, query: str) -> str:
        #Main processing function with comprehensive fallback behavior
        try:
            if self.is_multi_step(query):
                steps = self.split_query(query)
                
                response = f"I need to break this down into {len(steps)} steps:\n\n"
                steps_results = []
                
                for i, step in enumerate(steps, 1):
                    try:
                        step_result = self.process_step(step)
                        response += f"Step {i}: {step_result}\n"
                        steps_results.append(step_result)
                    except Exception as e:
                        fallback_msg = f"Step {i} failed, using fallback: {str(e)}"
                        response += f"Step {i}: {fallback_msg}\n"
                        steps_results.append(fallback_msg)

                try:
                    final_answer = self.create_final_answer(steps_results, query)
                    response += f"\nFinal Answer: {final_answer}"
                except Exception as e:
                    response += f"\nFinal Answer: Completed {len(steps)} steps (summary unavailable)"
                
            else:
                try:
                    step_result = self.process_step(query)
                    if "Knowledge query:" in step_result:
                        response = f"Based on my knowledge:\n\n{step_result.replace('Knowledge query: ', '')}"
                    elif "Translated" in step_result:
                        response = f"I'll translate this for you.\n\n{step_result}"
                    elif "Calculated" in step_result:
                        response = f"I'll calculate this for you.\n\n{step_result}"
                    else:
                        response = step_result
                except Exception as e:
                    response = f"I'm unable to process your request right now. Error: {str(e)}"
            
            # Save to memory and file
            self.save_interaction(query, response)
            return response
            
        except Exception as e:
            fallback_response = f"I encountered an unexpected error and cannot process your request: {str(e)}"
            try:
                self.save_interaction(query, fallback_response)
            except:
                pass
            return fallback_response

    def save_interaction(self, query: str, response: str):
        """Save interaction to memory and file with fallback"""
        interaction = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "query": query,
            "response": response
        }
        
        # Always save to memory first
        try:
            self.conversation_memory.append(interaction)
        except Exception:
            # Initialize memory if something went wrong
            self.conversation_memory = [interaction]
        
        # Auto-save to file with fallback
        try:
            with open("level3_interactions.txt", 'w', encoding='utf-8') as f:
                f.write("=== FULL AGENT CONVERSATION LOG ===\n\n")
                for i, entry in enumerate(self.conversation_memory, 1):
                    f.write(f"CONVERSATION {i}:\n")
                    f.write(f"Time: {entry['timestamp']}\n")
                    f.write(f"Query: {entry['query']}\n")
                    f.write(f"Response: {entry['response']}\n")
                    f.write("-" * 50 + "\n\n")
        except Exception:
            # Fallback: Try simpler filename
            try:
                with open("history.txt", 'w', encoding='utf-8') as f:
                    f.write(f"Last Query: {query}\n")
                    f.write(f"Last Response: {response}\n")
            except Exception:
                # Final fallback: just continue without saving to file
                pass

    def show_history(self):
        #Display conversation history with fallback
        try:
            if not self.conversation_memory:
                print("No conversation history available.")
                return
            
            print(f"\nConversation History ({len(self.conversation_memory)} entries):")
            for i, entry in enumerate(self.conversation_memory, 1):
                print(f"{i}. [{entry.get('timestamp', 'Unknown time')}]")
                print(f"   Query: {entry.get('query', 'Unknown query')}")
                response = entry.get('response', 'Unknown response')
                print(f"   Response: {response[:80]}{'...' if len(response) > 80 else ''}")
                print()
        except Exception as e:
            print(f"Unable to display history: {str(e)}")
            print("History may be corrupted or unavailable.")

def main():
    #Main CLI interface
    print("=== Level 3 - Full Agentic AI ===")
    print("Commands: 'quit' to exit | 'history' to view past conversations")
    print("(All conversations auto-saved to conversation_history.txt)\n")
    
    try:
        agent = FullAgent()
        print("Agent ready! Enter your queries...")
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye! Your conversation has been saved to conversation_history.txt")
                break
            elif user_input.lower() == 'history':
                agent.show_history()
                continue
            elif not user_input:
                continue
            
            response = agent.process_query(user_input)
            print(f"Bot: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()