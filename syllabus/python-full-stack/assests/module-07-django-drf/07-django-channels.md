# Django Channels & WebSockets

**Module 07 — Django & Django REST Framework | Topic 7**

---

## What Are WebSockets?

To understand WebSockets, let us compare two ways of communication:

**HTTP = Sending a letter (post)**
- You write a letter (request), send it to the post office (server)
- The post office sends a reply (response)
- Connection closed. If you want to ask something else, write another letter.
- This is called **request-response** — one question, one answer, done.

**WebSocket = Making a phone call**
- You dial the number (open connection)
- Both sides can talk anytime — you can speak, they can speak, no waiting
- The line stays open until someone hangs up
- This is called **full-duplex** — both sides communicate freely in real time.

### When Do You Need WebSockets?

| Use Case | HTTP Works? | WebSocket Needed? |
|----------|------------|-------------------|
| Loading a blog page | Yes | No |
| Checking order status every 5 seconds | Yes (but wasteful) | Better with WebSocket |
| Live chat application | Too slow | Yes |
| Live cricket score updates | Polling is wasteful | Yes |
| Real-time notifications | Polling is wasteful | Yes |
| Collaborative document editing | Too slow | Yes |

---

## ASGI vs WSGI

Django traditionally uses **WSGI** (Web Server Gateway Interface), which handles one request at a time — synchronous, like a single-lane road.

Django Channels upgrades Django to **ASGI** (Asynchronous Server Gateway Interface), which can handle many connections at once — asynchronous, like a multi-lane highway.

| Feature | WSGI | ASGI |
|---------|------|------|
| Protocol | HTTP only | HTTP + WebSocket + more |
| Concurrency | One request at a time | Many connections at once |
| Real-time | Not possible | Built for it |
| Django default | Yes | Needs `channels` package |

---

## Installing Django Channels

```bash
pip install channels
pip install channels-redis   # For channel layers (we will use this later)
```

Update `settings.py`:

```python
# settings.py
INSTALLED_APPS = [
    'daphne',          # ASGI server (installed with channels)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'notices',          # Our app
]

# Tell Django to use ASGI instead of WSGI
ASGI_APPLICATION = 'myproject.asgi.application'
```

Update `asgi.py`:

```python
# myproject/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notices.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notices.routing.websocket_urlpatterns
        )
    ),
})
```

The `ProtocolTypeRouter` decides what to do based on the connection type:
- HTTP requests go to Django as usual
- WebSocket connections go to your consumers

---

## Our Example: College Notice Board

Imagine TechPath Institute, Bhopal has a notice board outside the main building. Currently, students have to physically walk to the board to check for new notices. We will build a **real-time digital notice board** where:

- When a teacher posts a notice, every student connected sees it instantly
- Students can join a "room" for their department (CSE, ECE, etc.)
- No need to refresh the page

---

## Consumers — Handling WebSocket Connections

A **consumer** is like a view, but for WebSockets. While a Django view handles an HTTP request and returns a response, a consumer handles a WebSocket connection and can send/receive messages anytime.

### WebsocketConsumer (Synchronous)

```python
# notices/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class NoticeBoardConsumer(WebsocketConsumer):
    def connect(self):
        """Called when a student opens the notice board page."""
        self.accept()  # Accept the WebSocket connection
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Welcome to TechPath Notice Board!'
        }))

    def disconnect(self, close_code):
        """Called when a student closes the page."""
        pass  # Clean up if needed

    def receive(self, text_data):
        """Called when a message is received from the student."""
        data = json.loads(text_data)
        message = data.get('message', '')

        # Echo the message back (for now)
        self.send(text_data=json.dumps({
            'type': 'notice',
            'message': f'You said: {message}'
        }))
```

### AsyncWebsocketConsumer (Asynchronous — Recommended)

For better performance, use the async version:

```python
# notices/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NoticeBoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.department = self.scope['url_route']['kwargs']['department']
        self.room_group_name = f'notices_{self.department}'

        # Join the department group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected to {self.department.upper()} notice board'
        }))

    async def disconnect(self, close_code):
        # Leave the department group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        notice_title = data.get('title', '')
        notice_body = data.get('body', '')
        posted_by = data.get('posted_by', 'Unknown')

        # Broadcast to everyone in the department group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_notice',
                'title': notice_title,
                'body': notice_body,
                'posted_by': posted_by,
            }
        )

    async def new_notice(self, event):
        """Handler for notices broadcast to the group."""
        await self.send(text_data=json.dumps({
            'type': 'notice',
            'title': event['title'],
            'body': event['body'],
            'posted_by': event['posted_by'],
        }))
```

Key concepts in this consumer:

| Concept | What It Does |
|---------|-------------|
| `self.scope` | Contains connection info (URL params, user, headers) |
| `self.channel_name` | Unique name for this specific connection |
| `self.channel_layer` | The messaging system that connects consumers |
| `group_add` | Add this connection to a group (like joining a WhatsApp group) |
| `group_send` | Send a message to everyone in the group |
| `group_discard` | Remove this connection from the group |

---

## Routing — URLs for WebSockets

Just like Django has URL patterns for HTTP, Channels has routing for WebSocket connections:

```python
# notices/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notices/(?P<department>\w+)/$', consumers.NoticeBoardConsumer.as_asgi()),
]
```

