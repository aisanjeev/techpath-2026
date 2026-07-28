"""
=============================================================================
TechPath Institute — Python DSA Interview Practice
=============================================================================
This file contains 15 common interview problems with solutions.
All examples use Indian context (names, cities, prices in INR).

How to use:
  1. Try solving each problem yourself first (cover the solution!)
  2. Run this file: python code-interview-dsa-practice.py
  3. Check if your output matches the expected output
  4. Practice until you can solve each problem in under 10 minutes

Difficulty: Easy (suitable for fresher interviews)
Topics: Arrays, Strings, Dictionaries, Sorting, Searching, Stacks
=============================================================================
"""


# =============================================================================
# PROBLEM 1: Two Sum
# Given a list of prices and a budget, find two items that exactly match the budget.
# =============================================================================

def two_sum(prices: list[int], budget: int) -> list[int]:
    """
    Find indices of two items whose prices add up to the budget.

    Uses a hashmap for O(n) time complexity.

    >>> two_sum([120, 350, 80, 200, 150], 500)
    [1, 3]
    """
    seen = {}  # price -> index
    for i, price in enumerate(prices):
        complement = budget - price
        if complement in seen:
            return [seen[complement], i]
        seen[price] = i
    return []


# Test
print("=" * 60)
print("PROBLEM 1: Two Sum")
prices = [120, 350, 80, 200, 150]
budget = 500
result = two_sum(prices, budget)
print(f"Prices: {prices}")
print(f"Budget: ₹{budget}")
print(f"Items at indices {result}: ₹{prices[result[0]]} + ₹{prices[result[1]]} = ₹{budget}")
# Expected: [1, 3] — ₹350 + ₹200 = ₹500


# =============================================================================
# PROBLEM 2: Reverse a String
# =============================================================================

def reverse_string(s: str) -> str:
    """
    Reverse a string using slicing.

    >>> reverse_string("TechPath")
    'htaPceT'
    """
    return s[::-1]


print("\n" + "=" * 60)
print("PROBLEM 2: Reverse String")
print(reverse_string("TechPath"))    # htaPceT
print(reverse_string("Bhopal"))      # lapohB
print(reverse_string("Python"))      # nohtyP


# =============================================================================
# PROBLEM 3: Check Palindrome
# =============================================================================

