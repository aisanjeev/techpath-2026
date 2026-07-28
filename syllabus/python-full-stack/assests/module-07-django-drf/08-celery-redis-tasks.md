# Celery & Background Tasks

**Module 07 — Django & Django REST Framework | Topic 8**

---

## Why Do We Need Background Tasks?

Imagine a restaurant in Pune. When a customer places an order, the waiter writes it down and immediately goes back to serve other customers. The waiter does not go into the kitchen and cook the food — that would keep everyone waiting.

In web applications, the same thing happens:

- A user registers on your site. You need to send a welcome email.
- Should the user stare at a loading screen while the email is being sent? No.
- The server should say "Registration successful!" immediately and send the email **in the background**.

**Background tasks** are jobs that happen behind the scenes, without making the user wait.

### Common Background Tasks

| Task | Why Background? |
|------|----------------|
| Sending welcome emails | Email servers can be slow (2-5 seconds) |
| Generating PDF reports | Processing large data takes time |
| Sending bulk SMS to 1000 students | Cannot make the admin wait for all 1000 |
| Resizing uploaded images | Image processing is CPU-heavy |
| Syncing data with external APIs | Third-party APIs can be slow or fail |
| Cleaning up old records | Runs daily, no user interaction needed |

---

## What is Celery?

**Celery** is a task queue for Python. Think of it as a restaurant's order management system:

- **Django (the waiter)** takes the order and drops it on the counter
- **Redis (the order counter)** holds all pending orders in a queue
- **Celery worker (the cook)** picks up orders one by one and processes them
- **Celery beat (the alarm clock)** schedules recurring tasks (like "prepare chai at 4 PM daily")

```
User clicks "Register"
    |
    v
Django view saves user to DB
    |
    v
Django puts "send_welcome_email" task in Redis queue
    |
    v
Django responds: "Registration successful!" (user sees this instantly)
    |
    v
Celery worker picks up the task from Redis
    |
    v
Celery worker sends the email (takes 3 seconds, but user already got the response)
```

---

## What is Redis?

**Redis** is an in-memory data store. In our restaurant analogy, Redis is the order counter where pending orders are placed. Celery uses Redis as a **message broker** — a middleman that holds tasks until a worker picks them up.

Redis is very fast because it stores data in memory (RAM), not on disk.

---

## Installing Celery and Redis

```bash
pip install celery redis
```

Install Redis server:

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# Windows (using Docker)
docker run -p 6379:6379 redis

# Or use WSL on Windows
```

Verify Redis is running:

```bash
redis-cli ping
# Should return: PONG
```

---

## Configuring Celery with Django

### Step 1: Create the Celery App

```python
# myproject/celery.py
import os
from celery import Celery

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Create the Celery app
app = Celery('myproject')

# Load config from Django settings (variables starting with CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
```

### Step 2: Import Celery in `__init__.py`

```python
# myproject/__init__.py
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### Step 3: Add Celery Settings

```python
# settings.py

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'          # Redis as message broker
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'      # Store task results in Redis
CELERY_ACCEPT_CONTENT = ['json']                        # Only accept JSON data
CELERY_TASK_SERIALIZER = 'json'                         # Serialize tasks as JSON
CELERY_RESULT_SERIALIZER = 'json'                       # Serialize results as JSON
CELERY_TIMEZONE = 'Asia/Kolkata'                        # Indian timezone
```

---

## Creating Tasks with `@shared_task`

A **task** is a Python function decorated with `@shared_task`. This decorator tells Celery: "This function can be run in the background."

### Example 1: Sending a Welcome Email

```python
# accounts/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(user_email, user_name):
    """Send a welcome email to a newly registered user."""
    send_mail(
        subject='Welcome to TechPath Institute!',
        message=f'Hi {user_name},\n\n'
                f'Welcome to TechPath Institute, Bhopal! '
                f'Your account has been created successfully.\n\n'
                f'Start your learning journey today.\n\n'
                f'Best regards,\nTeam TechPath',
        from_email='noreply@techpath.biz',
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f'Welcome email sent to {user_email}'
```

### Using the Task in a View

```python
# accounts/views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from .tasks import send_welcome_email

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create user (fast — database operation)
        user = User.objects.create_user(username=username, email=email, password=password)

        # Queue the email task (does NOT wait for email to be sent)
        send_welcome_email.delay(email, username)

        # Respond immediately
        return JsonResponse({
            'success': True,
            'message': f'Welcome, {username}! Check your email.'
        })
```

Notice the `.delay()` call — this is the key. It puts the task in the Redis queue and returns immediately.

---

## Calling Tasks: `delay()` vs `apply_async()`

