# Product Requirements Document: [Your Product Name]

> **Instructions for TechPath students:**
> Replace all `[bracketed text]` with your own content.
> Delete these instruction blocks before submitting.
> This is a living document — update it as requirements change.

---

## 1. Overview

**Product Name:** [e.g., SmartAttend — Student Attendance Management System]

**One-line Description:** [e.g., A web app for trainers to mark attendance and for students to track their attendance percentage in real-time]

**Version:** 1.0

**Author:** [Your Name]

**Date:** [Today's Date]

**Status:** Draft | In Review | Approved

---

## 2. Problem Statement

### What problem are we solving?

[Describe the pain point. Be specific.]

> **Example:**
> At TechPath Institute, Bhopal, attendance is currently tracked on paper registers.
> This causes problems:
> - Trainers waste 10 minutes per class taking attendance
> - Students don't know their attendance percentage until exam time
> - Admin staff manually calculates percentages in Excel every month
> - Paper registers get lost or damaged
> - There is no way to send alerts to students with low attendance

### Who has this problem?

| Stakeholder | Pain Point |
|-------------|-----------|
| [Trainers] | [Wasting class time on paper attendance] |
| [Students] | [Not knowing their attendance % until too late] |
| [Admin] | [Manual Excel calculations every month] |
| [Parents] | [No visibility into child's attendance] |

---

## 3. Target Users

### Primary Users
- **[Role]:** [Description, approximate count]
  - Example: Trainers at TechPath Institute (5-10 trainers)
  - Example: Students enrolled in courses (100-200 students)

### Secondary Users
- **[Role]:** [Description]
  - Example: Institute admin staff (2-3 people)

### User Personas

#### Persona 1: [Name]
- **Name:** Amit Kumar (Trainer)
- **Age:** 32
- **Tech Comfort:** Moderate — uses phone apps, comfortable with web browsers
- **Goal:** Mark attendance for 30 students in under 2 minutes
- **Frustration:** Paper registers are slow and messy

#### Persona 2: [Name]
- **Name:** Priya Patel (Student)
- **Age:** 21
- **Tech Comfort:** High — uses apps daily
- **Goal:** Check her attendance anytime from her phone
- **Frustration:** Finds out about low attendance only during exam registration

---

## 4. User Stories

Write user stories in this format:
**As a [user type], I want to [action] so that [benefit].**

### Must Have (MVP — Minimum Viable Product)

| ID | User Story | Priority |
|----|-----------|----------|
| US-01 | As a trainer, I want to mark attendance for my batch so that records are digital | Must Have |
| US-02 | As a student, I want to view my attendance percentage so that I can track my eligibility | Must Have |
| US-03 | As an admin, I want to log in securely so that only authorized users access the system | Must Have |
| US-04 | [Your user story] | Must Have |
| US-05 | [Your user story] | Must Have |

### Should Have

| ID | User Story | Priority |
|----|-----------|----------|
| US-06 | As an admin, I want to download attendance reports as Excel files so that I can share with management | Should Have |
| US-07 | As a trainer, I want to edit past attendance if I made a mistake so that records are accurate | Should Have |
| US-08 | [Your user story] | Should Have |

### Could Have

| ID | User Story | Priority |
|----|-----------|----------|
| US-09 | As a student, I want to receive a notification when my attendance drops below 75% | Could Have |
| US-10 | As an admin, I want an AI chatbot that answers questions about attendance data | Could Have |

### Won't Have (This Version)

| ID | Feature | Reason |
|----|---------|--------|
| US-11 | Mobile app (Android/iOS) | Web app is enough for v1, mobile app in v2 |
| US-12 | Biometric attendance (fingerprint) | Requires hardware, out of budget |

---

## 5. Functional Requirements

| ID | Feature | Description | User Story |
|----|---------|-------------|------------|
| FR-01 | User Registration | Admin can create student and trainer accounts | US-03 |
| FR-02 | Login / Logout | Email + password authentication with JWT tokens | US-03 |
| FR-03 | Mark Attendance | Trainer selects batch, sees student list, marks present/absent | US-01 |
| FR-04 | View Attendance | Student sees their attendance calendar and percentage | US-02 |
| FR-05 | Attendance Report | Admin can filter by batch, month, and download as Excel | US-06 |
| FR-06 | [Your feature] | [Description] | [US-XX] |

---

## 6. Non-Functional Requirements

| Category | Requirement | Target |
|----------|------------|--------|
| Performance | Page load time | Under 2 seconds on 3G connection |
| Performance | API response time | Under 500ms for all endpoints |
| Security | Passwords | Hashed with bcrypt, minimum 8 characters |
| Security | API | JWT tokens with 60-minute expiry |
| Security | Data | HTTPS enforced in production |
| Availability | Uptime | 99.5% (approx. 3.6 hours downtime per month) |
| Scalability | Users | Support up to 500 concurrent users |
| Compatibility | Browsers | Chrome 90+, Firefox 90+, Safari 14+, Edge 90+ |
| Compatibility | Devices | Responsive — works on mobile, tablet, desktop |
| Accessibility | Standards | WCAG 2.1 Level A (basic accessibility) |

---

## 7. Acceptance Criteria

### US-01: Trainer marks attendance

```
GIVEN the trainer is logged in and has selected a batch
WHEN they see the student list for today's date
THEN they can mark each student as Present, Absent, or Late
AND they can submit all attendance in one click
AND they see a success message with the count marked
AND they cannot mark attendance for a future date
```

### US-02: Student views attendance

```
GIVEN the student is logged in
WHEN they open the attendance page
THEN they see a calendar view with colored dots (green=present, red=absent)
AND they see their total percentage at the top
AND they can filter by month
AND the page loads within 2 seconds
```

### [Add more acceptance criteria for each user story]

---

## 8. Wireframes / UI Sketches

> Attach hand-drawn or Figma wireframes for key screens:

| Screen | Description |
|--------|-------------|
| Login Page | Email + password form, "Forgot password?" link |
| Trainer Dashboard | Batch selector, date picker, student checklist |
| Student Dashboard | Attendance calendar, percentage counter, recent history |
| Admin Reports | Filters (batch, month), table with export button |

---

## 9. Technical Constraints

| Constraint | Detail |
|-----------|--------|
| Budget | Free tier only (no paid cloud services) |
| Hosting | Azure free tier / Render free tier |
| Database | PostgreSQL (free on Render/Supabase) |
| Timeline | 6 weeks from start to deployment |
| Team Size | 1-2 developers |

---

## 10. Out of Scope

List features that are explicitly NOT in this version:

- Mobile native app (Android/iOS)
- SMS/WhatsApp notifications
- Biometric (fingerprint/face) attendance
- Integration with university ERP systems
- Multi-language support (Hindi, etc.)
- Parent login portal

---

## 11. Success Metrics

How will we know this product is successful?

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Trainer adoption | 80% of trainers use it daily within 2 weeks | Usage analytics |
| Time saved | Attendance marking under 2 minutes (was 10 min) | User feedback |
| Data accuracy | Zero paper-based attendance entries | Admin report |
| Student awareness | 90% of students check their % at least weekly | Login analytics |

---

## 12. Timeline & Milestones

| Week | Milestone | Deliverables |
|------|-----------|-------------|
| Week 1 | Project Setup | Repo, DB schema, auth system, CI/CD pipeline |
| Week 2 | Core Backend | Student CRUD, attendance API, batch management |
| Week 3 | Frontend — Trainer | Mark attendance page, batch selection |
| Week 4 | Frontend — Student | Attendance view, calendar, percentage display |
| Week 5 | AI Feature + Reports | RAG chatbot for attendance queries, Excel export |
| Week 6 | Testing + Deployment | Bug fixes, load testing, deploy to production |

---

## 13. Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| AI API costs exceed free tier | Medium | Medium | Set usage limits, use local models as fallback |
| Students don't adopt the system | Low | High | Make it mobile-friendly, send reminders |
| Security breach (student data leak) | Low | Very High | Follow security checklist, HTTPS, input validation |
| Database migration breaks prod | Medium | High | Always backup before migrating, test on staging first |

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Owner | [Name] | [Date] | Pending |
| Tech Lead | [Name] | [Date] | Pending |
| Instructor | [Name] | [Date] | Pending |

---

*This PRD was created using the TechPath Institute PRD template.*
*Last updated: [Date]*
