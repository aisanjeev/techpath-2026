# Module 01: Python Core — Assignment

## Task 1: Student Grade Calculator (Beginner)

**Objective:** Build a program that takes student marks and generates a grade report.

**Requirements:**
1. Create a list of at least 5 students, each with: name, city, and marks in 3 subjects (out of 100 each)
2. Calculate total marks, percentage, and grade for each student:
   - A+ : 90% and above
   - A  : 75% to 89%
   - B  : 60% to 74%
   - C  : 40% to 59%
   - Fail: below 40%
3. Print a formatted table showing all students with their marks, percentage, and grade
4. Print class statistics: highest scorer, lowest scorer, class average, pass count, fail count

**Deliverables:**
- A single Python file `grade_calculator.py`
- Use f-strings for all output formatting
- Use at least one list comprehension
- Use at least one dictionary

---

## Task 2: Contact Book with File Storage (Intermediate)

**Objective:** Build a contact book that saves and loads data from a JSON file.

**Requirements:**
1. Store contacts as a list of dictionaries with: name, phone, email, city
2. Implement these functions:
   - `add_contact()` — Add a new contact
   - `search_contact(name)` — Search by name (case-insensitive, partial match)
   - `delete_contact(name)` — Delete a contact by name
   - `list_contacts()` — Display all contacts in a formatted table
   - `save_contacts(filename)` — Save all contacts to a JSON file
   - `load_contacts(filename)` — Load contacts from a JSON file
3. Use a menu-driven interface (print menu options, user enters choice number)
4. Validate phone numbers using regex (must be 10 digits)
5. Validate email format using regex

**Deliverables:**
- A single Python file `contact_book.py`
- The program should save contacts to `contacts.json` on exit
- Handle all possible errors (file not found, invalid input, etc.)
- Use at least one custom exception

---

## Task 3: CSV Report Generator (Intermediate)

**Objective:** Read student data from a CSV file, process it, and generate a summary report.

**Requirements:**
1. Create a CSV file `students_data.csv` with columns: Name, City, Course, Fee, Marks
2. Include at least 10 students with Indian names and cities
3. Write a Python program that:
   - Reads the CSV file
   - Shows the total number of students
   - Calculates the total and average fee collected
   - Lists students by city (grouped)
   - Lists students by course (grouped)
   - Finds the topper (highest marks) and lowest scorer
   - Generates a text file `report.txt` with all the above summary
4. Handle the case where the CSV file does not exist

**Deliverables:**
- `students_data.csv` — The input data file
- `csv_report.py` — The processing program
- The program should create `report.txt` when run

---

## Task 4: Text File Analyzer (Advanced)

**Objective:** Build a tool that analyzes any text file and provides detailed statistics.

**Requirements:**
1. Accept a filename as input (or use a default sample file)
2. Analyze the file and report:
   - Total characters (with and without spaces)
   - Total words
   - Total lines (including and excluding blank lines)
   - Top 10 most common words (ignore common words like "the", "is", "and", etc.)
   - Average word length
   - Longest and shortest words
   - Count of sentences (ending with . ? !)
   - All email addresses found (using regex)
   - All phone numbers found (using regex)
3. Save the analysis to a JSON file `analysis_result.json`
4. Use functions for each type of analysis
5. Handle errors gracefully (file not found, empty file, encoding issues)

**Deliverables:**
- `text_analyzer.py` — The main program
- `sample_text.txt` — A sample text file with at least 200 words (include some email addresses and phone numbers)
- The program should create `analysis_result.json` when run

**Bonus challenge:** Add an option to compare two text files and show differences in their statistics.

---

## Submission Guidelines
- Each Python file must run without errors
- Use meaningful variable and function names
- Add comments explaining your logic
- Use f-strings for formatted output
- Handle all edge cases and errors with try/except
- Follow PEP 8 style guidelines (consistent indentation, spacing)
