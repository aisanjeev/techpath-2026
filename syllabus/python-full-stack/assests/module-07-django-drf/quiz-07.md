# Quiz: Django & Django REST Framework

**Module 07 | 15 Questions | Pass Mark: 60%**
**TechPath Institute | Python Full Stack Course**

---

## Q1. In Django's MVT architecture, which component is responsible for handling business logic and returning a response?

- A) Model
- B) View ✅
- C) Template
- D) URL Conf

> **Explanation:** In Django's MVT pattern, the View handles business logic — it receives the request, interacts with the Model for data, and returns a response (often rendered through a Template). This is different from MVC where the Controller handles logic.

---

## Q2. What does the command `python manage.py makemigrations` do?

- A) Applies pending migrations to the database
- B) Creates the database tables directly
- C) Generates migration files based on model changes ✅
- D) Deletes all migration history

> **Explanation:** `makemigrations` looks at your model changes and creates migration files (Python scripts) describing those changes. It does NOT touch the database — you need `migrate` to actually apply them.

---

## Q3. Which model field would you use to store a student's fee amount like ₹15,499.50 where exact precision matters?

- A) FloatField()
- B) IntegerField()
- C) DecimalField(max_digits=8, decimal_places=2) ✅
- D) CharField(max_length=10)

> **Explanation:** DecimalField stores exact decimal numbers, which is important for money. FloatField uses floating-point math and can introduce tiny rounding errors (e.g., ₹15,499.50 might become ₹15,499.4999...). Always use DecimalField for financial values.

---

## Q4. What is the difference between `Student.objects.filter(city='Mumbai')` and `Student.objects.get(city='Mumbai')`?

- A) filter() returns one object; get() returns a QuerySet
- B) filter() returns a QuerySet (0 or more); get() returns exactly one object or raises an error ✅
- C) Both return the same result but filter() is faster
- D) get() works only with primary keys; filter() works with any field

> **Explanation:** filter() always returns a QuerySet (which can be empty or contain multiple objects). get() returns exactly one object — it raises DoesNotExist if no match is found and MultipleObjectsReturned if more than one match exists.

---

## Q5. You have a Student model with a ForeignKey to Course. Which QuerySet method reduces the number of database queries when accessing `student.course.name` for many students?

- A) Student.objects.prefetch_related('course')
- B) Student.objects.select_related('course') ✅
- C) Student.objects.values('course__name')
- D) Student.objects.annotate(course_name=F('course__name'))

> **Explanation:** select_related() performs a SQL JOIN for ForeignKey and OneToOneField relationships, fetching the related object in the same query. prefetch_related() is used for ManyToManyField and reverse ForeignKey relations where a JOIN is not possible.

---

## Q6. How do you register a model so it appears in the Django Admin panel?

- A) Add the model name to INSTALLED_APPS in settings.py
- B) Use admin.site.register(ModelName) in admin.py ✅
- C) Create a template file for the model
- D) Run python manage.py registermodel ModelName

> **Explanation:** You register models in the app's admin.py file using admin.site.register(ModelName). You can also use the @admin.register(ModelName) decorator with a custom ModelAdmin class to customize the admin interface.

---

## Q7. In Django, what is the purpose of the `{% csrf_token %}` tag inside a form template?

- A) It adds form validation for required fields
- B) It encrypts the form data before sending
- C) It protects against Cross-Site Request Forgery attacks by adding a hidden token ✅
- D) It enables file uploads in the form

> **Explanation:** {% csrf_token %} inserts a hidden input field with a unique token. When the form is submitted, Django checks that this token matches the one stored in the user's session. This prevents malicious websites from submitting forms on behalf of your users.

---

## Q8. Which Django class-based view would you use to show a paginated list of all courses?

- A) DetailView
- B) CreateView
- C) ListView ✅
- D) TemplateView

> **Explanation:** ListView is designed to display a list of objects from a model. It supports pagination through the paginate_by attribute. DetailView is for showing a single object, CreateView is for forms, and TemplateView renders a static template.

---

## Q9. In DRF, what does a ModelSerializer automatically generate?

- A) Database migrations
- B) URL patterns for the API
- C) Fields and validation rules based on the model definition ✅
- D) HTML templates for the browsable API

> **Explanation:** ModelSerializer reads your model's fields and automatically creates corresponding serializer fields with the right types and validation (e.g., max_length from CharField, required from blank/null settings). You just specify the model and fields in the Meta class.

---

## Q10. A DRF ModelViewSet with a DefaultRouter automatically provides endpoints for which actions?

- A) Only list and create
- B) Only list, create, and retrieve
- C) List, create, retrieve, update, partial_update, and destroy ✅
- D) Only retrieve and update

> **Explanation:** ModelViewSet inherits from all the mixins: ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, and DestroyModelMixin. Combined with a DefaultRouter, it generates all six standard REST endpoints (GET list, POST create, GET detail, PUT update, PATCH partial update, DELETE destroy).

---

## Q11. What is the difference between Token Authentication and JWT Authentication in DRF?

- A) Token auth is stored in the database; JWT is a self-contained token that does not need a database lookup ✅
- B) JWT must be stored in the database; Token auth is self-contained
- C) There is no difference — both work the same way
- D) Token auth uses cookies; JWT uses headers

> **Explanation:** DRF's built-in TokenAuthentication stores tokens in a database table and looks them up on every request. JWT (JSON Web Token) is self-contained — the server signs it with a secret key, and it can be verified without a database query. JWTs also have built-in expiration.

---

## Q12. Which DRF permission class allows anyone to read data (GET requests) but requires login for write operations (POST, PUT, DELETE)?

- A) IsAuthenticated
- B) AllowAny
- C) IsAdminUser
- D) IsAuthenticatedOrReadOnly ✅

> **Explanation:** IsAuthenticatedOrReadOnly allows unauthenticated users to make safe (read-only) requests like GET and HEAD. Any request that would modify data (POST, PUT, PATCH, DELETE) requires the user to be authenticated.

---

## Q13. What problem does Django Channels solve that regular Django cannot handle?

- A) Serving static files like CSS and JavaScript
- B) Handling real-time, bidirectional communication using WebSockets ✅
- C) Generating database migrations automatically
- D) Sending emails to users

> **Explanation:** Regular Django uses HTTP, which is request-response only — the server cannot push data to the client without being asked. Django Channels adds support for WebSockets and other long-lived connections, enabling real-time features like live chat, notifications, and live updates.

---

## Q14. In Celery, what does calling `send_welcome_email.delay(student_id=42)` do?

- A) Runs the function immediately and blocks until it finishes
- B) Schedules the function to run at a future date
- C) Sends the task to a message broker (like Redis) to be executed asynchronously by a worker ✅
- D) Deletes the task from the queue

> **Explanation:** The .delay() method sends the task to the message broker (e.g., Redis). A separate Celery worker process picks it up and executes it in the background. This means your web request returns immediately without waiting for the task to finish — useful for slow operations like sending emails.

---

## Q15. A DRF API returns status code 201. What does this mean?

- A) The request was successful but there is no content to return
- B) The server encountered an internal error
- C) A new resource was successfully created ✅
- D) The user is not authorized to access this resource

> **Explanation:** HTTP 201 Created means a new resource was successfully created on the server. This is typically returned after a successful POST request. Compare with 200 (OK — general success), 204 (No Content — success but nothing to return, common for DELETE), and 401 (Unauthorized).

---

*TechPath Institute — Module 07 Quiz*
