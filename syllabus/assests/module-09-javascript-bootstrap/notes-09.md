# Module 09 — JavaScript + Bootstrap — Quick Revision Notes

---

## JavaScript Basics
- JS adds **behavior** to web pages (HTML = structure, CSS = style, JS = action)
- Runs in the browser — no installation needed
- Add to HTML: `<script src="script.js"></script>` (before `</body>`)

## Variables
```javascript
let age = 22;         // can change later
const name = "Rahul"; // cannot change
var city = "Delhi";   // old way — avoid
```
| Use | When |
|-----|------|
| `const` | Value won't change (default choice) |
| `let` | Value will change (counters, toggles) |
| `var` | Never (legacy code only) |

## Data Types
| Type | Example | Check |
|------|---------|-------|
| String | `"hello"`, `'hi'`, `` `template` `` | `typeof x === "string"` |
| Number | `42`, `3.14` | `typeof x === "number"` |
| Boolean | `true`, `false` | `typeof x === "boolean"` |
| Array | `[1, 2, 3]` | `Array.isArray(x)` |
| Object | `{ name: "Rahul", age: 22 }` | `typeof x === "object"` |
| Null | `null` | Intentionally empty |
| Undefined | `undefined` | Variable declared but no value |

## Operators
```javascript
// Comparison — ALWAYS use === (strict)
5 === 5    // true (same type + value)
5 == "5"   // true (BAD — converts type)
5 !== 3    // true

// Logical
true && false  // AND → false
true || false  // OR → true
!true          // NOT → false

// Template Literal (string with variables)
const msg = `Hello ${name}, you are ${age} years old`;
```

## Conditionals
```javascript
if (marks >= 90) {
    grade = "A+";
} else if (marks >= 75) {
    grade = "A";
} else if (marks >= 60) {
    grade = "B";
} else {
    grade = "Fail";
}
```

## Loops
```javascript
// for loop
for (let i = 0; i < 5; i++) { console.log(i); }

// for...of (arrays)
for (const item of items) { console.log(item); }

// forEach (array method)
items.forEach(item => console.log(item));

// while
while (count > 0) { count--; }
```

## Functions
```javascript
// Regular function
function add(a, b) { return a + b; }

// Arrow function (modern)
const add = (a, b) => a + b;

// Default parameter
const greet = (name = "Guest") => `Hello ${name}`;
```

## Arrays
```javascript
const fruits = ["apple", "banana", "mango"];
fruits.push("grape");       // add to end
fruits.pop();               // remove from end
fruits.length;              // 3
fruits.includes("apple");   // true

// Key methods
fruits.map(f => f.toUpperCase());      // transform each
fruits.filter(f => f.length > 5);      // filter
fruits.find(f => f === "mango");       // find first match
fruits.forEach(f => console.log(f));   // loop
```

## Objects
```javascript
const student = {
    name: "Rahul",
    age: 22,
    courses: ["ADCA", "Python"],
    greet() { return `Hi, I'm ${this.name}`; }
};

student.name;           // "Rahul"
student.age = 23;       // update
student.city = "Delhi"; // add new property
const { name, age } = student; // destructuring
```

## DOM Manipulation
```javascript
// Select elements
document.getElementById("title");
document.querySelector(".card");        // first match
document.querySelectorAll(".card");     // all matches

// Change content
element.textContent = "New text";
element.innerHTML = "<strong>Bold</strong>";

// Change style
element.style.color = "red";
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("hidden");

// Events
button.addEventListener("click", () => {
    alert("Button clicked!");
});
```

## Common Events
| Event | Triggers When |
|-------|--------------|
| `click` | Element is clicked |
| `input` | Input value changes |
| `submit` | Form is submitted |
| `keydown` | Key is pressed |
| `DOMContentLoaded` | HTML fully loaded |
| `change` | Select/checkbox changes |

## Bootstrap Quick Reference
- Add via CDN: `<link>` in head, `<script>` before `</body>`
- Grid: `container` → `row` → `col-md-6`
- Breakpoints: `sm` (576px), `md` (768px), `lg` (992px), `xl` (1200px)

| Component | Class |
|-----------|-------|
| Button | `btn btn-primary` |
| Card | `card`, `card-body`, `card-title` |
| Navbar | `navbar navbar-expand-lg` |
| Alert | `alert alert-success` |
| Modal | `modal`, triggered by `data-bs-toggle` |
| Form | `form-control`, `form-label` |
| Table | `table table-striped table-hover` |
| Badge | `badge bg-primary` |
| Spinner | `spinner-border` |

## Useful Shortcuts
```javascript
console.log(x);          // debug output
console.table(array);    // show array as table
JSON.stringify(obj);     // object → string
JSON.parse(str);         // string → object
parseInt("42");          // string → number
Number("42.5");          // string → decimal
String(42);              // number → string
```
