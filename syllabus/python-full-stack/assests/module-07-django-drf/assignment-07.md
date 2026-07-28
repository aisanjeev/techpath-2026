# Module 07 — Assignment: Django & DRF Full Stack API

**Deadline:** End of module week
**Submission:** Django project folder + Postman/Swagger screenshots

---

## Build: TechPath Institute Student Portal API

Create a complete Django + DRF application for managing students, courses, and attendance at TechPath Institute, Bhopal.

### Task 1: Django Project Setup & Models — 25 marks

**Setup:**
- Create a Django project called `institute` with an app called `students`
- Configure SQLite database (default)
- Create a superuser for the admin panel

**Models:**

| Model | Fields |
|-------|--------|
| `Course` | name, duration_months, fee (Decimal), is_active, created_at |
| `Student` | name, email (unique), phone, city (choices: Bhopal/Delhi/Pune/Indore/Mumbai), gender, course (FK), marks (0-100), enrolled_on |
| `Attendance` | student (FK), date, is_present (bool), unique_together on student+date |

**Requirements:**
- All models must have `__str__` methods
- Add validators for marks (0-100)
- Use `auto_now_add` for dates
- Run migrations successfully

### Task 2: Admin Panel Customization — 15 marks

- Register all models in admin
- `StudentAdmin`: list_display (name, email, course, city, marks), list_filter (course, city), search_fields (name, email), list_editable (marks), list_per_page=20
- `CourseAdmin`: show student count in list_display
- Add a custom admin action: "Mark selected students as passed" (set marks to 40 if below 40)
- Screenshot the admin panel with at least 10 students

### Task 3: DRF Serializers & ViewSets — 30 marks

**Serializers:**
- `StudentSerializer` — all fields + computed `course_name` (read-only) + `status` (Pass/Fail)
- `CourseSerializer` — all fields + annotated `student_count`
- Validate marks (0-100) in serializer

**ViewSets:**
- `StudentViewSet` (ModelViewSet):
  - Filtering: by course, city, gender (django-filter)
  - Search: by name, email
  - Ordering: by name, marks, enrolled_on
  - Pagination: 10 per page
  - Custom action: `stats` — returns total, average marks, pass/fail count, city distribution
  - Custom action: `toppers` — returns top 5 students by marks

- `CourseViewSet` (ModelViewSet):
  - Search by name
  - Include student count

**Endpoints (via DefaultRouter):**

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/students/` | List students (paginated, filterable) |
| POST | `/api/students/` | Create student |
| GET | `/api/students/{id}/` | Get student detail |
| PUT | `/api/students/{id}/` | Full update |
| PATCH | `/api/students/{id}/` | Partial update |
| DELETE | `/api/students/{id}/` | Delete |
| GET | `/api/students/stats/` | Aggregate stats |
| GET | `/api/students/toppers/` | Top 5 students |
| GET | `/api/courses/` | List courses |
| POST | `/api/courses/` | Create course |

### Task 4: Authentication & Permissions — 30 marks

- Install and configure `djangorestframework-simplejwt`
- Add token endpoints: `/api/token/` and `/api/token/refresh/`
- Permissions:
  - List/Retrieve students: Anyone (AllowAny)
  - Create/Update/Delete students: Authenticated only (IsAuthenticated)
  - Stats and toppers: Anyone
- Test auth flow:
  1. Get token with POST `/api/token/` (username + password)
  2. Use token in header: `Authorization: Bearer <token>`
  3. Try create without token (should get 401)
  4. Try create with token (should succeed)
- Add throttling: 50/hour for anonymous, 200/hour for authenticated

**Submit screenshots of:**
- Token obtain request/response
- Authenticated POST creating a student
- Unauthenticated POST getting 401
- Throttle headers in response

---

## Project Structure

```
institute/
├── manage.py
├── requirements.txt
├── institute/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
└── students/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Models | All 3 models, validators, meta, str | 2 models work | Only 1 model |
| Admin | Full customization, actions | Basic registration | Just registered |
| DRF CRUD | All endpoints work, filters, search | Most endpoints | Only list works |
| Auth | JWT working, permissions per-action | Token works | No auth |
| Stats | Both custom actions return correct data | Stats works | No custom actions |
| Code Quality | Clean, commented, organized | Mostly clean | Messy, no comments |
