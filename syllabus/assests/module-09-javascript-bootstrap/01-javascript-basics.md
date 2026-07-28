# JavaScript — Making Web Pages Interactive

**Module 09 — JavaScript + Bootstrap | Topic 1**

---

## What is JavaScript?

**JavaScript (JS)** is the programming language of the web. It makes web pages **interactive**.

| Language | Role | Analogy |
|----------|------|---------|
| HTML | Structure (what to show) | Skeleton/bones |
| CSS | Style (how it looks) | Skin/clothes |
| **JavaScript** | Behavior (what it does) | Brain/muscles |

> **Examples of JS in action:** Clicking a button to show a menu, form validation, image sliders, pop-up alerts, live search, dark mode toggle.

---

## Where to Write JavaScript

### 1. Inside HTML file (internal)

```html
<script>
    alert("Hello, World!");
</script>
```

### 2. Separate file (external — BEST)

```html
<script src="script.js"></script>
```

> **Always put `<script>` at the bottom of `<body>`** — so HTML loads first, then JS runs.

---

## Variables — Storing Data

```javascript
// let — value CAN change
let age = 20;
age = 21;  // allowed

// const — value CANNOT change
const name = "Rahul";
// name = "Priya";  // ERROR! Can't change const

// var — old way (avoid using)
var city = "Delhi";
```

### When to Use What

| Keyword | Can Change? | Use When |
|---------|------------|----------|
| `const` | No | Value won't change (most of the time) |
| `let` | Yes | Value will change (counters, toggles) |
| `var` | Yes | Old code only (don't use in new code) |

> **Default to `const`.** Only use `let` when you need to change the value.

---

## Data Types

| Type | Example | What It Is |
|------|---------|-----------|
| **String** | `"Hello"` or `'Hello'` | Text |
| **Number** | `42`, `3.14` | Numbers (no quotes) |
| **Boolean** | `true`, `false` | Yes/No values |
| **Array** | `[1, 2, 3]` | List of items |
| **Object** | `{name: "Rahul", age: 20}` | Key-value pairs |
| **Null** | `null` | Empty on purpose |
| **Undefined** | `undefined` | Not assigned yet |

```javascript
const name = "Priya";           // String
const age = 22;                 // Number
const isStudent = true;         // Boolean
const marks = [85, 90, 78];     // Array
const student = {               // Object
    name: "Priya",
    age: 22,
    course: "ADCA"
};
```

---

## Operators

### Math Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Add | `5 + 3` | `8` |
| `-` | Subtract | `10 - 4` | `6` |
| `*` | Multiply | `3 * 4` | `12` |
| `/` | Divide | `15 / 3` | `5` |
| `%` | Remainder | `10 % 3` | `1` |
| `**` | Power | `2 ** 3` | `8` |

### Comparison Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `===` | Equal (strict) | `5 === 5` | `true` |
| `!==` | Not equal | `5 !== 3` | `true` |
| `>` | Greater than | `10 > 5` | `true` |
| `<` | Less than | `3 < 7` | `true` |
| `>=` | Greater or equal | `5 >= 5` | `true` |
| `<=` | Less or equal | `3 <= 2` | `false` |

> **Use `===` not `==`.** Triple equals checks both value AND type.

---

## Conditionals — Making Decisions

```javascript
const marks = 75;

if (marks >= 90) {
    console.log("Grade: A");
} else if (marks >= 75) {
    console.log("Grade: B");
} else if (marks >= 60) {
    console.log("Grade: C");
} else {
    console.log("Grade: F");
}
// Output: "Grade: B"
```

---

## Loops — Repeating Actions

### for loop

```javascript
// Print 1 to 5
for (let i = 1; i <= 5; i++) {
    console.log(i);
}
```

### while loop

```javascript
let count = 1;
while (count <= 5) {
    console.log(count);
    count++;
}
```

### for...of (loop through array)

```javascript
const fruits = ["Apple", "Banana", "Mango"];
for (const fruit of fruits) {
    console.log(fruit);
}
```

---

## Functions — Reusable Code Blocks

```javascript
// Declare a function
function greet(name) {
    return "Hello, " + name + "!";
}

// Call the function
console.log(greet("Rahul"));   // "Hello, Rahul!"
console.log(greet("Priya"));   // "Hello, Priya!"

// Arrow function (modern way)
const add = (a, b) => a + b;
console.log(add(5, 3));  // 8
```

---

## Arrays — Lists of Data

```javascript
const colors = ["Red", "Blue", "Green"];

// Access items (index starts at 0)
console.log(colors[0]);    // "Red"
console.log(colors[2]);    // "Green"
console.log(colors.length); // 3

// Add to end
colors.push("Yellow");

// Remove from end
colors.pop();

// Loop through
colors.forEach(color => {
    console.log(color);
});

// Find item
const found = colors.includes("Blue");  // true

// Filter
const longNames = colors.filter(c => c.length > 3);

// Map (transform each item)
const upper = colors.map(c => c.toUpperCase());
```

---

## Objects — Key-Value Data

```javascript
const student = {
    name: "Rahul",
    age: 20,
    course: "ADCA",
    marks: [85, 90, 78]
};

// Access values
console.log(student.name);       // "Rahul"
console.log(student["course"]);  // "ADCA"

// Add new property
student.email = "rahul@email.com";

// Object destructuring
const { name, age } = student;
console.log(name);  // "Rahul"
```

---

## DOM — Changing Web Pages with JS

**DOM** = Document Object Model — JavaScript's way to access and change HTML.

```javascript
// Select elements
const heading = document.getElementById("title");
const cards = document.querySelectorAll(".card");
const btn = document.querySelector(".btn");

// Change content
heading.textContent = "New Title";
heading.innerHTML = "<em>New Title</em>";

// Change style
heading.style.color = "blue";
heading.style.fontSize = "32px";

// Add/remove class
heading.classList.add("highlight");
heading.classList.remove("old-class");
heading.classList.toggle("dark-mode");

// Handle events
btn.addEventListener("click", () => {
    alert("Button clicked!");
});
```

### Common Events

| Event | When It Fires |
|-------|-------------|
| `click` | Element is clicked |
| `submit` | Form is submitted |
| `input` | User types in input field |
| `mouseover` | Mouse hovers over element |
| `keydown` | Key is pressed |
| `load` | Page finishes loading |

---

## Template Literals — Easy String Building

```javascript
const name = "Priya";
const age = 22;

// Old way (concatenation)
const msg1 = "Hello, " + name + "! You are " + age + " years old.";

// Modern way (template literals)
const msg2 = `Hello, ${name}! You are ${age} years old.`;
```

> Use backticks (\`) instead of quotes. Put variables inside `${variable}`.

---

## Summary

- **JavaScript** makes web pages interactive (brain/muscles)
- Use `const` by default, `let` when value changes
- 7 data types: String, Number, Boolean, Array, Object, Null, Undefined
- Use `===` for comparison (not `==`)
- **Functions** are reusable code blocks
- **Arrays** = lists, **Objects** = key-value pairs
- **DOM** lets JS change HTML/CSS on the page
- **Template literals** (\`${var}\`) for easy string building
