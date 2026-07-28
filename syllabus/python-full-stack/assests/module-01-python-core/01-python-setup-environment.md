# Python Setup & Environment

**Module 01 — Python Core: Language Fundamentals | Topic 1**

---

## Why Python?

Python is one of the most popular programming languages in the world. It is used for web development, data science, automation, AI, and much more. Companies like Google, Netflix, Instagram, and many Indian startups use Python daily.

**Why beginners love Python:**
- Easy to read — looks almost like English
- Huge community — millions of tutorials and answers online
- Versatile — one language for web, data, AI, scripting
- High demand — Python developers earn well in India (₹4-15 LPA for freshers)

---

## Installing Python

### Step 1: Download Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow button to download the latest version (Python 3.12+)
3. Run the installer

### Step 2: Important — Check "Add Python to PATH"

When the installer opens, you will see a checkbox at the bottom:

```
☑ Add Python 3.12 to PATH
```

**You MUST check this box.** Without it, your computer won't know where Python is installed.

### Step 3: Verify Installation

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux):

```bash
python --version
# Output: Python 3.12.x

pip --version
# Output: pip 24.x.x from ...
```

If you see version numbers, Python is installed correctly.

| Problem | Solution |
|---------|----------|
| `python` not recognized | Reinstall with "Add to PATH" checked |
| Shows Python 2.x | Use `python3` instead of `python` |
| `pip` not recognized | Use `python -m pip` instead |

---

## The Python REPL

REPL stands for **Read-Eval-Print-Loop**. It is an interactive Python shell where you can type code and see results instantly.

### Starting the REPL

```bash
python
```

You will see something like:

```
Python 3.12.4 (main, Jun  7 2024, 00:00:00)
>>> 
```

The `>>>` is the prompt — Python is waiting for your command.

### Trying It Out

```python
>>> 2 + 3
5

>>> "Hello, " + "TechPath!"
'Hello, TechPath!'

>>> print("Welcome to Python!")
Welcome to Python!

>>> 100 * 18 / 100    # Calculate 18% GST on ₹100
18.0

>>> exit()            # Leave the REPL
```

**Think of the REPL as a calculator on steroids** — you can test any Python code instantly without creating a file.

### When to Use the REPL

| Use REPL When... | Use a File When... |
|-------------------|--------------------|
| Testing a quick idea | Writing a real program |
| Checking syntax | Code is more than 5-10 lines |
| Learning a new function | You need to save and run later |
| Doing quick math | Building a project |

---

## VS Code — Your Code Editor

VS Code (Visual Studio Code) is a free, powerful code editor made by Microsoft. Most Python developers use it.

### Installing VS Code

