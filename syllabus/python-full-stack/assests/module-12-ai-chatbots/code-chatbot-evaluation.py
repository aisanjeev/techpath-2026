"""
Chatbot Evaluation Script -- TechPath Institute
================================================

This script demonstrates how to evaluate a RAG chatbot's quality using
RAGAS-style metrics. It measures:
  - Faithfulness: Does the answer stick to the context? (no hallucination)
  - Answer Relevancy: Does the answer actually address the question?
  - Context Precision: Were the retrieved documents useful?
  - Overall Score: A combined quality score

Instead of requiring the full RAGAS library, we use an LLM-as-judge approach
where Claude evaluates the chatbot's answers.

INSTALL INSTRUCTIONS:
    pip install anthropic tabulate

RUN:
    export ANTHROPIC_API_KEY=sk-ant-...    (Mac/Linux)
    set ANTHROPIC_API_KEY=sk-ant-...       (Windows)
    python code-chatbot-evaluation.py

The script will:
1. Define sample Q&A test cases
2. Simulate chatbot answers with retrieved context
3. Use Claude to score each answer on multiple metrics
4. Generate a detailed evaluation report
"""

# ============================================================
# IMPORTS
# ============================================================

import json
import time
from dataclasses import dataclass, field
from typing import Optional

import anthropic

# tabulate makes nice tables in the terminal
# Install: pip install tabulate
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False
    print("Note: Install 'tabulate' for nicer tables: pip install tabulate")


# ============================================================
# CONFIGURATION
# ============================================================

# Claude API client
client = anthropic.Anthropic()

# Model for evaluation (use a capable model for accurate judging)
EVAL_MODEL = "claude-sonnet-4-20250514"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TestCase:
    """
    A single test case for evaluating the chatbot.

    Fields:
        question: What the user asked
        context: What the RAG system retrieved from the knowledge base
        expected_answer: The ideal answer (ground truth)
        chatbot_answer: What the chatbot actually responded with
    """
    question: str
    context: str
    expected_answer: str
    chatbot_answer: str


@dataclass
class EvalResult:
    """
    Evaluation scores for a single test case.

    Each score is between 0.0 (worst) and 1.0 (best).
    """
    question: str
    faithfulness: float = 0.0
    relevancy: float = 0.0
    context_precision: float = 0.0
    overall: float = 0.0
    feedback: str = ""


@dataclass
class EvalReport:
    """
    Complete evaluation report across all test cases.
    """
    results: list[EvalResult] = field(default_factory=list)
    avg_faithfulness: float = 0.0
    avg_relevancy: float = 0.0
    avg_context_precision: float = 0.0
    avg_overall: float = 0.0
    total_cases: int = 0
    pass_count: int = 0
    fail_count: int = 0


# ============================================================
# SAMPLE TEST DATA -- TechPath Institute Context
# ============================================================
# These represent real conversations a student might have
# with the TechPath course FAQ chatbot.

