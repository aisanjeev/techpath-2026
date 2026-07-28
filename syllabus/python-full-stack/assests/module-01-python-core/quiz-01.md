# Quiz: Python Core — Language Fundamentals

**Module 01 | 15 Questions | Pass Mark: 60%**

---

## Q1. What must you check during Python installation on Windows to use Python from the command line?

- A) Install for all users
- B) Add Python to PATH ✅
- C) Install pip separately
- D) Choose custom installation

> **Explanation:** Checking 'Add Python to PATH' during installation allows you to run Python from any terminal or command prompt. Without this, the system will not find the python command.

---

## Q2. What is the output of: type(3.14)?

- A) `<class 'int'>`
- B) `<class 'decimal'>`
- C) `<class 'float'>` ✅
- D) `<class 'number'>`

> **Explanation:** 3.14 is a decimal number, and Python stores decimal numbers as the 'float' data type.

---

## Q3. What will int(7.9) return?

- A) 8
- B) 7 ✅
- C) 7.0
- D) Error

> **Explanation:** int() truncates the decimal part without rounding. So int(7.9) removes .9 and gives 7, not 8.

---

## Q4. Which of the following is a valid Python variable name?

- A) 2nd_student
- B) student-name
- C) student_name ✅
- D) class

> **Explanation:** student_name follows Python naming rules: starts with a letter, uses only letters/digits/underscores. '2nd_student' starts with a digit, 'student-name' uses a hyphen, and 'class' is a reserved keyword.

---

## Q5. What is the output of: print(f'{10 / 3:.2f}')?

- A) 3.33 ✅
- B) 3.3333333
- C) 3
- D) 3.34

> **Explanation:** The f-string format :.2f means 'format as float with 2 decimal places'. 10/3 = 3.333..., rounded to 2 decimals = 3.33.

---

## Q6. What does the 'elif' keyword do in Python?

- A) Ends the if block
- B) Checks another condition if the previous if was False ✅
- C) Creates a loop
- D) Defines an exception handler

> **Explanation:** elif (short for 'else if') checks an additional condition when the previous if or elif condition was False. It allows multiple condition checks in sequence.

---

## Q7. What will range(2, 8, 2) generate?

- A) 2, 3, 4, 5, 6, 7
- B) 2, 4, 6 ✅
- C) 2, 4, 6, 8
- D) 0, 2, 4, 6

> **Explanation:** range(start, stop, step) generates numbers from start to stop-1 with the given step. So range(2, 8, 2) gives 2, 4, 6 (8 is excluded).

---

## Q8. What does *args do in a function definition?

- A) Makes all arguments required
- B) Accepts any number of keyword arguments as a dictionary
- C) Accepts any number of positional arguments as a tuple ✅
- D) Multiplies the arguments together

> **Explanation:** *args collects any number of positional arguments into a tuple. For example, def total(*args) can accept total(1, 2, 3) where args = (1, 2, 3).

---

## Q9. Which data structure does NOT allow duplicate values?

- A) list
- B) tuple
- C) set ✅
- D) dict values

> **Explanation:** Sets automatically remove duplicates. If you create {1, 2, 2, 3}, it becomes {1, 2, 3}. Lists and tuples can have duplicates.

---

## Q10. What is the correct way to access the value for key 'name' in a dictionary safely?

- A) dict.name
- B) dict['name']
- C) dict.get('name', 'N/A') ✅
- D) dict.find('name')

> **Explanation:** dict.get('name', 'N/A') is the safest way because it returns the default value 'N/A' if the key does not exist, instead of raising a KeyError like dict['name'] would.

---

## Q11. What will [x**2 for x in range(4)] produce?

- A) [1, 4, 9, 16]
- B) [0, 1, 4, 9] ✅
- C) [0, 2, 4, 6]
- D) [1, 2, 3, 4]

> **Explanation:** range(4) generates 0, 1, 2, 3. Squaring each: 0**2=0, 1**2=1, 2**2=4, 3**2=9. Result: [0, 1, 4, 9].

---

## Q12. Which re module function returns ALL matches in a string?

- A) re.search()
- B) re.match()
- C) re.findall() ✅
- D) re.split()

> **Explanation:** re.findall() returns a list of all non-overlapping matches in the string. re.search() returns only the first match, and re.match() only checks the beginning of the string.

---

## Q13. What happens when you use 'w' mode to open a file that already exists?

- A) It appends to the end
- B) It raises a FileExistsError
- C) It deletes all existing content and starts fresh ✅
- D) It opens in read-only mode

> **Explanation:** Opening a file in 'w' (write) mode overwrites all existing content. If you want to add to the end without deleting, use 'a' (append) mode.

---

## Q14. What does the 'finally' block do in exception handling?

- A) Runs only if an exception occurs
- B) Runs only if no exception occurs
- C) Runs always, whether an exception occurred or not ✅
- D) Catches all uncaught exceptions

> **Explanation:** The 'finally' block always executes, regardless of whether an exception was raised or not. It is typically used for cleanup tasks like closing files or database connections.

---

## Q15. What is the purpose of a virtual environment (venv) in Python?

- A) To make Python run faster
- B) To isolate project dependencies from other projects ✅
- C) To run Python in a virtual machine
- D) To encrypt your Python code

> **Explanation:** A virtual environment creates an isolated space for each project's packages. This prevents dependency conflicts when different projects need different versions of the same package.
