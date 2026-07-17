#!/usr/bin/env python
"""Seed a complete demo training program with one sample of every asset type.

Creates:
  - 1 program  : Python Programming Fundamentals
  - 4 modules  : Getting Started / Learning Resources / Links / Assessments
  - 18 assets  : one per enabled type (markdown → lab)

Idempotent: re-running skips anything that already exists by slug/title.

    poetry run python scripts/seed_training_demo.py
    poetry run python scripts/seed_training_demo.py --clear   # drop first
"""
import argparse
import asyncio
import json
import logging
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.core.config import settings  # noqa: E402
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.models.media import MediaFile  # noqa: E402
from app.models.training import LectureAsset, TrainingModule, TrainingModuleAsset, TrainingProgram  # noqa: E402
from app.services.secrets_loader import load_secrets_from_keyvault  # noqa: E402

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("seed_training_demo")

# ---------------------------------------------------------------------------
# Asset payload definitions — one entry per enabled AssetType
# ---------------------------------------------------------------------------

INLINE_TEXT_ASSETS = [
    {
        "asset_type": "markdown",
        "title": "What is Python?",
        "body": """# What is Python?

Python is a high-level, general-purpose programming language known for its clean,
readable syntax that emphasises code readability.

## Key Features

- **Easy to learn** — English-like syntax, minimal boilerplate
- **Interpreted** — no compile step; great for rapid prototyping
- **Batteries included** — rich standard library covering everything from HTTP to JSON
- **Cross-platform** — runs on Windows, macOS, Linux without changes

## Hello World

```python
print("Hello, World!")
```

## Why Python for Data?

Python dominates data science, ML, and automation because of libraries like
`pandas`, `numpy`, `scikit-learn`, and `torch`.
""",
    },
    {
        "asset_type": "notes",
        "title": "Class Notes: Day 1",
        "body": """# Day 1 — Introduction & Setup

## Attendance
- Batch: Python Fundamentals – July
- Trainer: Sanjeev
- Date: Week 1, Day 1

## Topics Covered
1. What is programming?
2. Why Python?
3. Installing Python 3.12
4. Running your first script
5. Using the REPL

## Key Takeaways
- Python files end in `.py`
- `python` runs scripts; `python -i` opens an interactive shell
- Indentation is **syntax**, not style — 4 spaces is the community standard

## Questions Raised
- Q: Can Python run on a Raspberry Pi? → Yes, officially supported
- Q: Does indentation have to be spaces? → Spaces are preferred; tabs cause issues when mixed

## Homework
- Install Python 3.12 from python.org
- Run `print("I did it!")` in the REPL
""",
    },
    {
        "asset_type": "cheat_sheet",
        "title": "Python Quick Reference",
        "body": """# Python Quick Reference

## Data Types
| Type    | Example           | Notes                    |
|---------|-------------------|--------------------------|
| int     | `42`              | Unlimited precision      |
| float   | `3.14`            | IEEE 754 double          |
| str     | `"hello"`         | Immutable, Unicode       |
| list    | `[1, 2, 3]`       | Mutable, ordered         |
| tuple   | `(1, 2, 3)`       | Immutable, ordered       |
| dict    | `{"a": 1}`        | Key → value, ordered 3.7+|
| set     | `{1, 2, 3}`       | Unique, unordered        |
| bool    | `True / False`    | Subclass of int          |

## Control Flow
```python
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")
```

## Loops
```python
for item in iterable:       # for-each
    ...

while condition:            # while
    ...

[x**2 for x in range(10)]  # list comprehension
```

## Functions
```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"
```

## String Formatting
```python
f"Hello, {name}!"          # f-string (preferred)
"Hello, {}".format(name)   # .format()
"%s" % name                # %-style (legacy)
```

## Common Built-ins
`len()` `range()` `enumerate()` `zip()` `sorted()` `reversed()`
`map()` `filter()` `any()` `all()` `sum()` `min()` `max()`
""",
    },
    {
        "asset_type": "code_snippet",
        "title": "Hello World & Basic I/O",
        "body": """# language: python
# Basic Python — print, variables, user input

# 1. Hello World
print("Hello, World!")

# 2. Variables and types
name = "Python"
version = 3.12
is_awesome = True

print(f"Language: {name}, Version: {version}, Awesome: {is_awesome}")

# 3. User input
user_name = input("What is your name? ")
print(f"Welcome, {user_name}!")

# 4. Simple arithmetic
a, b = 10, 3
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b:.2f}")   # float division
print(f"{a} // {b} = {a // b}")     # integer division
print(f"{a} % {b} = {a % b}")       # modulo
print(f"{a} ** {b} = {a ** b}")     # power

# 5. String operations
sentence = "the quick brown fox"
print(sentence.upper())
print(sentence.title())
print(sentence.split())
print(" ".join(sentence.split()[::-1]))  # reverse words
""",
    },
]

