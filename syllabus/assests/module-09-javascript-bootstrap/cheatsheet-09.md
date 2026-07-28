# Cheat Sheet: JavaScript + Bootstrap

**Module 09 — Quick Reference**

---

## JavaScript Variables

```javascript
const name = "Rahul";   // can't change
let age = 20;           // can change
```

---

## Data Types

| Type | Example |
|------|---------|
| String | `"Hello"` |
| Number | `42`, `3.14` |
| Boolean | `true`, `false` |
| Array | `[1, 2, 3]` |
| Object | `{name: "R", age: 20}` |

---

## Operators

| Compare | Math |
|---------|------|
| `===` equal | `+` add |
| `!==` not equal | `-` subtract |
| `>` `<` `>=` `<=` | `*` `/ ` `%` `**` |

---

## Common Array Methods

| Method | What |
|--------|------|
| `.push()` | Add to end |
| `.pop()` | Remove from end |
| `.map()` | Transform each item |
| `.filter()` | Keep matching items |
| `.find()` | First match |
| `.forEach()` | Loop through |
| `.includes()` | Check if exists |
| `.reduce()` | Combine to one value |

---

## DOM Basics

```javascript
// Select
document.getElementById("id")
document.querySelector(".class")
document.querySelectorAll("div")

// Change
el.textContent = "new text"
el.style.color = "blue"
el.classList.add("active")
el.classList.toggle("dark")

// Events
el.addEventListener("click", () => {
  // do something
})
```

---

## Bootstrap Grid (12 columns)

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Half</div>
    <div class="col-md-6">Half</div>
  </div>
</div>
```

| Class | Width |
|-------|-------|
| col-12 | 100% |
| col-6 | 50% |
| col-4 | 33% |
| col-3 | 25% |

---

## Bootstrap Colors

| Prefix | Color |
|--------|-------|
| primary | Blue |
| success | Green |
| danger | Red |
| warning | Yellow |
| dark | Black |

Use with: `btn-*`, `text-*`, `bg-*`, `alert-*`

---

## Bootstrap Spacing

`m` = margin, `p` = padding
`t/b/s/e/x/y` = top/bottom/start/end/horizontal/vertical
`0-5` = size (0=none, 5=3rem)

Example: `mt-3` = margin-top 1rem, `px-4` = padding left+right 1.5rem