def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome (reads same forwards and backwards).
    Ignores case and spaces.

    >>> is_palindrome("madam")
    True
    >>> is_palindrome("Rahul")
    False
    """
    s = s.lower().replace(" ", "")
    return s == s[::-1]


print("\n" + "=" * 60)
print("PROBLEM 3: Palindrome Check")
test_words = ["madam", "Rahul", "racecar", "naman", "Python"]
for word in test_words:
    print(f"  '{word}' is palindrome: {is_palindrome(word)}")
# Expected: True, False, True, True, False


# =============================================================================
# PROBLEM 4: Find Most Frequent Element
# =============================================================================

def most_frequent(items: list) -> tuple:
    """
    Find the most frequent element and its count.

    >>> most_frequent(["Bhopal", "Pune", "Delhi", "Bhopal", "Pune", "Bhopal"])
    ('Bhopal', 3)
    """
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    max_item = max(freq, key=freq.get)
    return max_item, freq[max_item]


print("\n" + "=" * 60)
print("PROBLEM 4: Most Frequent Element")
cities = ["Bhopal", "Pune", "Delhi", "Bhopal", "Pune", "Bhopal", "Delhi"]
city, count = most_frequent(cities)
print(f"Cities: {cities}")
print(f"Most frequent: {city} (appears {count} times)")
# Expected: Bhopal (3 times)


# =============================================================================
# PROBLEM 5: FizzBuzz
# Classic interview question — every fresher should know this.
# =============================================================================

def fizzbuzz(n: int) -> list[str]:
    """
    For numbers 1 to n:
    - Divisible by 3 and 5: "FizzBuzz"
    - Divisible by 3 only: "Fizz"
    - Divisible by 5 only: "Buzz"
    - Otherwise: the number itself

    >>> fizzbuzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    """
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


print("\n" + "=" * 60)
print("PROBLEM 5: FizzBuzz (1-20)")
print(fizzbuzz(20))


# =============================================================================
# PROBLEM 6: Remove Duplicates
# =============================================================================

def remove_duplicates(items: list) -> list:
    """
    Remove duplicates while preserving order.

    >>> remove_duplicates([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
    [3, 1, 4, 5, 9, 2, 6]
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


print("\n" + "=" * 60)
print("PROBLEM 6: Remove Duplicates")
student_ids = [101, 102, 103, 101, 104, 102, 105, 103]
print(f"Original: {student_ids}")
print(f"Unique:   {remove_duplicates(student_ids)}")
# Expected: [101, 102, 103, 104, 105]


# =============================================================================
# PROBLEM 7: Anagram Check
# Two words are anagrams if they have the same letters in different order.
# =============================================================================

def are_anagrams(word1: str, word2: str) -> bool:
    """
    Check if two words are anagrams.

    >>> are_anagrams("listen", "silent")
    True
    >>> are_anagrams("hello", "world")
    False
    """
    return sorted(word1.lower()) == sorted(word2.lower())


print("\n" + "=" * 60)
print("PROBLEM 7: Anagram Check")
pairs = [("listen", "silent"), ("hello", "world"), ("race", "care"), ("python", "typhon")]
for w1, w2 in pairs:
    print(f"  '{w1}' and '{w2}': {are_anagrams(w1, w2)}")
# Expected: True, False, True, True


# =============================================================================
# PROBLEM 8: Find Missing Number
# Given numbers 1 to n with one missing, find the missing number.
# =============================================================================

def find_missing(nums: list[int], n: int) -> int:
    """
    Find the missing number in a sequence from 1 to n.
    Uses the mathematical formula: sum(1 to n) = n*(n+1)/2

    >>> find_missing([1, 2, 4, 5, 6], 6)
    3
    """
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum


print("\n" + "=" * 60)
print("PROBLEM 8: Missing Number")
roll_numbers = [1, 2, 3, 4, 6, 7, 8, 9, 10]  # Roll number 5 is missing
print(f"Roll numbers: {roll_numbers}")
print(f"Missing: {find_missing(roll_numbers, 10)}")
# Expected: 5


# =============================================================================
# PROBLEM 9: Valid Brackets
# Check if brackets in a string are balanced.
# =============================================================================

def is_valid_brackets(s: str) -> bool:
    """
    Check if brackets are properly balanced.

    >>> is_valid_brackets("({[]})")
    True
    >>> is_valid_brackets("({[}])")
    False
    """
    stack = []
    bracket_map = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()

    return len(stack) == 0


print("\n" + "=" * 60)
print("PROBLEM 9: Valid Brackets")
test_cases = ["({[]})", "({[}])", "()", "((()))", "(((", ""]
for tc in test_cases:
    print(f"  '{tc}': {is_valid_brackets(tc)}")
# Expected: True, False, True, True, False, True


# =============================================================================
# PROBLEM 10: Binary Search
# =============================================================================

def binary_search(arr: list[int], target: int) -> int:
    """
    Find the index of target in a sorted list. Returns -1 if not found.
    Time complexity: O(log n) — much faster than linear search for large lists.

    >>> binary_search([10, 20, 30, 40, 50, 60], 30)
    2
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


print("\n" + "=" * 60)
print("PROBLEM 10: Binary Search")
sorted_fees = [5000, 8000, 12000, 15000, 20000, 25000, 30000]
target_fee = 15000
idx = binary_search(sorted_fees, target_fee)
print(f"Fees: {sorted_fees}")
print(f"Looking for ₹{target_fee}: found at index {idx}")
# Expected: index 3


# =============================================================================
# PROBLEM 11: Count Words in a Sentence
# =============================================================================

def word_frequency(sentence: str) -> dict:
    """
    Count the frequency of each word in a sentence.

    >>> word_frequency("the cat sat on the mat the cat")
    {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}
    """
    words = sentence.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


print("\n" + "=" * 60)
print("PROBLEM 11: Word Frequency")
text = "Python is great Python is simple Python is powerful"
freq = word_frequency(text)
for word, count in freq.items():
    print(f"  '{word}': {count}")


# =============================================================================
# PROBLEM 12: Maximum Subarray Sum (Kadane's Algorithm)
# =============================================================================

def max_subarray_sum(nums: list[int]) -> int:
    """
    Find the maximum sum of a contiguous subarray.
    Uses Kadane's algorithm — O(n) time.

    >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    """
    max_sum = nums[0]
    current_sum = nums[0]

    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)

    return max_sum


print("\n" + "=" * 60)
print("PROBLEM 12: Maximum Subarray Sum")
# Monthly profit/loss for a small shop in Bhopal (in thousands ₹)
monthly_pl = [-5, 10, -3, 20, -8, 15, 5, -12, 8]
print(f"Monthly P&L (₹K): {monthly_pl}")
print(f"Best consecutive months sum: ₹{max_subarray_sum(monthly_pl)}K")
# Best streak: [10, -3, 20, -8, 15, 5] = 39K


# =============================================================================
# PROBLEM 13: Flatten a Nested List
# =============================================================================

def flatten(nested: list) -> list:
    """
    Flatten a nested list into a single list.

    >>> flatten([1, [2, 3], [4, [5, 6]]])
    [1, 2, 3, 4, 5, 6]
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


print("\n" + "=" * 60)
print("PROBLEM 13: Flatten Nested List")
nested = [["Rahul", "Priya"], ["Ananya", ["Vikram", "Neha"]], "Arjun"]
print(f"Nested:    {nested}")
print(f"Flattened: {flatten(nested)}")


# =============================================================================
# PROBLEM 14: Sort Students by Score
# =============================================================================

def sort_students(students: list[dict]) -> list[dict]:
    """
    Sort students by score in descending order.
    If scores are equal, sort by name alphabetically.

    Uses Python's built-in sorted() with a custom key.
    """
    return sorted(students, key=lambda s: (-s["score"], s["name"]))


print("\n" + "=" * 60)
print("PROBLEM 14: Sort Students by Score")
students = [
    {"name": "Rahul", "score": 85, "city": "Bhopal"},
    {"name": "Priya", "score": 92, "city": "Pune"},
    {"name": "Ananya", "score": 85, "city": "Delhi"},
    {"name": "Vikram", "score": 78, "city": "Jaipur"},
    {"name": "Neha", "score": 92, "city": "Hyderabad"},
]
for s in sort_students(students):
    print(f"  {s['name']:10} — {s['score']} marks ({s['city']})")
# Expected order: Neha 92, Priya 92, Ananya 85, Rahul 85, Vikram 78


# =============================================================================
# PROBLEM 15: Group Students by City
# =============================================================================

def group_by_city(students: list[dict]) -> dict:
    """
    Group students by their city.

    >>> group_by_city([{"name": "A", "city": "X"}, {"name": "B", "city": "X"}])
    {'X': ['A', 'B']}
    """
    groups = {}
    for student in students:
        city = student["city"]
        if city not in groups:
            groups[city] = []
        groups[city].append(student["name"])
    return groups


print("\n" + "=" * 60)
print("PROBLEM 15: Group Students by City")
all_students = [
    {"name": "Rahul", "city": "Bhopal"},
    {"name": "Priya", "city": "Pune"},
    {"name": "Ananya", "city": "Delhi"},
    {"name": "Vikram", "city": "Bhopal"},
    {"name": "Neha", "city": "Pune"},
    {"name": "Arjun", "city": "Bhopal"},
]
groups = group_by_city(all_students)
for city, names in groups.items():
    print(f"  {city}: {', '.join(names)}")
# Expected:
# Bhopal: Rahul, Vikram, Arjun
# Pune: Priya, Neha
# Delhi: Ananya


# =============================================================================
print("\n" + "=" * 60)
print("ALL 15 PROBLEMS COMPLETED!")
print("Practice these daily until you can solve each one from memory.")
print("Target: solve each problem in under 10 minutes during an interview.")
print("=" * 60)