PLACEHOLDER_FILES = [
    {
        "asset_type": "pdf",
        "title": "Python Course Syllabus",
        "filename": "python-syllabus.pdf",
        "content_type": "application/pdf",
        "ext": ".pdf",
        "size": 245_000,
    },
    {
        "asset_type": "ppt",
        "title": "Introduction to Python — Slides",
        "filename": "intro-slides.pptx",
        "content_type": (
            "application/vnd.openxmlformats-officedocument"
            ".presentationml.presentation"
        ),
        "ext": ".pptx",
        "size": 1_800_000,
    },
    {
        "asset_type": "video",
        "title": "Python Setup Tutorial (Screenshare Recording)",
        "filename": "setup-tutorial.mp4",
        "content_type": "video/mp4",
        "ext": ".mp4",
        "size": 87_000_000,
    },
    {
        "asset_type": "notebook",
        "title": "Day 1 Practice Exercises",
        "filename": "day1-exercises.ipynb",
        "content_type": "application/x-ipynb+json",
        "ext": ".ipynb",
        "size": 42_000,
    },
    {
        "asset_type": "zip",
        "title": "Starter Code Package",
        "filename": "starter-code.zip",
        "content_type": "application/zip",
        "ext": ".zip",
        "size": 350_000,
    },
    {
        "asset_type": "excel",
        "title": "Batch Progress Tracker",
        "filename": "progress-tracker.xlsx",
        "content_type": (
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        ),
        "ext": ".xlsx",
        "size": 28_000,
    },
    {
        "asset_type": "csv",
        "title": "Sample Sales Dataset",
        "filename": "sales-data.csv",
        "content_type": "text/csv",
        "ext": ".csv",
        "size": 15_000,
    },
    {
        "asset_type": "terminal_recording",
        "title": "Live Coding Demo — List Comprehensions",
        "filename": "list-comprehension-demo.cast",
        "content_type": "application/x-asciicast",
        "ext": ".cast",
        "size": 8_200,
    },
]

LINK_ASSETS = [
    {
        "asset_type": "external_url",
        "title": "Python Official Documentation",
        "external_url": "https://docs.python.org/3/",
    },
    {
        "asset_type": "github_repo",
        "title": "Course Code Repository",
        "external_url": "https://github.com/techpath-biz/python-fundamentals",
    },
    {
        "asset_type": "youtube",
        "title": "Python in 100 Seconds",
        "external_url": "https://www.youtube.com/watch?v=x7X9w_GIm1s",
    },
]