1. Go to [code.visualstudio.com](https://code.visualstudio.com/)
2. Download and install for your operating system
3. Open VS Code

### Essential Extensions

After installing VS Code, add these extensions:

| Extension | Publisher | Why You Need It |
|-----------|-----------|-----------------|
| **Python** | Microsoft | Syntax highlighting, IntelliSense, debugging |
| **Pylance** | Microsoft | Fast, smart code suggestions |
| **Code Runner** | Jun Han | Run code with one click |
| **Prettier** | Prettier | Auto-format your code |

### How to Install an Extension

1. Click the Extensions icon in the left sidebar (or press `Ctrl+Shift+X`)
2. Search for the extension name
3. Click **Install**

### Your First Python File

1. Open VS Code
2. Go to File > Open Folder > Create a new folder called `python-practice`
3. Create a new file: `hello.py`
4. Type:

```python
name = "Rahul"
print(f"Hello, {name}! Welcome to TechPath Institute.")
```

5. Run it: Right-click in the editor > "Run Python File in Terminal"

You should see:
```
Hello, Rahul! Welcome to TechPath Institute.
```

---

## Virtual Environments (venv)

### The Problem

Imagine you are working on two projects:
- **Project A** needs `requests` version 2.28
- **Project B** needs `requests` version 2.31

If both projects share the same Python installation, they will fight over which version to use. This is called a **dependency conflict**.

### The Solution: Virtual Environments

A virtual environment is like a separate room for each project. Each room has its own copy of Python and its own packages. Changes in one room don't affect another.

**Real-world analogy:** Think of it like having separate notebooks for each subject in college. Your Maths notes don't mix with your Science notes.

### Creating a Virtual Environment

```bash
# Navigate to your project folder
cd my-project

# Create a virtual environment named 'venv'
python -m venv venv
```

This creates a `venv` folder inside your project with its own Python copy.

### Activating the Virtual Environment

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac / Linux
source venv/bin/activate
```

After activation, your terminal prompt changes:

```
(venv) C:\Users\Rahul\my-project>
```

The `(venv)` prefix means you are inside the virtual environment.

### Installing Packages Inside venv

```bash
# Now pip installs packages ONLY in this venv
(venv) pip install requests
(venv) pip install flask
```

### Deactivating

```bash
(venv) deactivate
```

The `(venv)` prefix disappears — you are back to the global Python.

### Best Practice

**Always create a virtual environment for every project.** It is the first thing you do after creating a project folder:

```bash
mkdir my-new-project
cd my-new-project
python -m venv venv
venv\Scripts\activate      # Windows
pip install <your-packages>
```

---

## pip — Python Package Manager

pip (Package Installer for Python) lets you install packages from the Python Package Index (PyPI) — a huge library of free Python packages.

### Essential pip Commands

| Command | What It Does |
|---------|--------------|
| `pip install flask` | Install a package |
| `pip install flask==2.3.0` | Install specific version |
| `pip install flask>=2.3.0` | Install version 2.3.0 or newer |
| `pip install --upgrade flask` | Update to latest version |
| `pip uninstall flask` | Remove a package |
| `pip list` | Show all installed packages |
| `pip show flask` | Show details of a package |
| `pip freeze` | List packages with exact versions |

### requirements.txt — Saving Your Dependencies

When you share your project with someone else (or deploy it to a server), they need to install the same packages. The `requirements.txt` file lists all your dependencies.

```bash
# Save current packages to requirements.txt
pip freeze > requirements.txt
```

The file looks like:

```
flask==2.3.3
requests==2.31.0
numpy==1.26.4
```

To install all packages from this file:

```bash
pip install -r requirements.txt
```

### Common Packages for Beginners

| Package | Purpose |
|---------|---------|
| `requests` | Make HTTP requests (call APIs) |
| `flask` | Build web applications |
| `fastapi` | Build modern APIs |
| `numpy` | Work with numbers and arrays |
| `pandas` | Work with data tables |
| `pytest` | Write and run tests |

---

## Project Folder Structure

As a professional developer, organize your projects properly from day one:

```
my-python-project/
├── venv/                  # Virtual environment (don't edit this)
├── app/                   # Your code goes here
│   ├── __init__.py
│   └── main.py
├── tests/                 # Your test files
│   └── test_main.py
├── requirements.txt       # Dependencies
├── .gitignore             # Files Git should ignore
└── README.md              # Project description
```

### .gitignore for Python Projects

Create a `.gitignore` file to tell Git to ignore certain files:

```
venv/
__pycache__/
*.pyc
.env
.vscode/
```

**Never upload your `venv/` folder** to GitHub — it is large and can be recreated from `requirements.txt`.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Python Installation | Always check "Add to PATH" |
| REPL | Interactive shell for quick tests |
| VS Code | Recommended editor with Python extension |
| Virtual Environment | Isolates packages per project — always use one |
| pip | Install packages from PyPI |
| requirements.txt | Lists project dependencies for sharing |

---

## Practice Tasks

1. Install Python and verify with `python --version`
2. Open the REPL and calculate: What is 18% GST on ₹1500?
3. Install VS Code and the Python extension
4. Create a virtual environment and install the `requests` package
5. Create a `requirements.txt` file from your virtual environment
