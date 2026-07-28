# JavaScript — Real-World Mini Projects

**Module 09 — JavaScript + Bootstrap | Build to Learn**

---

## Why This Matters

> Reading about `addEventListener` doesn't make you a developer. Building a working calculator, a to-do app, and a quiz game does. These are the exact projects interviewers ask freshers about.

---

## Project 1: Calculator App

### What You'll Build

A functional calculator that looks like the iOS/Android calculator.

> 🖼️ **IMAGE:** A calculator app with dark background — display area showing "124.5" at top, number pad buttons (0-9), operator buttons (+, −, ×, ÷) in orange/accent color, C/CE buttons, decimal point, and equals button — clean grid layout with rounded buttons
> `js-calculator-final.png`

### Key JavaScript Concepts Used

| Concept | How It's Used |
|---------|--------------|
| `querySelector` | Select display and buttons |
| `addEventListener('click')` | Handle button clicks |
| `textContent` | Update display |
| `eval()` or manual parsing | Calculate result |
| String manipulation | Build expression |
| Conditional logic | Handle operators, clear, equals |

### Core Logic

```javascript
let display = document.querySelector('.display');
let currentInput = '';

function appendNumber(num) {
    currentInput += num;
    display.textContent = currentInput;
}

function appendOperator(op) {
    // Don't allow operator at start or double operator
    if (currentInput === '' || '+-*/'.includes(currentInput.slice(-1))) return;
    currentInput += op;
    display.textContent = currentInput;
}

function calculate() {
    try {
        let result = Function('"use strict"; return (' + currentInput + ')')();
        // Round to avoid floating point issues (0.1 + 0.2 = 0.30000000000000004)
        result = Math.round(result * 1000000) / 1000000;
        display.textContent = result;
        currentInput = String(result);
    } catch (e) {
        display.textContent = 'Error';
        currentInput = '';
    }
}

function clearDisplay() {
    currentInput = '';
    display.textContent = '0';
}
```

**Watch out for:** `0.1 + 0.2 = 0.30000000000000004` in JavaScript! Always round results.

---

## Project 2: To-Do List App

### What You'll Build

A task manager with add, complete, delete, and local storage (tasks survive page refresh).

> 🖼️ **IMAGE:** A to-do list app — input field at top with "Add Task" button, below it a list of tasks: some with checkboxes unchecked (normal text), some checked (text has strikethrough), each task has a red delete (×) button on the right — clean white card design on light gray background
> `js-todo-app-final.png`

### Key JavaScript Concepts Used

| Concept | How It's Used |
|---------|--------------|
| `createElement` | Create new task elements dynamically |
| `appendChild` / `remove` | Add/delete tasks from DOM |
| `classList.toggle` | Toggle "completed" style |
| `localStorage` | Save tasks so they survive refresh |
| `JSON.stringify/parse` | Convert tasks array to/from string |
| Event delegation | Handle clicks on dynamically created elements |

### Core Logic

```javascript
let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function addTask() {
    const input = document.querySelector('#taskInput');
    const text = input.value.trim();
    if (text === '') return;

    tasks.push({ text: text, done: false });
    saveTasks();
    renderTasks();
    input.value = '';
    input.focus();
}

function toggleTask(index) {
    tasks[index].done = !tasks[index].done;
    saveTasks();
    renderTasks();
}

function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    renderTasks();
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function renderTasks() {
    const list = document.querySelector('#taskList');
    list.innerHTML = '';

    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        li.className = task.done ? 'task done' : 'task';

        li.innerHTML = `
            <span onclick="toggleTask(${index})">${task.text}</span>
            <button onclick="deleteTask(${index})">×</button>
        `;

        list.appendChild(li);
    });
}

// Handle Enter key
document.querySelector('#taskInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addTask();
});

// Load on page start
renderTasks();
```

### What Makes This Job-Relevant

This small project covers:
- **DOM manipulation** — creating, reading, updating, deleting elements
- **Event handling** — click, keydown, dynamic events
- **Data persistence** — localStorage
- **Array methods** — push, splice, forEach
- **State management** — keeping UI in sync with data

These are the exact patterns used in React, Vue, and Angular — just at a smaller scale.

---

## Project 3: Quiz Game

### What You'll Build

An interactive quiz with score tracking, timer, and result screen.

> 🖼️ **IMAGE:** A quiz game interface — top bar showing "Question 3 of 10" and a countdown timer "0:28", question text in the center, 4 answer option buttons below (one highlighted green as correct after clicking), a progress bar at the bottom, and "Next" button
> `js-quiz-game-final.png`

### Core Logic