STRUCTURED_ASSETS = [
    {
        "asset_type": "quiz",
        "title": "Python Basics — Check Yourself",
        "config_json": json.dumps({
            "questions": [
                {
                    "question": "Which keyword defines a function in Python?",
                    "options": ["func", "def", "function", "define"],
                    "correct_index": 1,
                },
                {
                    "question": "What does `len([1, 2, 3])` return?",
                    "options": ["2", "3", "4", "1"],
                    "correct_index": 1,
                },
                {
                    "question": "Which of these creates an empty dictionary?",
                    "options": ["[]", "()", "{}", "set()"],
                    "correct_index": 2,
                },
                {
                    "question": "What is the output of `print(10 // 3)`?",
                    "options": ["3.33", "3", "4", "1"],
                    "correct_index": 1,
                },
                {
                    "question": "Python list indices start at:",
                    "options": ["1", "0", "-1", "None of the above"],
                    "correct_index": 1,
                },
            ]
        }),
    },
    {
        "asset_type": "assignment",
        "title": "Build a Command-Line Calculator",
        "config_json": json.dumps({
            "instructions": (
                "Build a command-line calculator that reads two numbers and an operator "
                "(+, -, *, /) from the user and prints the result.\n\n"
                "## Requirements\n"
                "1. Accept two float inputs from the user\n"
                "2. Accept an operator: `+`, `-`, `*`, `/`\n"
                "3. Print the result rounded to 2 decimal places\n"
                "4. Handle division by zero gracefully with an error message\n"
                "5. Keep asking for input until the user types `quit`\n\n"
                "## Example\n"
                "```\n"
                "Enter first number: 10\n"
                "Operator (+/-/*/÷): /\n"
                "Enter second number: 3\n"
                "Result: 3.33\n"
                "```\n\n"
                "## Submission\n"
                "Submit a single `calculator.py` file."
            ),
            "due_in_days": 3,
            "max_score": 10,
        }),
    },
    {
        "asset_type": "lab",
        "title": "Set Up Your Python Development Environment",
        "config_json": json.dumps({
            "objective": (
                "By the end of this lab you will have Python 3.12, pip, and VS Code "
                "installed and will have run your first Python script."
            ),
            "steps": [
                {
                    "title": "Install Python 3.12",
                    "instructions": (
                        "Download the installer from https://www.python.org/downloads/.\n"
                        "On Windows: check **Add Python to PATH** before clicking Install.\n"
                        "Verify: open a terminal and run `python --version`."
                    ),
                    "verify_command": "python --version",
                    "expected_output": "Python 3.12",
                },
                {
                    "title": "Upgrade pip",
                    "instructions": "Run: `python -m pip install --upgrade pip`",
                    "verify_command": "pip --version",
                    "expected_output": "pip 24",
                },
                {
                    "title": "Install VS Code",
                    "instructions": (
                        "Download from https://code.visualstudio.com/.\n"
                        "Install the **Python** extension by Microsoft."
                    ),
                },
                {
                    "title": "Create and run your first script",
                    "instructions": (
                        "Create a file called `hello.py` containing:\n"
                        "```python\nprint('Hello, TechPath!')\n```\n"
                        "Run it: `python hello.py`"
                    ),
                    "verify_command": "python hello.py",
                    "expected_output": "Hello, TechPath!",
                },
                {
                    "title": "Install course dependencies",
                    "instructions": (
                        "Create `requirements.txt` with:\n"
                        "```\nrequests\npandas\njupyter\n```\n"
                        "Install: `pip install -r requirements.txt`"
                    ),
                },
            ],
            "estimated_minutes": 30,
        }),
    },
]

# Modules and which asset types belong in each
MODULE_PLAN = [
    {
        "title": "Getting Started",
        "slug": "getting-started",
        "description": "Foundations: what Python is, how to read code, and your first lines.",
        "display_order": 1,
        "estimated_minutes": 60,
        "asset_types": ["markdown", "notes", "cheat_sheet", "code_snippet"],
    },
    {
        "title": "Learning Resources",
        "slug": "learning-resources",
        "description": "Slides, recordings, exercises, and datasets for offline study.",
        "display_order": 2,
        "estimated_minutes": 45,
        "asset_types": ["pdf", "ppt", "video", "notebook", "zip", "excel", "csv", "terminal_recording"],
    },
    {
        "title": "Reference & Further Reading",
        "slug": "reference-links",
        "description": "Curated links: docs, source code, video extras.",
        "display_order": 3,
        "estimated_minutes": 20,
        "asset_types": ["external_url", "github_repo", "youtube"],
    },
    {
        "title": "Assessments",
        "slug": "assessments",
        "description": "Knowledge check, take-home assignment, and hands-on lab.",
        "display_order": 4,
        "estimated_minutes": 90,
        "asset_types": ["quiz", "assignment", "lab"],
    },
]


