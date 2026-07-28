# Quiz: JavaScript + Bootstrap

**Module 09 | 12 Questions | Pass Mark: 60%**

---

## Q1. What is JavaScript used for in web development?

- A) Styling web pages
- B) Making web pages interactive ✅
- C) Creating database tables
- D) Deploying websites

> **Explanation:** JavaScript makes web pages interactive — handling clicks, form validation, animations, dynamic content changes.

---

## Q2. Which keyword should you use to declare a variable that won't change?

- A) var
- B) let
- C) const ✅
- D) static

> **Explanation:** Use `const` for values that won't change. Use `let` only when the value needs to change. Avoid `var`.

---

## Q3. What does === check in JavaScript?

- A) Only value
- B) Only type
- C) Both value AND type ✅
- D) Nothing

> **Explanation:** `===` (strict equality) checks both value AND type. `'5' === 5` is false (string vs number). Always use `===`.

---

## Q4. What is the output of: console.log(typeof 42)?

- A) integer
- B) number ✅
- C) string
- D) float

> **Explanation:** JavaScript has only one number type called "number" — no separate integer or float types.

---

## Q5. How do you add an element to the end of an array?

- A) array.add(item)
- B) array.push(item) ✅
- C) array.append(item)
- D) array.insert(item)

> **Explanation:** `array.push(item)` adds an item to the end. `array.pop()` removes the last item.

---

## Q6. What is a template literal in JavaScript?

- A) A string using backticks with ${} for variables ✅
- B) A type of loop
- C) A CSS template
- D) A function template

> **Explanation:** Template literals use backticks (\`) and `${variable}` for easy string building: `` `Hello, ${name}!` ``

---

## Q7. What does document.querySelector('.card') select?

- A) All elements with class "card"
- B) The first element with class "card" ✅
- C) The element with id "card"
- D) All card tags

> **Explanation:** `querySelector` returns the FIRST matching element. Use `querySelectorAll` to get ALL matching elements.

---

## Q8. How many columns does Bootstrap's grid system have?

- A) 6
- B) 10
- C) 12 ✅
- D) 16

> **Explanation:** Bootstrap divides the page into 12 columns. `col-6` = 50% width, `col-4` = 33.3%, `col-3` = 25%.

---

## Q9. Which Bootstrap class creates a blue button?

- A) btn-blue
- B) btn-primary ✅
- C) button-blue
- D) btn-info

> **Explanation:** `btn-primary` creates a blue button. Bootstrap uses color names: primary (blue), success (green), danger (red).

---

## Q10. What does "col-md-6" mean in Bootstrap?

- A) 6px margin on medium screens
- B) 6 columns wide on medium screens and up ✅
- C) 6 items in a row
- D) Medium padding of 6

> **Explanation:** `col-md-6` means take 6 out of 12 columns (50% width) on medium screens (768px) and up.

---

## Q11. Which array method creates a new array by transforming each item?

- A) forEach
- B) filter
- C) map ✅
- D) find

> **Explanation:** `map()` creates a new array by applying a function to each item. `[1,2,3].map(x => x*2)` returns `[2,4,6]`.

---

## Q12. What is the arrow function syntax for: function add(a,b) { return a+b; }?

- A) add = (a,b) -> a+b
- B) const add = (a,b) => a+b ✅
- C) const add = (a,b) >> a+b
- D) add => (a,b) = a+b

> **Explanation:** Arrow functions: `const add = (a, b) => a + b;` Shorter syntax for simple functions.

---

## Answer Key

| Q  | Answer | Q  | Answer |
|----|--------|----|--------|
| 1  | B      | 7  | B      |
| 2  | C      | 8  | C      |
| 3  | C      | 9  | B      |
| 4  | B      | 10 | B      |
| 5  | B      | 11 | C      |
| 6  | A      | 12 | B      |
