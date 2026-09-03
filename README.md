# AI Study Coach — Gemini Prompting Techniques

A small FastAPI + Gemini app that takes a student's exam situation and
generates a personalized study plan, letting you compare three prompting
techniques side by side:

1. **Zero-shot** — Gemini gets only the task instructions, no examples.
2. **Few-shot** — Gemini gets 2 worked examples first, then the new student.
3. **Structured reasoning** — Gemini is told to work through 7 explicit
   steps (identify weak topics → prioritize → consider time → recommend
   activities → build the plan → justify each choice) before answering.

## Project structure

```
ai-study-coach/
├── app.py            # FastAPI backend, /api/generate-plan endpoint
├── prompts.py         # The 3 prompt-builder functions (one per technique)
├── requirements.txt
├── static/
│   ├── index.html     # Form + results UI
│   ├── style.css
│   └── script.js
└── README.md
```

## Setup

```bash
cd ai-study-coach
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Get a free Gemini API key from https://aistudio.google.com/app/apikey,
then set it as an environment variable:

```bash
export GEMINI_API_KEY="your-key-here"     # Windows: set GEMINI_API_KEY=your-key-here
```

Run the app:

```bash
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

> If `GEMINI_API_KEY` isn't set, the app still runs — it will show you the
> exact prompt that *would* have been sent, with a message explaining the
> key is missing. This is useful for demoing the prompt engineering itself
> without an API key.

## How to use it for the assignment

1. Fill in a student's details (or use the sample: Ahmed, Python
   Programming, weak in "loops, functions, debugging", 5 days, 2 hrs/day,
   Beginner).
2. Generate the plan once with **each** of the three techniques.
3. Use "View prompt sent" to see and copy the exact prompt used for each
   technique — useful for your report/screenshots.
4. Compare the three responses for quality, consistency, and how well
   they follow the requested day-by-day format.

## Where each requirement lives

| Assignment requirement                          | Where it is                          |
|---------------------------------------------------|---------------------------------------|
| Zero-shot prompt                                   | `prompts.py → build_zero_shot_prompt` |
| Few-shot prompt (2–3 examples)                     | `prompts.py → build_few_shot_prompt`  |
| Structured reasoning prompt (7 steps)              | `prompts.py → build_structured_prompt`|
| Python + Gemini API application                    | `app.py`                              |
| User inputs (name, subject, weak topics, days, hours/day, skill level) | `static/index.html` form |
| Choice of technique (zero-shot / few-shot / structured) | Radio buttons in the form + `technique` field sent to `/api/generate-plan` |
| Gemini's response displayed in the app             | `static/script.js → showResult()`     |