async def clear_demo(db) -> None:
    """Remove the demo program and all assets seeded by this script."""
    result = await db.execute(
        select(TrainingProgram).where(TrainingProgram.slug == "python-programming-fundamentals")
    )
    prog = result.scalar_one_or_none()
    if prog:
        # cascade deletes modules → module_assets; assets deleted separately
        await db.delete(prog)
        logger.info("Deleted demo program and its modules")

    # Delete assets by title prefix used in this seed
    seed_titles = (
        [a["title"] for a in INLINE_TEXT_ASSETS]
        + [a["title"] for a in PLACEHOLDER_FILES]
        + [a["title"] for a in LINK_ASSETS]
        + [a["title"] for a in STRUCTURED_ASSETS]
    )
    assets = (await db.execute(
        select(LectureAsset).where(LectureAsset.title.in_(seed_titles))
    )).scalars().all()
    for asset in assets:
        await db.delete(asset)
    logger.info("Deleted %d demo assets", len(assets))
    await db.flush()


async def _find_or_create_asset(db, asset_type: str, title: str, **payload) -> tuple[LectureAsset, bool]:
    existing = (await db.execute(
        select(LectureAsset).where(LectureAsset.title == title, LectureAsset.asset_type == asset_type)
    )).scalar_one_or_none()
    if existing:
        return existing, False
    obj = LectureAsset(
        public_id=str(uuid.uuid4()),
        asset_type=asset_type,
        title=title,
        status="published",
        is_active=True,
        **payload,
    )
    db.add(obj)
    await db.flush()
    return obj, True


async def _placeholder_media_file(db, *, filename: str, content_type: str, size: int) -> MediaFile:
    """Create a stub MediaFile row (no real bytes — seed only)."""
    stub_hash = uuid.uuid5(uuid.NAMESPACE_URL, filename).hex
    existing = (await db.execute(
        select(MediaFile).where(MediaFile.file_hash == stub_hash)
    )).scalar_one_or_none()
    if existing:
        return existing
    mf = MediaFile(
        filename=filename,
        stored_path=f"seed/placeholder/{filename}",
        file_hash=stub_hash,
        content_type=content_type,
        size=size,
    )
    db.add(mf)
    await db.flush()
    return mf


