# Module 02: Advanced Python — Assignment

## Task 1: Institute Management System with OOP (Beginner)

**Objective:** Build a class-based system to manage TechPath Institute operations.

**Requirements:**
1. Create the following classes with proper inheritance:
   - `Person` (base class): name, age, city, phone
   - `Student(Person)`: course, fee, marks list, enrollment_date
   - `Trainer(Person)`: subject, experience_years, salary
   - `Admin(Person)`: department, access_level
2. Each class should have:
   - `__init__`, `__str__`, and `__repr__` methods
   - At least one `@property` (e.g., `average_marks`, `grade`, `monthly_salary`)
   - A `to_dict()` method that returns all attributes as a dictionary
3. Create a `Classroom` class that:
   - Holds a list of students and a trainer
   - Implements `__len__`, `__contains__`, `__getitem__`, `__iter__`
   - Has methods: `add_student()`, `remove_student()`, `get_topper()`, `get_stats()`
4. Create at least 5 students, 2 trainers, and 1 classroom to demonstrate everything

**Deliverables:**
- A single file `institute_system.py`
- The program should print a formatted report when run

---

## Task 2: Smart Logger with Decorators (Intermediate)

**Objective:** Build a decorator library and use it to enhance functions.

**Requirements:**
1. Create these decorators:
   - `@timer` — Logs execution time
   - `@logger` — Logs function name, arguments, and return value
   - `@retry(max_attempts=3, delay=1)` — Retries on exception (decorator with arguments)
   - `@validate_types(**expected_types)` — Validates argument types (e.g., `@validate_types(name=str, age=int)`)
   - `@cache` — Caches results for same arguments (memoization)
2. Use `functools.wraps` in all decorators to preserve function metadata
3. Demonstrate stacking multiple decorators on a single function
4. Write at least 3 functions using these decorators:
   - A fee calculator (use `@timer` + `@validate_types`)
   - A data fetcher (use `@retry` + `@logger`)
   - A Fibonacci function (use `@cache` + `@timer`)
5. Show that `@cache` makes Fibonacci dramatically faster

**Deliverables:**
- `decorators.py` — The decorator library
- `demo_decorators.py` — Demo script showing all decorators in action

---

## Task 3: Async Student Data Pipeline (Intermediate)

**Objective:** Build an async data pipeline that processes student records concurrently.

**Requirements:**
1. Create an async function `fetch_student(student_id)` that simulates an API call with `asyncio.sleep(random_delay)`
2. Create an async function `process_batch(student_ids)` that fetches multiple students concurrently using `asyncio.gather()`
3. Implement a generator `student_id_generator(prefix, count)` that yields student IDs lazily
4. Measure and compare:
   - Sequential processing time (one student at a time)
   - Concurrent processing time (all at once with `gather`)
   - Batch processing time (groups of 5 with `gather`)
5. Use `asyncio.Semaphore` to limit concurrency to 5 simultaneous requests
6. Handle timeouts using `asyncio.wait_for()`
7. Print a summary showing the time savings from concurrency

**Deliverables:**
- `async_pipeline.py` — The complete async pipeline
- The program should print timing comparisons when run

---

## Task 4: Tested Student Analytics Library (Advanced)

**Objective:** Build a reusable analytics library with full test coverage using pytest.

**Requirements:**
1. Create `analytics.py` with these functions/classes:
   - `StudentAnalytics` class with methods:
     - `add_student(name, city, course, fee, marks)` — Add a student record
     - `get_topper()` → Student with highest average marks
     - `get_city_stats()` → Dict of {city: count, average_marks, total_fee}
     - `get_course_stats()` → Dict of {course: count, pass_rate, average_fee}
     - `get_grade_distribution()` → Dict of {grade: count}
     - `export_json(filename)` → Save all data as JSON
     - `import_json(filename)` → Load data from JSON
   - Use `@dataclass` for the Student model
   - Use type hints everywhere
   - Use `@property` for computed fields
   - Raise custom exceptions (`StudentNotFoundError`, `DuplicateStudentError`)
2. Create `test_analytics.py` with:
   - At least 15 test functions
   - Use `@pytest.fixture` for test data
   - Use `@pytest.mark.parametrize` for testing multiple inputs
   - Test edge cases (empty list, single student, all same marks)
   - Test custom exceptions are raised correctly
   - Test file I/O (JSON export/import)
   - Achieve at least 90% code coverage

**Deliverables:**
- `analytics.py` — The analytics library
- `test_analytics.py` — The test suite
- Run `pytest -v --cov=analytics` and paste the output as a comment at the end of the test file

---

## Submission Guidelines
- All files must run without errors
- Use type hints in all function signatures
- Use docstrings for all classes and functions
- Follow PEP 8 style guidelines
- No third-party packages except pytest and pydantic (install with pip)
- Include sample output as comments at the bottom of each file
