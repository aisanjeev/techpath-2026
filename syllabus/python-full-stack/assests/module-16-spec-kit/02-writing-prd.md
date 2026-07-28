# Writing a Product Requirements Document (PRD)

**Module 16 -- Spec-Kit Development Methodology | Topic 2**

---

## What is a PRD?

A Product Requirements Document (PRD) is a written description of what a product should do. It answers the most fundamental question in software development: **"What are we building and why?"**

Think of a PRD like a restaurant menu. The menu does not tell the chef how to cook each dish (that is the recipe). Instead, it tells the chef what dishes the restaurant offers and what each dish should contain. The PRD is the menu; the code is the recipe.

A good PRD ensures that everyone on the team -- developers, designers, testers, and stakeholders -- shares the same understanding of what the product should do.

---

## Sections of a PRD

Every PRD follows a standard structure. Here are the key sections:

### 1. Problem Statement

This section explains the problem you are solving. It should be specific and grounded in reality.

**Bad example:** "People need a better app."

**Good example:** "Small coaching institutes in Bhopal with 50-200 students manage attendance using paper registers. This leads to errors, lost records, and inability to generate monthly reports for parents."

### 2. Target Users

Who will use this product? Define your users clearly.

| User Type | Description | Key Need |
|-----------|------------|----------|
| Institute Admin | Manages the coaching center | View reports, manage batches |
| Teacher | Takes attendance daily | Quick, mobile-friendly attendance |
| Parent | Checks child's attendance | Monthly attendance summary via SMS |

### 3. User Stories

User stories describe features from the user's perspective. They follow a simple template:

```
As a [type of user], I want to [do something], so that [I get some benefit].
```

**Examples:**

- As a **teacher**, I want to **mark attendance for my batch in under 2 minutes**, so that **I do not waste class time**.
- As an **admin**, I want to **see a monthly attendance report for any student**, so that **I can share it with parents**.
- As a **parent**, I want to **receive an SMS if my child is absent**, so that **I am aware immediately**.

### 4. Acceptance Criteria

Acceptance criteria define when a user story is "done." They are the specific, testable conditions that must be true for the feature to be accepted.

For the teacher attendance story above:

- The teacher can see a list of students in the selected batch
- Each student has a Present/Absent toggle
- The teacher can submit attendance with one button click
- Submission takes less than 3 seconds
- A success message appears after submission
- Attendance cannot be submitted twice for the same batch on the same day

### 5. Out of Scope

This section is just as important as what is in scope. It prevents scope creep -- the tendency for projects to grow beyond their original plan.

**Example Out of Scope items:**
- Fee management (will be built in Phase 2)
- Video lectures or course content
- Integration with government school databases
- Support for multiple languages (English only for MVP)

---

## Gherkin Syntax: Structured Acceptance Criteria

Gherkin is a structured way to write acceptance criteria using three keywords: **Given**, **When**, and **Then**. It reads like plain English but is precise enough to be turned into automated tests.

### The Pattern

```gherkin
Given [some initial context]
When [an action is performed]
Then [an expected outcome occurs]
```

### Examples

**Feature: Mark Attendance**

```gherkin
Scenario: Teacher marks attendance for a batch
  Given the teacher is logged in
  And the teacher has selected batch "Python Morning"
  And today's attendance has not been submitted for this batch
  When the teacher marks 18 students as present and 2 as absent
  And clicks the "Submit Attendance" button
  Then the attendance is saved for today
  And a success message "Attendance submitted successfully" is displayed
  And the submit button becomes disabled for this batch today
```

**Feature: Absent Student Notification**

```gherkin
Scenario: Parent receives SMS for absent child
  Given the student "Ananya Sharma" is enrolled in batch "Python Morning"
  And her parent's mobile number is registered as "9876543210"
  When the teacher marks Ananya as absent
  And submits the attendance
  Then an SMS is sent to 9876543210
  And the SMS contains "Ananya Sharma was marked absent on 25-Jul-2026"
```

### Why Gherkin Matters

| Benefit | Explanation |
|---------|-------------|
| Readable by everyone | Non-technical stakeholders can understand and verify |
| Testable | Can be directly converted to automated tests (BDD) |
| Unambiguous | Forces you to be specific about inputs and outputs |
| Complete | Makes you think about edge cases and preconditions |

---

## Sample PRD: QuickKart -- A Neighborhood Grocery Delivery App

Below is a simplified but realistic PRD for an Indian e-commerce application.

---

### QuickKart PRD

**Version:** 1.0
**Author:** Sneha Kulkarni
**Date:** 25 July 2026
**Status:** Draft

#### 1. Problem Statement

Residents of Arera Colony, Bhopal, currently order groceries by calling local kirana stores or visiting in person. Phone orders are error-prone (wrong items, missed quantities), and store owners have no system to track orders or manage delivery schedules. During monsoon season, footfall drops 40%, hurting store revenue.

#### 2. Target Users