```javascript
const questions = [
    {
        question: "What does HTML stand for?",
        options: [
            "Hyper Text Markup Language",
            "High Tech Modern Language",
            "Hyper Transfer Markup Language",
            "Home Tool Markup Language"
        ],
        correct: 0
    },
    {
        question: "Which CSS property makes text bold?",
        options: ["text-style: bold", "font-weight: bold", "text-weight: bold", "font-bold: true"],
        correct: 1
    }
    // ... more questions
];

let currentQuestion = 0;
let score = 0;
let timeLeft = 30;
let timer;

function loadQuestion() {
    const q = questions[currentQuestion];
    document.querySelector('#question').textContent = q.question;
    document.querySelector('#progress').textContent =
        `Question ${currentQuestion + 1} of ${questions.length}`;

    const optionsContainer = document.querySelector('#options');
    optionsContainer.innerHTML = '';

    q.options.forEach((option, index) => {
        const btn = document.createElement('button');
        btn.textContent = option;
        btn.className = 'option-btn';
        btn.onclick = () => checkAnswer(index, btn);
        optionsContainer.appendChild(btn);
    });

    // Start timer
    timeLeft = 30;
    clearInterval(timer);
    timer = setInterval(updateTimer, 1000);
}

function checkAnswer(selected, btn) {
    clearInterval(timer);
    const correct = questions[currentQuestion].correct;

    // Disable all buttons
    document.querySelectorAll('.option-btn').forEach(b => b.disabled = true);

    if (selected === correct) {
        btn.classList.add('correct');
        score++;
    } else {
        btn.classList.add('wrong');
        // Highlight correct answer
        document.querySelectorAll('.option-btn')[correct].classList.add('correct');
    }

    // Auto-advance after 1.5 seconds
    setTimeout(() => {
        currentQuestion++;
        if (currentQuestion < questions.length) {
            loadQuestion();
        } else {
            showResult();
        }
    }, 1500);
}

function updateTimer() {
    timeLeft--;
    document.querySelector('#timer').textContent = `0:${timeLeft.toString().padStart(2, '0')}`;
    if (timeLeft <= 0) {
        clearInterval(timer);
        // Auto-skip on timeout
        currentQuestion++;
        if (currentQuestion < questions.length) loadQuestion();
        else showResult();
    }
}

function showResult() {
    const percentage = Math.round((score / questions.length) * 100);
    document.querySelector('#quiz-container').innerHTML = `
        <h2>Quiz Complete!</h2>
        <p class="score">Score: ${score}/${questions.length} (${percentage}%)</p>
        <p>${percentage >= 70 ? '🎉 Great job!' : '📚 Keep practicing!'}</p>
        <button onclick="location.reload()">Try Again</button>
    `;
}

loadQuestion();
```

---

## Project 4: Expense Tracker

### What You'll Build

Track income and expenses with a running balance. Data saved in localStorage.

> 🖼️ **IMAGE:** An expense tracker app — top shows balance "₹15,240" in large text, two summary boxes below (Income: ₹25,000 in green, Expense: ₹9,760 in red), then a form to add transaction (description, amount, type dropdown), and a scrollable list of recent transactions with amounts and delete buttons
> `js-expense-tracker-final.png`

### What This Teaches

| Skill | Used For |
|-------|----------|
| Form handling | Getting user input |
| Array filtering | Separating income/expense |
| `reduce()` | Calculating totals |
| `toLocaleString('en-IN')` | Indian number formatting (₹12,500) |
| Conditional styling | Green for income, red for expense |
| localStorage | Data persistence |

### Key Code Pattern: Indian Currency Formatting

```javascript
function formatCurrency(amount) {
    return '₹' + Math.abs(amount).toLocaleString('en-IN');
}

// ₹12,50,000 (Indian format with lakh/crore grouping)
```

---

## JavaScript Patterns That Come Up in Every Interview

### 1. Debouncing (Search Box)

Don't fire API call on every keystroke — wait until user stops typing.

```javascript
let debounceTimer;
searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        searchAPI(e.target.value);
    }, 300); // Wait 300ms after last keystroke
});
```

### 2. Fetching Data from API

```javascript
async function fetchUsers() {
    try {
        const response = await fetch('https://api.example.com/users');
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();
        displayUsers(data);
    } catch (error) {
        console.error('Error:', error.message);
        showErrorMessage('Could not load users. Please try again.');
    }
}
```

### 3. Event Delegation

Instead of adding click listener to 100 buttons individually:

```javascript
// Bad: listener on each button
buttons.forEach(btn => btn.addEventListener('click', handler));

// Good: one listener on the parent
document.querySelector('#button-container').addEventListener('click', (e) => {
    if (e.target.matches('.action-btn')) {
        handleAction(e.target.dataset.id);
    }
});
```

---

## Practice Exercises (Build These Yourself)

### Exercise 1: Stopwatch
- Start, Stop, Reset buttons
- Display: 00:00:00 (minutes:seconds:milliseconds)
- Lap times feature

### Exercise 2: Random Password Generator
- Input: password length (slider or number input)
- Checkboxes: uppercase, lowercase, numbers, symbols
- Generate button → display password
- Copy to clipboard button

### Exercise 3: Weather App (API)
- Input: city name
- Fetch weather from a free API (OpenWeatherMap)
- Display: temperature, humidity, condition, icon
- Handle errors: city not found

### Exercise 4: Image Gallery with Lightbox
- Grid of thumbnail images
- Click any image → full-size view in a modal overlay
- Previous/Next navigation in lightbox
- Close with × button or Escape key
