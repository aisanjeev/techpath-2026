# Quiz: Python Libraries

**Module 11 | 12 Questions | Pass Mark: 60%**

---

## Q1. What is NumPy used for?
- A) Web development
- B) Fast math on arrays and matrices ✅
- C) Database management
- D) File compression

> **Explanation:** NumPy provides fast math operations on arrays and matrices.

---

## Q2. What is a Pandas DataFrame?
- A) A type of graph
- B) A table-like data structure with rows and columns ✅
- C) A database engine
- D) A web framework

> **Explanation:** A DataFrame is like an Excel spreadsheet in Python — rows and columns with labels.

---

## Q3. How do you read a CSV file in Pandas?
- A) pd.open_csv()
- B) pd.read_csv() ✅
- C) pd.load_csv()
- D) pd.import_csv()

> **Explanation:** `pd.read_csv('file.csv')` reads a CSV file into a DataFrame.

---

## Q4. Which library creates charts and graphs in Python?
- A) NumPy
- B) Pandas
- C) Matplotlib ✅
- D) Requests

> **Explanation:** Matplotlib creates line charts, bar charts, pie charts with `plt.plot()`, `plt.bar()`, etc.

---

## Q5. What does df.describe() show?
- A) Column names only
- B) Statistical summary (mean, min, max, count) ✅
- C) Data types
- D) First 5 rows

> **Explanation:** `df.describe()` shows count, mean, std, min, max, and quartiles for all numeric columns.

---

## Q6. How do you filter rows where marks > 80 in Pandas?
- A) df.filter(marks > 80)
- B) df[df['Marks'] > 80] ✅
- C) df.where('Marks', 80)
- D) df.select(marks > 80)

> **Explanation:** `df[df['Marks'] > 80]` filters to only rows where Marks column is greater than 80.

---

## Q7. What does requests.get(url) do?
- A) Downloads a file
- B) Sends an HTTP GET request to a URL ✅
- C) Opens a browser
- D) Creates a web server

> **Explanation:** `requests.get(url)` sends a GET request and returns the response. Use `.json()` to parse JSON.

---

## Q8. What is BeautifulSoup used for?
- A) Making soups
- B) Parsing HTML to extract data from web pages ✅
- C) Creating web pages
- D) Styling web pages

> **Explanation:** BeautifulSoup parses HTML and lets you find elements by tag, class, or ID — for web scraping.

---

## Q9. Which command installs a Python package?
- A) python install package
- B) pip install package ✅
- C) npm install package
- D) apt install package

> **Explanation:** `pip` is Python's package manager. `pip install package_name` downloads and installs from PyPI.

---

## Q10. What does json.dumps() do?
- A) Deletes JSON
- B) Converts Python dict to JSON string ✅
- C) Reads a JSON file
- D) Dumps data to database

> **Explanation:** `json.dumps()` converts a Python dict to a JSON string. `json.loads()` does the reverse.

---

## Q11. What is a virtual environment in Python?
- A) A virtual reality tool
- B) An isolated space for project-specific packages ✅
- C) A cloud server
- D) A virtual machine

> **Explanation:** A virtual environment keeps each project's dependencies separate so they don't conflict.

---

## Q12. What does df.groupby('Course')['Marks'].mean() do?
- A) Groups data and calculates average marks per course ✅
- B) Creates a new column
- C) Sorts by course name
- D) Deletes the course column

> **Explanation:** `groupby` groups rows by Course, then `.mean()` calculates the average Marks per group.

---

## Answer Key

| Q  | Answer | Q  | Answer |
|----|--------|----|--------|
| 1  | B      | 7  | B      |
| 2  | B      | 8  | B      |
| 3  | B      | 9  | B      |
| 4  | C      | 10 | B      |
| 5  | B      | 11 | B      |
| 6  | B      | 12 | A      |
