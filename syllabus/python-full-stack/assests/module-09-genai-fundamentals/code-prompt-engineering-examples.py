"""
Prompt Engineering Examples — Module 09 Code Snap

Install: pip install openai anthropic tiktoken
Set env: set OPENAI_API_KEY=sk-...
Run:     python code-prompt-engineering-examples.py

This file demonstrates all major prompting techniques using the OpenAI API.
Each function is a self-contained example you can run and modify.
All examples use TechPath Institute context with Indian names.
"""

import os
import json
from openai import OpenAI

# Initialize client (reads OPENAI_API_KEY from environment)
client = OpenAI()
MODEL = "gpt-4o-mini"  # Use mini for practice (cheaper), switch to gpt-4o for production


def call_llm(messages, temperature=0.7, max_tokens=500):
    """Helper: send messages to the LLM and return the response text"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


# ============================================================
# 1. ZERO-SHOT PROMPTING — No examples, just instructions
# ============================================================
def zero_shot_classification():
    """Classify student feedback without giving any examples"""
    reviews = [
        "The Python course at TechPath was absolutely brilliant! Trainer explained everything so clearly.",
        "Waste of money. The lab computers were always broken and the trainer was always late.",
        "The course content was okay. Some topics were good, some were boring.",
    ]

    print("=== ZERO-SHOT CLASSIFICATION ===\n")

    for review in reviews:
        result = call_llm(
            messages=[{
                "role": "user",
                "content": f"Classify this student review as positive, negative, or neutral. "
                           f"Reply with just the label.\n\nReview: \"{review}\"\n\nLabel:"
            }],
            temperature=0,  # Deterministic for classification
        )
        print(f"Review: {review[:60]}...")
        print(f"Label:  {result.strip()}\n")


# ============================================================
# 2. FEW-SHOT PROMPTING — Teach by example
# ============================================================
def few_shot_extraction():
    """Extract structured data by showing examples first"""
    print("=== FEW-SHOT EXTRACTION ===\n")

    prompt = """Extract student details from the text. Follow this format exactly.

Text: "Rahul Sharma from Bhopal joined Python Full Stack. His marks are 85."
Output: Name: Rahul Sharma | City: Bhopal | Course: Python Full Stack | Marks: 85

Text: "Priya Patel, Indore, enrolled in Data Science with 92 marks."
Output: Name: Priya Patel | City: Indore | Course: Data Science | Marks: 92

Text: "Ananya from Delhi got 78 in the Web Development program at TechPath."
Output: Name: Ananya | City: Delhi | Course: Web Development | Marks: 78

Text: "Vikram Joshi scored 65 marks in Python Full Stack. He lives in Pune."
Output:"""

    result = call_llm(
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    print(f"Extracted: {result.strip()}\n")


# ============================================================
# 3. CHAIN-OF-THOUGHT — Step-by-step reasoning
# ============================================================
def chain_of_thought_reasoning():
    """Make the model reason step by step for better accuracy"""
    print("=== CHAIN-OF-THOUGHT REASONING ===\n")

    prompt = """A student at TechPath Institute has the following marks:
- Python: 78/100
- Django: 85/100
- JavaScript: 42/100
- Database: 91/100

Rules:
1. Must score at least 40 in each subject to pass that subject
2. Must pass ALL subjects to get a certificate
3. Overall percentage = average of all subjects
4. Grades: A (80+), B (60-79), C (40-59), F (<40)

Question: Does this student get a certificate? What is their overall grade?

Think step by step before giving the final answer."""

    result = call_llm(
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=800,
    )
    print(result)
    print()


# ============================================================
# 4. STRUCTURED OUTPUT — Get JSON back
# ============================================================
def structured_json_output():
    """Force the model to return structured JSON"""
    print("=== STRUCTURED JSON OUTPUT ===\n")

    prompt = """Extract information from this paragraph and return ONLY valid JSON.

"TechPath Institute Bhopal is offering a new batch for Python Full Stack course
starting from August 2026. The course is 8 months long and costs Rs.45000.
The trainer is Mr. Sanjeev Kumar. Classes are Monday to Friday, 10 AM to 1 PM.
Maximum batch size is 30 students. Prerequisites: basic computer knowledge."

