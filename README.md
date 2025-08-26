# Chatbot-with-Agentic-AI-Behaviour
# Python Software Engineer Assignment: LLM + Agentic Thinking

This repository contains a complete implementation of the LLM + Agentic AI assignment with three progressive levels of complexity.

## Overview

The project implements an intelligent chatbot system that demonstrates:
- LLM API integration (gemini-2.5-flash)
- Prompt engineering for structured responses
- Tool usage and integration
- Multi-step reasoning and task decomposition
- Agentic AI behavior

## Project Structure

```
├── README.md                           # This file
├── chatbot.py                          # Level 1: Basic LLM chatbot
├── calculator_tool.py                  # Calculator tool for math operations
├── chatbot_with_tool.py                # Level 2: LLM with calculator tool
├── translator_tool.py                  # Translator tool (English to German)
├── full_agent.py                      # Level 3:Full Agentic AI with mutli-step tasks
├── requirements.txt                   # Dependencies for LangChain
├── level1_interactions.txt           # Level 1 interaction logs(text)
├── level2_interactions.txt           # Level 2 interaction logs (text)
├── level3_interactions.txt           # Level 3 interaction logs (text)
```

## Setup Instructions

### Prerequisites
- Python 3.7+
- Gemini API key

### Installation

1. **Clone/Download the project files**

       # Make sure all .py files are in the same directory
   
2.**Install dependencies**

       pip install requiremnts.txt

3.Set the google gemini api key in your environment

      export GEMINI_AI_KEY="YOUR_API_KEY"

4.Run the python code files

      python chatbot.py   #for level1
      python chatbot_with_tool.py   #for level2
      python full_agent.py  #for level3


## How to Run Each Level

### Level 1: Basic LLM Chatbot (EASY)
```bash
python chatbot.py
```

**Features:**
- Step-by-step reasoning for all responses
- Structured output format
- Refuses math calculations and suggests calculator tool
- Logs all interactions to `level1_interactions.log`

**Test Cases:**
- "What are the colors in a rainbow?"
- "Tell me why the sky is blue?"
- "Which planet is the hottest?"
- "What is 15 + 23?" (should refuse)

### Level 2: LLM with Calculator Tool (MEDIUM)
```bash
python chatbot_with_tool.py
```

**Features:**
- Automatically detects math queries
- Uses calculator tool for mathematical operations
- Falls back to LLM for general knowledge
- Handles single-task queries only
- Logs to both text and JSON formats

**Test Cases:**
- "What is 12 times 7?" (uses calculator)
- "Add 45 and 30" (uses calculator)
- "What is the capital of France?" (uses LLM)
- "Multiply 9 and 8, and also tell me the capital of Japan." (graceful failure)

### Level 3: Full Agentic AI (HARD) - Two Implementations
```bash
python full_agent.py
```
**Features**
- **Multi-Step Intelligence**: Automatically breaks down complex queries into logical steps and executes them sequentially
- **Integrated Tools**: Calculator for math operations, translator for English-to-German, and knowledge base for general questions
- **Robust Fallbacks**: Switches to Gemini AI when primary tools fail, ensuring reliable responses even during errors
- **Auto-Save History**: Maintains conversation memory and saves all interactions to file with multiple backup options
- **Smart Processing**: Detects query types and provides step-by-step breakdowns with progress tracking
  
**Test Cases:**
- "Translate 'Good Morning' into German and then multiply 5 and 6."
- "Add 10 and 20, then translate 'Have a nice day' into German."
- "Tell me the capital of Italy, then multiply 12 and 12."
- "Translate 'Sunshine' into German." (single step)
- "Add 2 and 2 and multiply 3 and 3."
- "What is the distance between Earth and Mars?" (LLM only)

##  Tools Description

### Calculator Tool (`calculator_tool.py`)
- Supports basic operations: addition, subtraction, multiplication, division
- Handles multiple input formats: "add 5 and 3", "5 + 3", "multiply 7 and 8"
- Returns structured JSON responses
- Includes error handling for division by zero

### Translator Tool (`translator_tool.py`)
- Translates English to German
- Contains 50+ common words and phrases
- Supports both direct matches and word-by-word translation
- Returns structured JSON responses with translation metadata

## 💡 Usage Examples

### Level 1 Example:
```
You: What are the colors in a rainbow?
Bot: Step 1: Identify the phenomenon - A rainbow is created by light refraction
Step 2: List the colors in order from top to bottom
Step 3: Remember the mnemonic "Roy G. Biv"
Final Answer: Red, Orange, Yellow, Green, Blue, Indigo, Violet
```

### Level 2 Example:
```
You: What is 12 times 7?
Bot: I'll use the calculator tool to solve this.

Calculation: multiplication
Result: 84
```

### Level 3 Example:
```
You: Translate 'Good Morning' into German and then multiply 5 and 6.
Agent: I need to break this down into steps:

Step 1: Translation: 'Good Morning' → 'guten morgen'
Step 2: Calculator: 30

Summary: Completed 2 steps successfully.
```

## Logging

Each level generates detailed interaction text logs with timestamps,user queries and bot responses

**Author:** Anughna Kandimalla 