SAMPLE_TEST_CASES = [
    # TEST 1: Direct factual question (should score high)
    TestCase(
        question="What is the fee for the Python Full Stack course?",
        context="TechPath Institute offers a Python Full Stack Developer course. The duration is 6 months. The fee is ₹49,999. EMI options are available starting at ₹8,333 per month for 6 months.",
        expected_answer="The fee for the Python Full Stack course at TechPath Institute is ₹49,999. EMI options are available starting at ₹8,333 per month.",
        chatbot_answer="The Python Full Stack course at TechPath Institute costs ₹49,999. You can also pay in EMIs of ₹8,333 per month for 6 months.",
    ),

    # TEST 2: Question where chatbot adds information not in context (hallucination)
    TestCase(
        question="Does TechPath provide hostel facility?",
        context="TechPath Institute is located in MP Nagar Zone-II, Bhopal, Madhya Pradesh. The campus is near the DB Mall and easily accessible by city bus routes 9 and 12. Free parking is available for two-wheeler vehicles.",
        expected_answer="I don't have information about hostel facilities. Please contact the TechPath office for details.",
        chatbot_answer="Yes, TechPath Institute has a fully furnished hostel with AC rooms, mess facility, and 24/7 security. The hostel fee is ₹5,000 per month.",
    ),

    # TEST 3: Placement-related question (should be accurate)
    TestCase(
        question="What is the placement record at TechPath?",
        context="TechPath placement statistics for 2025: 87% of eligible students placed within 3 months of course completion. Top recruiters: TCS (12 students), Infosys (8 students), startups (25 students). Highest package offered: ₹8.5 LPA for a Python Full Stack graduate placed at a Pune-based fintech startup.",
        expected_answer="TechPath has an 87% placement rate. Top recruiters include TCS, Infosys, and startups. The highest package was ₹8.5 LPA.",
        chatbot_answer="TechPath Institute has a strong placement record with 87% of students getting placed within 3 months. Companies like TCS, Infosys, and various startups hire from TechPath. The highest package offered was ₹8.5 LPA at a Pune-based fintech startup.",
    ),

    # TEST 4: Irrelevant answer (chatbot goes off-topic)
    TestCase(
        question="What batch timings are available?",
        context="TechPath Institute batch timings: Morning batch 10:00 AM to 1:00 PM, Afternoon batch 2:00 PM to 5:00 PM, Evening batch 6:00 PM to 8:00 PM (online only), Weekend batch Saturday-Sunday 10:00 AM to 4:00 PM. Students can switch batches with 2 days advance notice.",
        expected_answer="TechPath offers Morning (10 AM - 1 PM), Afternoon (2 PM - 5 PM), Evening (6 PM - 8 PM, online), and Weekend (Sat-Sun, 10 AM - 4 PM) batches.",
        chatbot_answer="Python is a great programming language created by Guido van Rossum. It is used by companies like Google, Netflix, and Instagram.",
    ),

    # TEST 5: Partially correct answer
    TestCase(
        question="What modules are covered in the Python Full Stack course?",
        context="The Python Full Stack course syllabus covers 18 modules: Python Core, Advanced Python, Python Libraries, Database Design, Git & GitHub, FastAPI, Django & DRF, Frontend (React), GenAI Fundamentals, LangChain, LangGraph, AI Chatbots, Docker, CI/CD, Cloud Deployment, Spec Kit, Capstone Project, and Career Launch.",
        expected_answer="The course has 18 modules covering Python, databases, web frameworks (FastAPI, Django), frontend (React), AI/ML (GenAI, LangChain, LangGraph, Chatbots), DevOps (Docker, CI/CD, Cloud), and a capstone project.",
        chatbot_answer="The Python Full Stack course covers Python basics, web development, and some AI topics. I think it has about 12 modules.",
    ),

    # TEST 6: Question about trainers
    TestCase(
        question="Who teaches the Python course at TechPath?",
        context="TechPath Institute trainers have 5+ years of industry experience. Lead Python trainer Vikram Malhotra previously worked at Wipro and has built production applications using FastAPI and Django. The AI/ML module is taught by Sneha Iyer who has published research papers on LLM applications.",
        expected_answer="Vikram Malhotra teaches Python (ex-Wipro, 5+ years experience). Sneha Iyer teaches the AI/ML module.",
        chatbot_answer="The lead Python trainer is Vikram Malhotra, who has over 5 years of industry experience and previously worked at Wipro. He specializes in FastAPI and Django. The AI/ML modules are taught by Sneha Iyer, a published researcher in LLM applications.",
    ),
]


# ============================================================
# EVALUATION FUNCTIONS
# ============================================================