Return JSON with these fields:
{
    "institute": "",
    "city": "",
    "course_name": "",
    "start_date": "",
    "duration_months": 0,
    "fee_inr": 0,
    "trainer": "",
    "schedule": "",
    "batch_size": 0,
    "prerequisites": ""
}"""

    result = call_llm(
        messages=[
            {"role": "system", "content": "You are a JSON extraction assistant. Return ONLY valid JSON, no extra text."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    # Parse and pretty-print the JSON
    try:
        start = result.find('{')
        end = result.rfind('}') + 1
        parsed = json.loads(result[start:end])
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except (json.JSONDecodeError, ValueError):
        print("Failed to parse JSON. Raw output:")
        print(result)
    print()


# ============================================================
# 5. SYSTEM PROMPT — Setting personality and rules
# ============================================================
def system_prompt_demo():
    """Show how system prompts control model behavior"""
    print("=== SYSTEM PROMPT DEMO ===\n")

    # Same question, different system prompts
    question = "How do I learn Python?"

    personas = [
        {
            "name": "Strict Teacher",
            "prompt": "You are a strict, disciplined Python trainer at TechPath Institute, Bhopal. "
                      "You give direct, no-nonsense answers. Keep answers under 3 sentences. "
                      "Always mention practice and hard work."
        },
        {
            "name": "Friendly Mentor",
            "prompt": "You are a friendly, encouraging mentor at TechPath Institute. "
                      "You use simple language with lots of emojis. You always motivate students. "
                      "Give practical advice with examples."
        },
        {
            "name": "Technical Expert",
            "prompt": "You are a senior Python developer with 15 years of experience. "
                      "You give technically precise answers with code examples. "
                      "Always mention best practices and real-world usage."
        },
    ]

    for persona in personas:
        result = call_llm(
            messages=[
                {"role": "system", "content": persona["prompt"]},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        print(f"--- {persona['name']} ---")
        print(result.strip())
        print()


# ============================================================
# 6. TEMPERATURE COMPARISON — Same prompt, different temps
# ============================================================
def temperature_comparison():
    """Show how temperature affects output creativity"""
    print("=== TEMPERATURE COMPARISON ===\n")

    prompt = "Write a one-sentence motivational quote for Python students at TechPath Institute."

    temperatures = [0.0, 0.7, 1.5]

    for temp in temperatures:
        results = []
        for _ in range(3):  # Run 3 times to show variation
            result = call_llm(
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=100,
            )
            results.append(result.strip())

        print(f"Temperature = {temp}:")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r}")
        print()


# ============================================================
# 7. MULTI-TURN CONVERSATION — Maintaining context
# ============================================================
def multi_turn_conversation():
    """Show how to maintain conversation history"""
    print("=== MULTI-TURN CONVERSATION ===\n")

    conversation = [
        {"role": "system", "content": "You are a Python tutor at TechPath Institute. Keep answers short (2-3 sentences)."},
    ]

    user_messages = [
        "What is a dictionary in Python?",
        "Give me an example with student data",
        "How do I loop through it?",
    ]

    for user_msg in user_messages:
        print(f"Student: {user_msg}")

        conversation.append({"role": "user", "content": user_msg})

        response = call_llm(messages=conversation, max_tokens=200)

        conversation.append({"role": "assistant", "content": response})

        print(f"Tutor: {response.strip()}\n")


# ============================================================
# 8. PROMPT TEMPLATE — Reusable prompt with variables
# ============================================================
def prompt_template_demo():
    """Create reusable prompt templates for common tasks"""
    print("=== PROMPT TEMPLATE ===\n")

    # Template for generating assignment questions
    template = """You are a trainer at TechPath Institute, Bhopal.

Generate {count} practice questions for the topic: {topic}
Difficulty level: {difficulty}
Target audience: {audience}

Rules:
- Questions should be practical, not theoretical
- Include code snippets where relevant
- Use Indian context (names, cities, currency in Rs.)
- Format as numbered list

Questions:"""

    # Fill the template
    prompt = template.format(
        count=3,
        topic="Python Lists and Dictionaries",
        difficulty="Beginner",
        audience="First-year students learning Python at TechPath Institute",
    )

    result = call_llm(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600,
    )

    print(result.strip())
    print()


# ============================================================
# 9. TOKEN COUNTING — Understanding costs
# ============================================================
def token_counting_demo():
    """Count tokens and estimate API costs"""
    print("=== TOKEN COUNTING ===\n")

    try:
        import tiktoken
    except ImportError:
        print("Install tiktoken: pip install tiktoken")
        return

    encoder = tiktoken.encoding_for_model("gpt-4o")

    texts = [
        "Hello",
        "TechPath Institute, Bhopal",
        "Python is a programming language created by Guido van Rossum.",
        "Write a function that takes a list of student names and marks, "
        "and returns the topper from TechPath Institute.",
    ]

    print(f"{'Text':<60} {'Tokens':>8}")
    print("-" * 70)

    for text in texts:
        tokens = encoder.encode(text)
        print(f"{text[:58]:<60} {len(tokens):>8}")

    # Cost estimation
    print("\n--- Cost Estimation (GPT-4o-mini) ---")
    input_tokens = 500
    output_tokens = 300
    input_cost = (input_tokens / 1_000_000) * 0.15   # $0.15 per 1M input tokens
    output_cost = (output_tokens / 1_000_000) * 0.60  # $0.60 per 1M output tokens
    total_usd = input_cost + output_cost
    total_inr = total_usd * 84

    print(f"Input:  {input_tokens} tokens → ${input_cost:.6f}")
    print(f"Output: {output_tokens} tokens → ${output_cost:.6f}")
    print(f"Total:  ${total_usd:.6f} (approx Rs.{total_inr:.4f})")
    print(f"\nFor 1000 such calls: ${total_usd * 1000:.2f} (approx Rs.{total_inr * 1000:.2f})")
    print()


# ============================================================
# MAIN — Run all examples
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PROMPT ENGINEERING EXAMPLES — TechPath Institute")
    print("=" * 60)
    print()

    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set!")
        print("Set it with: set OPENAI_API_KEY=sk-your-key-here")
        print()
        print("Running token counting demo (no API needed)...\n")
        token_counting_demo()
    else:
        # Run all demos
        zero_shot_classification()
        few_shot_extraction()
        chain_of_thought_reasoning()
        structured_json_output()
        system_prompt_demo()
        temperature_comparison()
        multi_turn_conversation()
        prompt_template_demo()
        token_counting_demo()

    print("Done! Modify the prompts above and experiment.")