| User | Description | Pain Point |
|------|------------|------------|
| Customer | Residents of Arera Colony, ages 25-55 | Inconvenient to visit store; phone orders have errors |
| Store Owner | 3-5 kirana store owners in the area | Cannot track orders; no delivery management |
| Delivery Person | 2-3 delivery staff per store | No route optimization; paper-based tracking |

#### 3. User Stories

**Customer Stories:**

```
US-01: As a customer, I want to browse products by category (dal, rice, 
       snacks, beverages), so that I can find items quickly.

US-02: As a customer, I want to add items to a cart and place an order, 
       so that I can get groceries delivered to my home.

US-03: As a customer, I want to pay via UPI (PhonePe, Google Pay) or 
       cash on delivery, so that I can choose my preferred payment method.

US-04: As a customer, I want to see estimated delivery time, so that I 
       know when to expect my order.

US-05: As a customer, I want to reorder my previous orders with one tap, 
       so that I save time on weekly staples.
```

**Store Owner Stories:**

```
US-06: As a store owner, I want to see all incoming orders on a dashboard, 
       so that I can manage fulfillment.

US-07: As a store owner, I want to update product prices and availability, 
       so that customers see accurate information.

US-08: As a store owner, I want to see daily/weekly revenue reports, 
       so that I can track my business performance.
```

#### 4. Acceptance Criteria (Selected Stories)

**US-01: Browse Products**

```gherkin
Scenario: Customer browses products by category
  Given the customer has opened the QuickKart app
  When the customer selects the "Dal & Pulses" category
  Then a list of dal products is displayed
  And each product shows name, price per kg, and availability status
  And products marked "Out of Stock" appear at the bottom of the list

Scenario: Customer searches for a specific product
  Given the customer is on the home screen
  When the customer types "Toor Dal" in the search bar
  Then products matching "Toor Dal" appear within 1 second
  And results show brand name, weight options, and price
```

**US-03: Payment via UPI**

```gherkin
Scenario: Customer pays using UPI
  Given the customer has items in the cart totaling Rs 450
  And the customer has selected "UPI" as payment method
  When the customer enters UPI ID "rahul@paytm"
  And clicks "Pay Now"
  Then a payment request is sent to the UPI app
  And the order status shows "Payment Pending"
  And upon successful payment, status changes to "Order Confirmed"
  And the customer receives an order confirmation with order number
```

#### 5. Out of Scope (Version 1.0)

- Multi-city support (Bhopal only for MVP)
- Subscription boxes or recurring orders
- In-app chat between customer and store
- Rating and review system
- Loyalty points or discount coupons
- Integration with accounting software (Tally, Zoho)

#### 6. Success Metrics

| Metric | Target |
|--------|--------|
| Orders per day (per store) | 20+ within 3 months |
| Average order value | Rs 300+ |
| Customer retention (monthly) | 40%+ |
| Order fulfillment time | Under 45 minutes |
| App crash rate | Less than 0.5% |

---

## PRD Template

You can use this template for your own projects:

```markdown
# [Product Name] -- Product Requirements Document

**Version:** [1.0]
**Author:** [Your Name]
**Date:** [DD Month YYYY]
**Status:** [Draft / In Review / Approved]

## 1. Problem Statement
[Describe the problem in 3-5 sentences. Be specific about who has 
the problem and what impact it has.]

## 2. Target Users
[Table with user types, descriptions, and key pain points]

## 3. User Stories
[List user stories in the format: As a [user], I want to [action], 
so that [benefit].]

## 4. Acceptance Criteria
[Gherkin scenarios for the most important user stories]

## 5. Out of Scope
[Bulleted list of features NOT included in this version]

## 6. Success Metrics
[Table of measurable outcomes with target values]

## 7. Dependencies and Assumptions
[List any external services, APIs, or conditions required]

## 8. Timeline
[High-level milestones with dates]
```

---

## Common PRD Mistakes

| Mistake | Why It Is a Problem | How to Fix It |
|---------|-------------------|---------------|
| Too vague | "The app should be fast" -- how fast? | Use specific numbers: "Page loads in under 2 seconds" |
| Too technical | "Use Redis caching with LRU eviction" | The PRD is about WHAT, not HOW |
| No acceptance criteria | Nobody knows when a feature is "done" | Add Gherkin scenarios for every story |
| Missing "out of scope" | Team keeps adding features | Explicitly list what is NOT included |
| Written once, never updated | PRD becomes outdated | Review and update after each sprint |

---

## Key Takeaways

1. A PRD answers "What are we building and why?" -- not "How do we build it?"
2. User stories follow the pattern: As a [user], I want to [action], so that [benefit].
3. Acceptance criteria are testable conditions that define "done."
4. Gherkin syntax (Given/When/Then) makes criteria precise and automatable.
5. Always include an "Out of Scope" section to prevent scope creep.
6. A PRD is a living document -- update it as requirements evolve.

---

*TechPath Institute -- Spec-Kit Development Methodology*
