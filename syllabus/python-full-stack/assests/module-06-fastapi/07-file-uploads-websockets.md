# File Uploads, WebSockets & Streaming

**Module 06 — FastAPI: Modern API Development | Topic 7**

---

## File Uploads

### Single File Upload

```python
from fastapi import UploadFile, File, HTTPException
import shutil
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"File type {file.content_type} not allowed")

    # Validate file size (5 MB max)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large. Maximum 5 MB.")

    # Save the file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type,
        "path": str(file_path)
    }
```

### Multiple File Upload

```python
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(contents)
        results.append({
            "filename": file.filename,
            "size": len(contents)
        })
    return {"uploaded": len(results), "files": results}
```

### File Upload with Form Data

```python
from fastapi import Form

@app.post("/students/with-photo")
async def create_student_with_photo(
    name: str = Form(...),
    email: str = Form(...),
    city: str = Form("Bhopal"),
    photo: UploadFile = File(None)
):
    result = {"name": name, "email": email, "city": city}

    if photo:
        contents = await photo.read()
        file_path = UPLOAD_DIR / f"{email}_{photo.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)
        result["photo"] = str(file_path)

    return result
```

### Serving Uploaded Files

```python
from fastapi.staticfiles import StaticFiles

# Mount the uploads directory as a static route
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Files are now accessible at:
# http://localhost:8000/uploads/rahul_photo.jpg
```

### Best Practices for File Uploads

| Practice | Why |
|----------|-----|
| Validate file type (MIME type) | Prevent uploading malicious files |
| Limit file size | Prevent server running out of disk space |
| Generate unique filenames | Prevent overwriting existing files |
| Store outside web root | Prevent direct URL access to private files |
| Use cloud storage in production | Azure Blob, AWS S3 for scalability |

---

## WebSockets — Real-Time Communication

HTTP is **request-response**: the client asks, the server answers. WebSockets are **bidirectional**: both client and server can send messages at any time.

```
HTTP:       Client ──request──► Server ──response──► Client (connection closes)
WebSocket:  Client ◄──────────────────────────────► Server (connection stays open)
```

### When to Use WebSockets

| Use Case | Example |
|----------|---------|
| Chat applications | WhatsApp-style messaging |
| Live notifications | "Priya just enrolled in your course" |
| Real-time dashboards | Live student count, revenue tracker |
| Collaborative editing | Google Docs-style simultaneous editing |
| Live quiz/polling | Real-time quiz responses in a classroom |

### Basic WebSocket Endpoint

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the connection

    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_text()
            print(f"Received: {data}")

            # Send a response
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### Chat Room Example

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    """Manages all active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """Send a message to ALL connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{username}")
async def chat(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    await manager.broadcast(f"{username} joined the chat!")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat.")
```

### Client-Side WebSocket (JavaScript)

```html
<script>
    const ws = new WebSocket("ws://localhost:8000/ws/chat/Rahul");

    ws.onopen = () => {
        console.log("Connected!");
    };

    ws.onmessage = (event) => {
        console.log("Received:", event.data);
        // Display the message in the UI
    };

    ws.onclose = () => {
        console.log("Disconnected");
    };

    // Send a message
    function sendMessage(text) {
        ws.send(text);
    }
</script>
```

### WebSocket with JSON

```python
@app.websocket("/ws/notifications")
async def notifications(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # data is a Python dict

            response = {
                "type": "notification",
                "message": f"Received: {data.get('action')}",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass
```

---

## Streaming Responses

For large data or real-time data, send the response in chunks instead of all at once.

### StreamingResponse

```python
from fastapi.responses import StreamingResponse
import csv
import io

@app.get("/students/export")
async def export_students(db: AsyncSession = Depends(get_db)):
    students = await get_all_students(db)

    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Name", "Email", "City", "Fee Paid"])
        for s in students:
            writer.writerow([s.id, s.name, s.email, s.city, s.fee_paid])
        output.seek(0)
        yield output.read()

    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students.csv"}
    )
```

### Server-Sent Events (SSE)

SSE is a one-way stream from server to client — simpler than WebSockets for notifications.

```python
import asyncio
from fastapi.responses import StreamingResponse

@app.get("/events")
async def server_sent_events():
    async def event_generator():
        counter = 0
        while True:
            counter += 1
            yield f"data: Event #{counter} at {datetime.now().isoformat()}\n\n"
            await asyncio.sleep(2)  # Send every 2 seconds

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

**Client-side:**
```javascript
const source = new EventSource("http://localhost:8000/events");
source.onmessage = (event) => {
    console.log("Received:", event.data);
};
```

---

## File Download

```python
from fastapi.responses import FileResponse

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream"
    )
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| UploadFile | Handle file uploads with validation |
| File(...) | Mark a parameter as a file upload |
| StaticFiles | Serve uploaded files via URL |
| WebSocket | Bidirectional real-time communication |
| ConnectionManager | Track and broadcast to multiple clients |
| StreamingResponse | Send large data in chunks |
| SSE | One-way server-to-client event stream |
| FileResponse | Send files for download |

---

*TechPath Institute — Python Full Stack Development*
