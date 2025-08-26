#Translator Tool - English to German translation using Google Gemini LLM

import os
import google.generativeai as genai

class TranslatorTool:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    def translate(self, text: str) -> dict:
        if not text or not text.strip():
            return {"success": False, "error": "Empty text provided", "original": text}
        
        try:
            prompt = f"""Translate the following English text to German. 
            Provide only the German translation, nothing else.
            
            English: {text}
            German:"""
            
            response = self.model.generate_content(prompt)
            german_text = response.text.strip()
            
            # Clean up the response - remove any extra formatting
            if german_text.startswith("German:"):
                german_text = german_text[7:].strip()
            
            return {
                "success": True,
                "original": text,
                "translation": german_text,
                "language_pair": "en-de"
            }
            
        except Exception as e:
            return {
                "success": False, 
                "error": f"Translation failed: {str(e)}", 
                "original": text
            }

if __name__ == "__main__":
    try:
        translator = TranslatorTool()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your GEMINI_API_KEY environment variable")