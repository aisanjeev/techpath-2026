# Quiz: Python Programming

**Module 10 | 12 Questions | Pass Mark: 60%**

---

## Q1. What is the correct way to print text in Python?

- A) echo('Hello')
- B) System.out.println('Hello')
- C) print('Hello') ✅
- D) console.log('Hello')

> **Explanation:** Python uses `print()` to output text. echo is PHP, System.out.println is Java, console.log is JavaScript.

---

## Q2. What is the output of: print(type(3.14))?

- A) `<class 'int'>`
- B) `<class 'float'>` ✅
- C) `<class 'str'>`
- D) `<class 'double'>`

> **Explanation:** 3.14 is a decimal number, which is `float` type in Python. Python has no `double` type.

---

## Q3. Which keyword creates a variable that should not change?

- A) const
- B) final
- C) Python has no constant keyword ✅
- D) let

> **Explanation:** Python has no const or final keyword. By convention, use ALL_CAPS for constants: `MAX_SIZE = 100`.

---

## Q4. What does 10 // 3 give in Python?

- A) 3.33
- B) 3 ✅
- C) 4
- D) Error

> **Explanation:** `//` is integer division (floor division). `10 // 3 = 3` (drops the decimal). Regular `/` gives `3.333...`

---

## Q5. How do you create a list in Python?

- A) list = (1, 2, 3)
- B) list = [1, 2, 3] ✅
- C) list = {1, 2, 3}
- D) list = <1, 2, 3>

> **Explanation:** Lists use square brackets `[]`. Parentheses `()` are for tuples. Curly braces `{}` are for sets or dicts.

---

## Q6. What does the append() method do?

- A) Removes last item
- B) Adds item to the end of a list ✅
- C) Sorts the list
- D) Reverses the list

> **Explanation:** `list.append(item)` adds an item to the end of the list. It modifies the original list.

---

## Q7. What is an f-string in Python?

- A) A file string
- B) A formatted string with variables inside {} ✅
- C) A frozen string
- D) A function string

> **Explanation:** f-strings let you put variables directly in strings: `f"Hello {name}, age {age}"`.

---

## Q8. What is a dictionary in Python?

- A) A list of words
- B) Key-value pairs like {"name": "Rahul"} ✅
- C) A sorted array
- D) A type of function

> **Explanation:** A dictionary stores key-value pairs: `{"name": "Rahul", "age": 20}`. Access by key: `student["name"]`.

---

## Q9. What does "with open()" do?

- A) Opens a web browser
- B) Opens a file and auto-closes when done ✅
- C) Opens a new window
- D) Opens a database

> **Explanation:** `with open('file.txt', 'r') as f:` opens a file and automatically closes it when the block ends.

---

## Q10. What is a list comprehension?

- A) A way to understand lists
- B) A short way to create lists: [x**2 for x in range(5)] ✅
- C) A list sorting method
- D) A list documentation

> **Explanation:** List comprehension creates lists in one line: `[x**2 for x in range(5)]` gives `[0, 1, 4, 9, 16]`.

---

## Q11. What keyword defines a function in Python?

- A) function
- B) func
- C) def ✅
- D) fn

> **Explanation:** Python uses `def` to define functions: `def greet(name): return f'Hello, {name}!'`

---

## Q12. What does try/except do in Python?

- A) Tries to run code, runs except block if an error occurs ✅
- B) Tests code speed
- C) Tries two solutions
- D) Exports code

> **Explanation:** try/except handles errors gracefully. Code in `try` runs first. If it fails, `except` runs instead of crashing.

---

## Answer Key

| Q  | Answer | Q  | Answer |
|----|--------|----|--------|
| 1  | C      | 7  | B      |
| 2  | B      | 8  | B      |
| 3  | C      | 9  | B      |
| 4  | B      | 10 | B      |
| 5  | B      | 11 | C      |
| 6  | B      | 12 | A      |