def evaluate_faithfulness(test_case: TestCase) -> float:
    """
    Faithfulness measures whether the chatbot's answer is supported
    by the retrieved context. A faithful answer does not make up facts.

    Score:
        1.0 = Every claim in the answer is in the context
        0.5 = Some claims are in the context, some are not
        0.0 = The answer is completely made up (hallucination)
    """
    prompt = f"""You are an evaluation judge. Score the FAITHFULNESS of a chatbot answer.

Faithfulness means: every fact in the answer must be supported by the context.
If the answer includes information NOT in the context, it is unfaithful (hallucination).

CONTEXT (what the chatbot was given):
{test_case.context}

CHATBOT ANSWER (what the chatbot replied):
{test_case.chatbot_answer}

Score from 0.0 to 1.0:
- 1.0 = Every claim is supported by the context
- 0.7 = Most claims are supported, minor additions
- 0.5 = About half the claims are unsupported
- 0.3 = Most claims are not in the context
- 0.0 = The answer is entirely made up

Reply with ONLY a JSON object: {{"score": <number>, "reason": "<one sentence>"}}"""

    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        result = json.loads(response.content[0].text)
        return float(result["score"])
    except (json.JSONDecodeError, KeyError, ValueError):
        # If parsing fails, try to extract just a number
        text = response.content[0].text.strip()
        for word in text.split():
            try:
                score = float(word)
                if 0 <= score <= 1:
                    return score
            except ValueError:
                continue
        return 0.5  # default fallback


def evaluate_relevancy(test_case: TestCase) -> float:
    """
    Answer Relevancy measures whether the chatbot's answer actually
    addresses the user's question.

    Score:
        1.0 = The answer directly and completely addresses the question
        0.5 = The answer partially addresses the question
        0.0 = The answer is completely off-topic
    """
    prompt = f"""You are an evaluation judge. Score the RELEVANCY of a chatbot answer.

Relevancy means: does the answer actually address what the user asked?

USER QUESTION:
{test_case.question}

CHATBOT ANSWER:
{test_case.chatbot_answer}

Score from 0.0 to 1.0:
- 1.0 = Directly and completely answers the question
- 0.7 = Answers the question but misses some parts
- 0.5 = Partially relevant
- 0.3 = Loosely related but does not answer the question
- 0.0 = Completely off-topic or irrelevant

Reply with ONLY a JSON object: {{"score": <number>, "reason": "<one sentence>"}}"""

    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        result = json.loads(response.content[0].text)
        return float(result["score"])
    except (json.JSONDecodeError, KeyError, ValueError):
        text = response.content[0].text.strip()
        for word in text.split():
            try:
                score = float(word)
                if 0 <= score <= 1:
                    return score
            except ValueError:
                continue
        return 0.5