| Method | Usage | When to Use |
|--------|-------|-------------|
| `task.delay(arg1, arg2)` | Simple call, shortcut for `apply_async` | Most of the time |
| `task.apply_async(args=[arg1, arg2], kwargs={})` | Full control over task execution | When you need countdown, ETA, or retries |

### Using `apply_async` for More Control

```python
from .tasks import send_welcome_email

# Send email after 60 seconds (countdown)
send_welcome_email.apply_async(
    args=['rahul@example.com', 'Rahul'],
    countdown=60   # Wait 60 seconds before executing
)

# Send email at a specific time (ETA)
from datetime import datetime, timedelta

tomorrow_9am = datetime.now() + timedelta(days=1)
tomorrow_9am = tomorrow_9am.replace(hour=9, minute=0, second=0)

send_welcome_email.apply_async(
    args=['priya@example.com', 'Priya'],
    eta=tomorrow_9am
)

# Retry on failure
send_welcome_email.apply_async(
    args=['amit@example.com', 'Amit'],
    retry=True,
    retry_policy={
        'max_retries': 3,
        'interval_start': 10,   # Wait 10 seconds before first retry
    }
)
```

---

## Example 2: Generating a Student Report

Ananya (admin) wants to generate a PDF report of all students in the CSE department. This involves querying hundreds of records and creating a PDF — it could take 10-15 seconds.

```python
# reports/tasks.py
from celery import shared_task
import csv
import os

@shared_task
def generate_student_report(department, requested_by_email):
    """Generate a CSV report of students in a department."""
    from students.models import Student
    from django.core.mail import EmailMessage

    students = Student.objects.filter(branch=department, is_active=True)

    # Create CSV file
    file_path = f'/tmp/report_{department}.csv'
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Email', 'Semester', 'CGPA', 'City'])

        for student in students:
            writer.writerow([
                student.name,
                student.email,
                student.semester,
                student.cgpa,
                student.city,
            ])

    # Send the report via email
    email = EmailMessage(
        subject=f'{department} Student Report - TechPath Institute',
        body=f'Hi,\n\nPlease find the {department} student report attached.\n\nTeam TechPath',
        from_email='noreply@techpath.biz',
        to=[requested_by_email],
    )
    email.attach_file(file_path)
    email.send()

    # Clean up
    os.remove(file_path)

    return f'Report for {department} sent to {requested_by_email}'
```

```python
# In the admin view
from reports.tasks import generate_student_report

def export_report(request):
    department = request.GET.get('department', 'CSE')
    generate_student_report.delay(department, request.user.email)
    return JsonResponse({
        'message': f'{department} report is being generated. You will receive it via email shortly.'
    })
```

---

## Example 3: Sending Bulk SMS

Sneha (admin) needs to send an exam reminder SMS to all 500 active students. Sending one SMS takes about 1 second (API call). Without Celery, the admin would wait 500 seconds (over 8 minutes).

```python
# notifications/tasks.py
from celery import shared_task
import time

@shared_task
def send_single_sms(phone_number, message):
    """Send SMS to a single student."""
    # In production, call your SMS API here (e.g., Twilio, MSG91)
    # This is a simulation
    print(f'Sending SMS to {phone_number}: {message}')
    time.sleep(0.5)  # Simulating API call delay
    return f'SMS sent to {phone_number}'


@shared_task
def send_bulk_exam_reminder(exam_name, exam_date):
    """Send exam reminder to all active students."""
    from students.models import Student

    students = Student.objects.filter(is_active=True)
    message = f'Reminder: {exam_name} is on {exam_date}. All the best! - TechPath Institute'

    count = 0
    for student in students:
        # Queue each SMS as a separate task
        send_single_sms.delay(student.phone, message)
        count += 1

    return f'Queued {count} SMS messages for {exam_name}'
```

```python
# In the admin view
from notifications.tasks import send_bulk_exam_reminder

def send_reminders(request):
    send_bulk_exam_reminder.delay('End Semester Exam', '15th December 2026')
    return JsonResponse({
        'message': 'Exam reminders are being sent to all students.'
    })
```

The admin sees "Reminders are being sent" instantly. Each SMS is a separate Celery task, so they run in parallel across multiple workers.

---

## Periodic Tasks with Celery Beat

Some tasks need to run on a schedule — like a daily attendance report or a weekly database cleanup. **Celery Beat** is the scheduler that triggers tasks at specified intervals, like an alarm clock.

### Installation

```bash
pip install django-celery-beat
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_celery_beat',
]
```

Run migrations:

```bash
python manage.py migrate
```

### Defining Periodic Tasks in Settings