A CSE student connects to: `ws://localhost:8000/ws/notices/cse/`
An ECE student connects to: `ws://localhost:8000/ws/notices/ece/`

---

## Channel Layers with Redis

A **channel layer** is the messaging backbone that lets different consumers talk to each other. Without it, each consumer is isolated — like having phones that cannot call each other.

**Redis** is used as the channel layer backend because it is fast, reliable, and designed for real-time messaging.

### Installing Redis

On Ubuntu/Debian:
```bash
sudo apt install redis-server
sudo systemctl start redis
```

On Windows (for development):
```bash
# Use WSL or download from https://github.com/microsoftarchive/redis/releases
# Or use Docker:
docker run -p 6379:6379 redis
```

### Configuring Channel Layers

```python
# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

For development without Redis, you can use the in-memory layer (not for production):

```python
# settings.py (development only)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
```

### Testing the Channel Layer

```bash
python manage.py shell
```

```python
import channels.layers
from asgiref.sync import async_to_sync

channel_layer = channels.layers.get_channel_layer()
async_to_sync(channel_layer.send)('test_channel', {'type': 'hello', 'message': 'hi'})
result = async_to_sync(channel_layer.receive)('test_channel')
print(result)
# {'type': 'hello', 'message': 'hi'}
```

If this works, your channel layer is configured correctly.

---

## Frontend — Connecting from the Browser

Here is a simple HTML page that connects to the notice board:

```html
<!-- notices/templates/notices/board.html -->
<!DOCTYPE html>
<html>
<head>
    <title>TechPath Notice Board - {{ department|upper }}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; }
        .notice { background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .notice h3 { margin: 0 0 5px; }
        .notice small { color: #666; }
        #post-form { margin: 20px 0; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; box-sizing: border-box; }
        button { background: #2563eb; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>TechPath Notice Board — {{ department|upper }}</h1>
    <div id="post-form">
        <input type="text" id="title" placeholder="Notice Title" />
        <textarea id="body" placeholder="Notice Body" rows="3"></textarea>
        <input type="text" id="posted_by" placeholder="Your Name" />
        <button onclick="postNotice()">Post Notice</button>
    </div>
    <div id="notices"></div>

    <script>
        const department = "{{ department }}";
        const ws = new WebSocket(`ws://${window.location.host}/ws/notices/${department}/`);

        ws.onopen = function() {
            console.log('Connected to notice board');
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'notice') {
                const noticesDiv = document.getElementById('notices');
                noticesDiv.innerHTML = `
                    <div class="notice">
                        <h3>${data.title}</h3>
                        <p>${data.body}</p>
                        <small>Posted by: ${data.posted_by}</small>
                    </div>
                ` + noticesDiv.innerHTML;
            }
        };

        ws.onclose = function() {
            console.log('Disconnected from notice board');
        };

        function postNotice() {
            const title = document.getElementById('title').value;
            const body = document.getElementById('body').value;
            const posted_by = document.getElementById('posted_by').value;

            ws.send(JSON.stringify({ title, body, posted_by }));

            // Clear the form
            document.getElementById('title').value = '';
            document.getElementById('body').value = '';
        }
    </script>
</body>
</html>
```

### Django View and URL for the Template

```python
# notices/views.py
from django.shortcuts import render

def notice_board(request, department):
    return render(request, 'notices/board.html', {
        'department': department
    })
```

```python
# notices/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('notices/<str:department>/', views.notice_board, name='notice_board'),
]
```

---

## Real-Time Notifications from Django Views

Sometimes you want to send WebSocket messages from a regular Django view or a Celery task — not from inside a consumer. For example, when Ananya (a teacher) creates a notice through the admin panel, all connected students should see it.

```python
# notices/views.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

def create_notice_api(request):
    """API endpoint for teachers to post notices."""
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        department = request.POST.get('department')

        # Save to database (assuming Notice model exists)
        # Notice.objects.create(title=title, body=body, department=department)

        # Broadcast to all connected students in that department
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notices_{department}',
            {
                'type': 'new_notice',
                'title': title,
                'body': body,
                'posted_by': request.user.username,
            }
        )

        return JsonResponse({'status': 'Notice posted and broadcast!'})
```

---

## Running the ASGI Server

Instead of `runserver`, use Daphne (the ASGI server that comes with Channels):

```bash
# Development
python manage.py runserver   # Channels auto-patches this to use ASGI

# Production
daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
```

---

## Summary — How the Pieces Fit Together

```
Student opens page
    |
    v
Browser creates WebSocket connection
    |
    v
ASGI Router (asgi.py) checks protocol
    |
    v
WebSocket --> Channels routing (routing.py)
    |
    v
Consumer handles connect/receive/disconnect
    |
    v
Channel Layer (Redis) manages groups
    |
    v
Messages broadcast to all group members
```

---

## Quick Reference

| Concept | What It Does |
|---------|-------------|
| WebSocket | Persistent two-way connection between browser and server |
| ASGI | Async server interface — supports HTTP + WebSocket |
| Consumer | Like a view, but for WebSocket connections |
| Routing | Maps WebSocket URLs to consumers |
| Channel Layer | Messaging backbone (uses Redis) for cross-consumer communication |
| Group | A set of connections that receive the same broadcasts |
| `group_send` | Send a message to all connections in a group |
| Daphne | ASGI server for production deployment |

---

*TechPath Institute — Python Full Stack Development Program*
