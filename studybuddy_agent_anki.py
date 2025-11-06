"""
StudyBuddy AI Agent – With Anki Export Feature
Author: Aaryaveer Yadav | Reg No: 23BAI10323

NOTE: Replace "YOUR_API_KEY_HERE" with your actual OpenAI API key.
"""

import os
import csv
import json
from openai import OpenAI

# Replace with your key locally; keep it secret.
API_KEY = ""

client = OpenAI(api_key=API_KEY)

# Prompts for 4-layer architecture
PROMPT_INPUT_UNDERSTANDING = """
You are the Input Understanding module for StudyBuddy.
Extract topic, intent (want_quiz/want_summary/want_flashcards), difficulty, length, and notes.
Output JSON: {"topic": "...", "intent": "...", "difficulty": "...", "length": 0, "notes": "...", "clarifying_question": null}
"""

PROMPT_STATE_TRACKER = """
Maintain a short session context JSON with topic, intent, difficulty, and recent_items.
"""

PROMPT_TASK_PLANNER = """
Based on Input and State JSON, plan a sequence of actions: e.g. ["extract_facts", "generate_quiz", "format_output"].
Return JSON list of steps.
"""

PROMPT_OUTPUT_GENERATOR = """
Generate markdown output based on plan.
If intent = "want_quiz", produce numbered questions and answers.
If intent = "want_flashcards", produce Q/A pairs suitable for export to CSV.
Tone: encouraging, concise. Limit to 300 words.
"""

def ask_llm(prompt, user_input=None):
    messages = [{"role": "system", "content": prompt}]
    if user_input:
        messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

def export_to_anki(data):
    """Exports Q/A pairs to anki_export.csv."""
    filename = "anki_export.csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Question", "Answer"])
        for q, a in data:
            writer.writerow([q.strip(), a.strip()])
    print(f"✅ Exported to {filename} successfully.")

def parse_quiz_to_csv(output_text):
    """Parses markdown quiz/flashcard text into Q/A pairs."""
    lines = output_text.splitlines()
    qa_pairs = []
    current_q = None
    for line in lines:
        if line.strip().startswith(("Q:", "1.", "2.", "3.")):
            current_q = line.split(":", 1)[-1].strip()
        elif line.strip().startswith(("A:", "Answer:", "Ans:")) and current_q:
            ans = line.split(":", 1)[-1].strip()
            qa_pairs.append((current_q, ans))
            current_q = None
    return qa_pairs

def run_studybuddy(user_text, session_state):
    input_json_raw = ask_llm(PROMPT_INPUT_UNDERSTANDING, user_text)
    try:
        input_json = json.loads(input_json_raw)
    except json.JSONDecodeError:
        input_json = {"topic": user_text, "intent": "want_quiz", "difficulty": "medium"}

    plan_raw = ask_llm(PROMPT_TASK_PLANNER, json.dumps(input_json))
    output_text = ask_llm(PROMPT_OUTPUT_GENERATOR, json.dumps({"plan": plan_raw, "input": input_json}))

    # Export flashcards or quizzes to CSV for Anki
    qa_data = parse_quiz_to_csv(output_text)
    if qa_data:
        export_to_anki(qa_data)

    return output_text

if __name__ == "__main__":
    session_state = {"last_topic": "", "last_intent": "", "recent_items": []}
    user_text = input("Enter your request (e.g., '5 flashcards on TCP handshake'): ")
    output = run_studybuddy(user_text, session_state)
    print("\n==== StudyBuddy Output ====\n")
    print(output)
    print("\nIf Q/A pairs were found, they are saved in 'anki_export.csv' for import into Anki or Quizlet.")