async def main(clear: bool) -> int:
    if settings.has_keyvault_config:
        await load_secrets_from_keyvault(update_db=False)

    async with AsyncSessionLocal() as db:
        try:
            if clear:
                await clear_demo(db)

            # ------------------------------------------------------------------
            # 1. Program
            # ------------------------------------------------------------------
            existing_prog = (await db.execute(
                select(TrainingProgram).where(
                    TrainingProgram.slug == "python-programming-fundamentals"
                )
            )).scalar_one_or_none()

            if existing_prog:
                logger.info("Program already exists (id=%s) — skipping create", existing_prog.id)
                program = existing_prog
            else:
                program = TrainingProgram(
                    title="Python Programming Fundamentals",
                    slug="python-programming-fundamentals",
                    summary="From zero to confident: Python syntax, data structures, and real exercises.",
                    description=(
                        "A structured 4-week program covering core Python from scratch. "
                        "Combines live sessions, self-study resources, and hands-on labs "
                        "to give students practical confidence writing Python code."
                    ),
                    delivery_mode="hybrid",
                    level="beginner",
                    duration="4 weeks",
                    status="published",
                    display_order=1,
                    is_active=True,
                    tags_json=json.dumps(["python", "programming", "beginner", "fundamentals"]),
                )
                db.add(program)
                await db.flush()
                logger.info("Created program: %s (id=%s)", program.title, program.id)

            # ------------------------------------------------------------------
            # 2. Assets — build a lookup {asset_type: LectureAsset}
            # ------------------------------------------------------------------
            asset_map: dict[str, LectureAsset] = {}
            created_count = 0

            # Inline text
            for spec in INLINE_TEXT_ASSETS:
                asset, created = await _find_or_create_asset(
                    db, spec["asset_type"], spec["title"], body=spec["body"]
                )
                asset_map[spec["asset_type"]] = asset
                created_count += int(created)
                logger.info(
                    "%s asset '%s' (id=%s)",
                    "Created" if created else "Reused",
                    asset.title,
                    asset.id,
                )

            # File placeholders
            for spec in PLACEHOLDER_FILES:
                mf = await _placeholder_media_file(
                    db,
                    filename=spec["filename"],
                    content_type=spec["content_type"],
                    size=spec["size"],
                )
                asset, created = await _find_or_create_asset(
                    db, spec["asset_type"], spec["title"], media_file_id=mf.id
                )
                asset_map[spec["asset_type"]] = asset
                created_count += int(created)
                logger.info(
                    "%s asset '%s' (id=%s)",
                    "Created" if created else "Reused",
                    asset.title,
                    asset.id,
                )

            # Links
            for spec in LINK_ASSETS:
                asset, created = await _find_or_create_asset(
                    db, spec["asset_type"], spec["title"], external_url=spec["external_url"]
                )
                asset_map[spec["asset_type"]] = asset
                created_count += int(created)
                logger.info(
                    "%s asset '%s' (id=%s)",
                    "Created" if created else "Reused",
                    asset.title,
                    asset.id,
                )

            # Structured
            for spec in STRUCTURED_ASSETS:
                asset, created = await _find_or_create_asset(
                    db, spec["asset_type"], spec["title"], config_json=spec["config_json"]
                )
                asset_map[spec["asset_type"]] = asset
                created_count += int(created)
                logger.info(
                    "%s asset '%s' (id=%s)",
                    "Created" if created else "Reused",
                    asset.title,
                    asset.id,
                )

            logger.info("Assets done: %d created, %d reused", created_count, 18 - created_count)

            # ------------------------------------------------------------------
            # 3. Modules + placements
            # ------------------------------------------------------------------
            for mod_spec in MODULE_PLAN:
                # Find or create module
                existing_mod = (await db.execute(
                    select(TrainingModule).where(
                        TrainingModule.program_id == program.id,
                        TrainingModule.slug == mod_spec["slug"],
                    )
                )).scalar_one_or_none()

                if existing_mod:
                    module = existing_mod
                    logger.info("Module '%s' already exists — skipping", module.title)
                else:
                    module = TrainingModule(
                        program_id=program.id,
                        title=mod_spec["title"],
                        slug=mod_spec["slug"],
                        description=mod_spec["description"],
                        display_order=mod_spec["display_order"],
                        estimated_minutes=mod_spec["estimated_minutes"],
                        status="published",
                    )
                    db.add(module)
                    await db.flush()
                    logger.info("Created module: %s (id=%s)", module.title, module.id)

                # Attach assets that belong here
                for order, atype in enumerate(mod_spec["asset_types"], start=1):
                    if atype not in asset_map:
                        continue
                    asset = asset_map[atype]
                    # Check if already placed
                    already = (await db.execute(
                        select(TrainingModuleAsset).where(
                            TrainingModuleAsset.module_id == module.id,
                            TrainingModuleAsset.asset_id == asset.id,
                        )
                    )).scalar_one_or_none()
                    if not already:
                        db.add(TrainingModuleAsset(
                            module_id=module.id,
                            asset_id=asset.id,
                            display_order=order,
                            is_required=True,
                        ))
                        logger.info("  Placed: %s → %s", module.title, asset.title)

            await db.flush()
            await db.commit()

            logger.info("")
            logger.info("=" * 60)
            logger.info("  Demo seed complete")
            logger.info("  Program : Python Programming Fundamentals")
            logger.info("  Modules : %d", len(MODULE_PLAN))
            logger.info("  Assets  : 18 (one per type)")
            logger.info("=" * 60)
            return 0

        except Exception:
            await db.rollback()
            logger.exception("Seed failed — rolled back")
            return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed demo training data")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete the demo program and assets before re-seeding",
    )
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.clear)))