```python
# settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Send daily attendance report at 6 PM IST
    'daily-attendance-report': {
        'task': 'reports.tasks.send_daily_attendance',
        'schedule': crontab(hour=18, minute=0),
    },

    # Clean up expired sessions every Sunday at midnight
    'weekly-session-cleanup': {
        'task': 'maintenance.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=0, minute=0, day_of_week=0),
    },

    # Check server health every 5 minutes
    'health-check': {
        'task': 'monitoring.tasks.check_server_health',
        'schedule': 300.0,  # Every 300 seconds (5 minutes)
    },

    # Monthly fee reminder on the 1st of every month
    'monthly-fee-reminder': {
        'task': 'notifications.tasks.send_fee_reminder',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),
    },
}
```

### Common Schedule Patterns

| Pattern | Crontab | Meaning |
|---------|---------|---------|
| Every minute | `crontab()` | Runs every minute |
| Every hour | `crontab(minute=0)` | At minute 0 of every hour |
| Daily at 9 AM | `crontab(hour=9, minute=0)` | 9:00 AM every day |
| Every Monday at 8 AM | `crontab(hour=8, minute=0, day_of_week=1)` | Monday 8:00 AM |
| 1st of every month | `crontab(hour=0, minute=0, day_of_month=1)` | Midnight on the 1st |
| Every 10 minutes | `600.0` (seconds) | Every 600 seconds |

---

## Running Celery

You need to run three separate processes:

### 1. Django Server (the waiter)

```bash
python manage.py runserver
```

### 2. Celery Worker (the cook)

```bash
celery -A myproject worker --loglevel=info
```

On Windows, you may need to add `--pool=solo`:

```bash
celery -A myproject worker --loglevel=info --pool=solo
```

You will see output like:

```
[config]
.> app:         myproject:0x...
.> transport:   redis://localhost:6379/0
.> results:     redis://localhost:6379/0
.> concurrency: 4 (prefork)

[queues]
.> celery       exchange=celery(direct) key=celery

[tasks]
  . accounts.tasks.send_welcome_email
  . reports.tasks.generate_student_report
  . notifications.tasks.send_single_sms
  . notifications.tasks.send_bulk_exam_reminder
```

### 3. Celery Beat (the alarm clock) — only if using periodic tasks

```bash
celery -A myproject beat --loglevel=info
```

---

## Monitoring with Flower

**Flower** is a web-based monitoring tool for Celery. Think of it as a CCTV for your kitchen — you can see which tasks are running, which failed, and how many are in the queue.

### Installation

```bash
pip install flower
```

### Running Flower

```bash
celery -A myproject flower --port=5555
```

Open `http://localhost:5555` in your browser.

### What Flower Shows You

| Tab | Information |
|-----|-------------|
| Dashboard | Active workers, task counts, success/failure rates |
| Tasks | List of all tasks with status, runtime, and results |
| Workers | CPU usage, memory, currently running tasks |
| Broker | Queue sizes, pending messages |
| Monitor | Real-time graphs of task throughput |

---

## Task Error Handling and Retries

What if the email server is down? Your task should retry instead of failing silently.

```python
# accounts/tasks.py
from celery import shared_task

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # Wait 60 seconds between retries
)
def send_welcome_email(self, user_email, user_name):
    try:
        # ... send email logic ...
        pass
    except Exception as exc:
        print(f'Email to {user_email} failed: {exc}. Retrying...')
        raise self.retry(exc=exc)
```

| Parameter | What It Does |
|-----------|-------------|
| `bind=True` | Gives access to `self` (the task instance) for retries |
| `max_retries=3` | Try at most 3 times before giving up |
| `default_retry_delay=60` | Wait 60 seconds between retries |
| `self.retry(exc=exc)` | Re-queue the task for another attempt |

---

## Complete Project Structure

```
myproject/
    myproject/
        __init__.py       # Import celery_app here
        settings.py       # Celery config here
        celery.py         # Celery app definition
        urls.py
        asgi.py
        wsgi.py
    accounts/
        tasks.py          # send_welcome_email
    reports/
        tasks.py          # generate_student_report
    notifications/
        tasks.py          # send_single_sms, send_bulk_exam_reminder
    manage.py
```

---

## Quick Reference

| Concept | What It Does |
|---------|-------------|
| Celery | Task queue library — runs functions in the background |
| Redis | In-memory data store used as Celery's message broker |
| `@shared_task` | Decorator that makes a function a Celery task |
| `.delay()` | Queue a task for immediate background execution |
| `.apply_async()` | Queue a task with extra options (countdown, ETA, retries) |
| Celery Worker | Process that picks up and executes tasks |
| Celery Beat | Scheduler for periodic/recurring tasks |
| Flower | Web dashboard for monitoring Celery tasks |
| `bind=True` | Allows task to reference itself for retries |
| `max_retries` | Maximum number of retry attempts |

---

*TechPath Institute — Python Full Stack Development Program*
