# Quiz: Advanced Python

**Module 02 | 15 Questions | Pass Mark: 60%**

---

## Q1. What is the purpose of __init__ in a Python class?

- A) To destroy the object
- B) To initialize the object's attributes when it is created ✅
- C) To print the object's details
- D) To import the class

> **Explanation:** __init__ is the constructor method that runs automatically when you create a new object. It sets up the initial state (attributes) of the object.

---

## Q2. What does super().__init__() do inside a child class?

- A) Creates a new parent object
- B) Calls the parent class's constructor to initialize inherited attributes ✅
- C) Deletes the parent class
- D) Makes the child class abstract

> **Explanation:** super().__init__() calls the parent class's constructor, which initializes the attributes defined in the parent's __init__. This avoids duplicating the parent's initialization code.

---

## Q3. Which decorator makes a method accessible without creating an instance of the class?

- A) @property
- B) @classmethod
- C) @staticmethod ✅
- D) @abstractmethod

> **Explanation:** @staticmethod makes a method that can be called on the class directly (e.g., MathUtils.is_even(4)) without needing an instance. It receives neither self nor cls.

---

## Q4. What does map(lambda x: x * 2, [1, 2, 3]) return when wrapped in list()?

- A) [1, 2, 3, 1, 2, 3]
- B) [2, 4, 6] ✅
- C) [1, 4, 9]
- D) 12

> **Explanation:** map() applies the lambda function (multiply by 2) to each item: 1*2=2, 2*2=4, 3*2=6. Result: [2, 4, 6].

---

## Q5. What is the key difference between a generator function and a regular function?

- A) Generators are faster
- B) Generators use yield instead of return and produce values lazily ✅
- C) Generators can only return integers
- D) Generators cannot accept arguments

> **Explanation:** A generator function uses yield to produce values one at a time (lazy evaluation) instead of returning all values at once. This saves memory because values are generated on demand.

---

## Q6. What is a decorator in Python?

- A) A function that deletes another function
- B) A function that adds behavior to another function without modifying it ✅
- C) A way to create classes
- D) A type of loop

> **Explanation:** A decorator is a function that wraps another function to add extra behavior (like logging, timing, or access control) without changing the original function's code.

---

## Q7. What does @functools.wraps(func) do inside a decorator?

- A) Makes the function run faster
- B) Preserves the original function's name and docstring ✅
- C) Makes the function async
- D) Adds error handling

> **Explanation:** @wraps(func) copies the original function's __name__, __doc__, and other attributes to the wrapper function. Without it, the decorated function would lose its identity.

---

## Q8. What is the output of: list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))?

- A) [1, 3, 5]
- B) [2, 4] ✅
- C) [1, 2, 3, 4, 5]
- D) [False, True, False, True, False]

> **Explanation:** filter() keeps only items where the function returns True. The lambda checks if x is even (x % 2 == 0), so only 2 and 4 pass the filter.

---

## Q9. What keyword makes a Python function asynchronous?

- A) yield
- B) await
- C) async ✅
- D) concurrent

> **Explanation:** The 'async' keyword before 'def' makes a function asynchronous (a coroutine). 'await' is used inside async functions to wait for other async operations.

---

## Q10. What does asyncio.gather() do?

- A) Runs tasks one after another
- B) Runs multiple async tasks concurrently and waits for all to complete ✅
- C) Cancels all running tasks
- D) Creates a new event loop

> **Explanation:** asyncio.gather() runs multiple coroutines concurrently (not sequentially) and returns their results once all have completed. This is much faster than awaiting them one by one.

---

## Q11. What does Pydantic do that a regular dataclass does not?

- A) Generate __init__ automatically
- B) Validate data types and convert values automatically ✅
- C) Make attributes immutable
- D) Add methods to the class

> **Explanation:** Pydantic validates that data matches the expected types and automatically converts compatible types (e.g., string '22' to int 22). Dataclasses only structure data without validation.

---

## Q12. What is the purpose of @pytest.mark.parametrize?

- A) To skip a test
- B) To run the same test function with multiple different inputs ✅
- C) To mock a function
- D) To measure test performance

> **Explanation:** @pytest.mark.parametrize lets you run the same test function with different sets of inputs and expected outputs, generating a separate test case for each combination.

---

## Q13. What does the yield keyword do inside a pytest fixture?

- A) Returns multiple test results
- B) Separates setup code (before yield) from teardown code (after yield) ✅
- C) Skips the test
- D) Creates a generator test

> **Explanation:** In a pytest fixture, yield separates setup from teardown. Code before yield runs as setup, yield provides the fixture value, and code after yield runs as cleanup after the test completes.

---

## Q14. What is the MRO (Method Resolution Order) in Python?

- A) The order in which methods are defined in a class
- B) The order Python searches for a method in the class hierarchy (from child to parent) ✅
- C) The order in which objects are created
- D) The order of arguments in a function

> **Explanation:** MRO determines the order Python looks up methods when a class has multiple parent classes. It follows C3 Linearization: child first, then left-to-right through parents.

---

## Q15. Which of the following correctly creates a frozen (immutable) dataclass?

- A) @dataclass(immutable=True)
- B) @dataclass(frozen=True) ✅
- C) @dataclass(readonly=True)
- D) @dataclass(const=True)

> **Explanation:** @dataclass(frozen=True) creates an immutable dataclass where attributes cannot be modified after creation. Any attempt to change an attribute raises a FrozenInstanceError.