def evaluate_context_precision(test_case: TestCase) -> float:
    """
    Context Precision measures whether the retrieved context actually
    contains the information needed to answer the question.

    This tells you if your RAG retrieval is working well.

    Score:
        1.0 = The context has all the information needed
        0.5 = The context has some relevant information
        0.0 = The context is not relevant to the question at all
    """
    prompt = f"""You are an evaluation judge. Score the CONTEXT PRECISION.

Context Precision means: does the retrieved context contain the information
needed to answer the user's question?

USER QUESTION:
{test_case.question}

RETRIEVED CONTEXT:
{test_case.context}

EXPECTED ANSWER:
{test_case.expected_answer}

Score from 0.0 to 1.0:
- 1.0 = Context contains all needed information
- 0.7 = Context contains most needed information
- 0.5 = Context has some relevant information
- 0.3 = Context has little relevant information
- 0.0 = Context is completely irrelevant

Reply with ONLY a JSON object: {{"score": <number>, "reason": "<one sentence>"}}"""

    response = client.messages.create(
        model=EVAL_MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        result = json.loads(response.content[0].text)
        return float(result["score"])
    except (json.JSONDecodeError, KeyError, ValueError):
        text = response.content[0].text.strip()
        for word in text.split():
            try:
                score = float(word)
                if 0 <= score <= 1:
                    return score
            except ValueError:
                continue
        return 0.5


def evaluate_single_case(test_case: TestCase, case_number: int) -> EvalResult:
    """
    Run all three evaluations on a single test case and return the result.
    Adds a small delay between API calls to avoid rate limits.
    """
    print(f"\n  Evaluating Test Case {case_number}: {test_case.question[:50]}...")

    # Run each evaluation
    print(f"    Checking faithfulness...")
    faithfulness = evaluate_faithfulness(test_case)
    time.sleep(0.5)  # small delay to avoid rate limits

    print(f"    Checking relevancy...")
    relevancy = evaluate_relevancy(test_case)
    time.sleep(0.5)

    print(f"    Checking context precision...")
    context_precision = evaluate_context_precision(test_case)

    # Calculate overall score (weighted average)
    # Faithfulness is most important (40%), then relevancy (35%), then precision (25%)
    overall = (
        faithfulness * 0.40 +
        relevancy * 0.35 +
        context_precision * 0.25
    )

    # Generate feedback based on scores
    feedback_parts = []
    if faithfulness < 0.7:
        feedback_parts.append("Answer contains hallucinated information")
    if relevancy < 0.7:
        feedback_parts.append("Answer does not address the question well")
    if context_precision < 0.7:
        feedback_parts.append("Retrieved context was not relevant enough")
    if not feedback_parts:
        feedback_parts.append("Good quality answer")

    result = EvalResult(
        question=test_case.question,
        faithfulness=round(faithfulness, 2),
        relevancy=round(relevancy, 2),
        context_precision=round(context_precision, 2),
        overall=round(overall, 2),
        feedback="; ".join(feedback_parts),
    )

    # Print a quick summary for this case
    status = "PASS" if overall >= 0.7 else "FAIL"
    print(f"    Result: {status} (Overall: {overall:.2f})")

    return result


# ============================================================
# REPORT GENERATION
# ============================================================

def generate_report(results: list[EvalResult]) -> EvalReport:
    """
    Calculate averages across all test cases and generate the report.
    """
    total = len(results)
    if total == 0:
        return EvalReport()

    avg_faith = sum(r.faithfulness for r in results) / total
    avg_rel = sum(r.relevancy for r in results) / total
    avg_prec = sum(r.context_precision for r in results) / total
    avg_overall = sum(r.overall for r in results) / total

    pass_count = sum(1 for r in results if r.overall >= 0.7)

    return EvalReport(
        results=results,
        avg_faithfulness=round(avg_faith, 2),
        avg_relevancy=round(avg_rel, 2),
        avg_context_precision=round(avg_prec, 2),
        avg_overall=round(avg_overall, 2),
        total_cases=total,
        pass_count=pass_count,
        fail_count=total - pass_count,
    )


def print_report(report: EvalReport):
    """
    Print a formatted evaluation report to the terminal.
    """
    print("\n" + "=" * 70)
    print("  CHATBOT EVALUATION REPORT -- TechPath Institute FAQ Bot")
    print("=" * 70)

    # -- Per-case results table --
    print("\n--- Per-Question Results ---\n")

    if HAS_TABULATE:
        # Use tabulate for a nice table
        table_data = []
        for i, r in enumerate(report.results, 1):
            status = "PASS" if r.overall >= 0.7 else "FAIL"
            table_data.append([
                i,
                r.question[:40] + "..." if len(r.question) > 40 else r.question,
                f"{r.faithfulness:.2f}",
                f"{r.relevancy:.2f}",
                f"{r.context_precision:.2f}",
                f"{r.overall:.2f}",
                status,
            ])

        headers = ["#", "Question", "Faith.", "Relev.", "Ctx Prec.", "Overall", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        # Fallback: simple text format
        print(f"{'#':<3} {'Question':<42} {'Faith.':<8} {'Relev.':<8} {'Ctx.P':<8} {'Score':<8} {'Status'}")
        print("-" * 95)
        for i, r in enumerate(report.results, 1):
            status = "PASS" if r.overall >= 0.7 else "FAIL"
            q = r.question[:40] + "..." if len(r.question) > 40 else r.question
            print(f"{i:<3} {q:<42} {r.faithfulness:<8.2f} {r.relevancy:<8.2f} {r.context_precision:<8.2f} {r.overall:<8.2f} {status}")

    # -- Feedback for each case --
    print("\n--- Feedback ---\n")
    for i, r in enumerate(report.results, 1):
        print(f"  Q{i}: {r.feedback}")

    # -- Summary statistics --
    print("\n--- Summary ---\n")
    print(f"  Total test cases  : {report.total_cases}")
    print(f"  Passed (>= 0.70)  : {report.pass_count}")
    print(f"  Failed (< 0.70)   : {report.fail_count}")
    print(f"  Pass rate         : {report.pass_count / report.total_cases * 100:.0f}%")

    print(f"\n  Avg Faithfulness      : {report.avg_faithfulness:.2f}")
    print(f"  Avg Relevancy         : {report.avg_relevancy:.2f}")
    print(f"  Avg Context Precision : {report.avg_context_precision:.2f}")
    print(f"  Avg Overall Score     : {report.avg_overall:.2f}")

    # -- Quality verdict --
    print("\n--- Verdict ---\n")
    if report.avg_overall >= 0.85:
        print("  EXCELLENT -- The chatbot is production-ready.")
    elif report.avg_overall >= 0.70:
        print("  GOOD -- The chatbot works well but has room for improvement.")
    elif report.avg_overall >= 0.50:
        print("  NEEDS WORK -- The chatbot has significant quality issues.")
    else:
        print("  POOR -- The chatbot needs major rework before deployment.")

    # -- Recommendations --
    print("\n--- Recommendations ---\n")
    if report.avg_faithfulness < 0.7:
        print("  [!] Faithfulness is low. The chatbot is hallucinating.")
        print("      Fix: Add stronger instructions to stick to context only.")
        print("      Fix: Use a system prompt like 'Only answer from the given context.'")
    if report.avg_relevancy < 0.7:
        print("  [!] Relevancy is low. The chatbot gives off-topic answers.")
        print("      Fix: Improve the system prompt to stay on topic.")
        print("      Fix: Add intent detection to filter irrelevant queries.")
    if report.avg_context_precision < 0.7:
        print("  [!] Context Precision is low. The RAG retrieval is not finding relevant docs.")
        print("      Fix: Try smaller chunk sizes or better embeddings.")
        print("      Fix: Add more FAQ entries to the knowledge base.")
    if report.avg_overall >= 0.7:
        print("  [OK] Overall quality is acceptable. Monitor with regular eval runs.")

    print("\n" + "=" * 70)


# ============================================================
# MAIN -- Run the evaluation
# ============================================================

def main():
    """
    Main function: run all evaluations and print the report.
    """
    print("=" * 70)
    print("  TechPath Chatbot Evaluation")
    print("  Using RAGAS-style metrics with LLM-as-judge")
    print("=" * 70)
    print(f"\n  Model for evaluation: {EVAL_MODEL}")
    print(f"  Number of test cases: {len(SAMPLE_TEST_CASES)}")
    print(f"  Metrics: Faithfulness, Relevancy, Context Precision")
    print(f"\n  Running evaluations...\n")

    # Evaluate each test case
    results = []
    for i, test_case in enumerate(SAMPLE_TEST_CASES, 1):
        result = evaluate_single_case(test_case, i)
        results.append(result)
        time.sleep(1)  # delay between test cases to avoid rate limits

    # Generate and print the report
    report = generate_report(results)
    print_report(report)

    # Save report as JSON (optional, for tracking over time)
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": EVAL_MODEL,
        "summary": {
            "total_cases": report.total_cases,
            "pass_count": report.pass_count,
            "fail_count": report.fail_count,
            "avg_faithfulness": report.avg_faithfulness,
            "avg_relevancy": report.avg_relevancy,
            "avg_context_precision": report.avg_context_precision,
            "avg_overall": report.avg_overall,
        },
        "results": [
            {
                "question": r.question,
                "faithfulness": r.faithfulness,
                "relevancy": r.relevancy,
                "context_precision": r.context_precision,
                "overall": r.overall,
                "feedback": r.feedback,
            }
            for r in report.results
        ],
    }

    report_path = "eval_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print(f"\n  Report saved to: {report_path}")
    print(f"  Run this script regularly to track quality over time.\n")


if __name__ == "__main__":
    main()
