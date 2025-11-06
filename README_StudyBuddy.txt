📘 StudyBuddy — AI Agent Assignment
Author: Aaryaveer Yadav | Reg No: 23BAI10323

--------------------------------------
🧠 PURPOSE
--------------------------------------
StudyBuddy is an AI-powered revision assistant designed using the 4-layer agent model.
It helps students turn topics or notes into short quizzes, summaries, or flashcards.

--------------------------------------
⚙️ SETUP INSTRUCTIONS
--------------------------------------
1️⃣ Install dependencies:
    pip install openai

2️⃣ Get your API key:
    Go to https://platform.openai.com/api-keys
    Create a new secret key and copy it.

3️⃣ Paste your key into the Python file:
    Find the line:
        API_KEY = "YOUR_API_KEY_HERE"
    Replace the placeholder text with your real key (keep the quotes).

4️⃣ Run the agent:
    python studybuddy_agent_anki.py

--------------------------------------
📤 USING THE ANKI EXPORT FEATURE
--------------------------------------
After running a quiz or flashcard generation request, the agent automatically saves
a file called 'anki_export.csv' in the same directory.

Format:
Question,Answer

You can import this file directly into Anki or Quizlet.

--------------------------------------
💡 COMMON ERRORS
--------------------------------------
❌ RateLimitError or 'insufficient_quota':
    - You've used all your API credits.
    - Fix: Go to https://platform.openai.com/account/billing and add a payment method,
      or wait for your free-tier quota to reset.

❌ invalid_api_key:
    - The key is wrong or revoked. Create a new one at https://platform.openai.com/api-keys

--------------------------------------
✅ TIPS
--------------------------------------
- Keep responses short: "Give me a 5-question easy quiz on TCP."
- Use follow-ups like "make harder" or "convert to flashcards."
- Never share your API key publicly.
