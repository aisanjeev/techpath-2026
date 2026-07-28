# Multimodal AI

**Module 12 -- AI Chatbots | Topic 6**

---

## What is Multimodal AI?

Multimodal means the AI can understand **more than just text**. It can also process images, audio, and documents. Models like Claude and GPT-4V can look at an image and answer questions about it.

**Analogy:** A text-only AI is like someone who can only read books. A multimodal AI is like someone who can read books, look at photos, listen to audio, and watch videos -- and understand all of them.

| Modality | What It Processes | Example |
|----------|------------------|---------|
| Text | Written words | "What is Python?" |
| Image | Photos, screenshots, diagrams | "What error is in this screenshot?" |
| Audio | Spoken words, sounds | "Transcribe this lecture" |
| Video | Moving images | "Summarize this tutorial" (limited support) |

---

## Sending Images to Claude

Claude can analyze images and answer questions about them.

```python
import anthropic
import base64

client = anthropic.Anthropic()

def analyze_image(image_path: str, question: str) -> str:
    """Send an image to Claude and ask a question about it."""
    # Read and encode the image
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
    
    # Determine media type
    ext = image_path.split(".")[-1].lower()
    media_types = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}
    media_type = media_types.get(ext, "image/png")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return response.content[0].text

# Usage
result = analyze_image("error_screenshot.png", "What error is shown? How do I fix it?")
print(result)
```

### Sending Image URLs

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://example.com/diagram.png",
                },
            },
            {"type": "text", "text": "Explain this diagram."},
        ],
    }],
)
```

---

## Use Cases for Multimodal Chatbots

### 1. Error Screenshot Analysis

Students can screenshot their error and get help:

```python
def analyze_error_screenshot(image_path: str) -> str:
    return analyze_image(
        image_path,
        "This is a screenshot of a programming error. "
        "1. What error is shown? "
        "2. What caused it? "
        "3. How to fix it? "
        "Explain in simple language for a beginner."
    )
```

### 2. OCR -- Reading Text from Images

Extract text from handwritten notes, printed documents, or whiteboard photos:

```python
def extract_text_from_image(image_path: str) -> str:
    return analyze_image(
        image_path,
        "Extract ALL the text visible in this image. "
        "Maintain the original formatting and structure."
    )

# Student photographs handwritten notes
text = extract_text_from_image("handwritten_notes.jpg")
print(text)
```

### 3. Diagram Explanation

Students upload ER diagrams, flowcharts, or architecture diagrams:

```python
def explain_diagram(image_path: str) -> str:
    return analyze_image(
        image_path,
        "Explain this diagram in detail. "
        "What does each component represent? "
        "How do they connect to each other? "
        "Use simple language for a TechPath student."
    )
```

### 4. Code from Screenshots

Read code from a screenshot (when students cannot copy-paste):

```python
def read_code_from_image(image_path: str) -> str:
    return analyze_image(
        image_path,
        "Read the code in this image. "
        "1. Type out the exact code "
        "2. Explain what it does "
        "3. Point out any bugs you see"
    )
```

### 5. Document Analysis

Read forms, invoices, or certificates:

```python
def analyze_document(image_path: str) -> str:
    return analyze_image(
        image_path,
        "Read this document and extract: "
        "- Name, date, and any ID numbers "
        "- Key information and amounts "
        "- Any signatures or stamps present"
    )
```

---

## Multiple Images in One Request

Send several images at once for comparison or analysis:

```python
def compare_images(image1_path: str, image2_path: str, question: str) -> str:
    """Compare two images."""
    images = []
    for path in [image1_path, image2_path]:
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")
        ext = path.split(".")[-1].lower()
        images.append({
            "type": "image",
            "source": {"type": "base64", "media_type": f"image/{ext}", "data": data},
        })
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": images + [{"type": "text", "text": question}],
        }],
    )
    return response.content[0].text

# Compare two code screenshots
result = compare_images(
    "before_fix.png",
    "after_fix.png",
    "What changed between these two versions of the code?"
)
```

---

## Building a Multimodal Chat API

```python
from fastapi import FastAPI, UploadFile, File, Form
import base64

app = FastAPI()

@app.post("/multimodal-chat")
async def multimodal_chat(
    question: str = Form(...),
    image: UploadFile = File(None),
):
    content = []
    
    # Add image if provided
    if image:
        image_data = base64.standard_b64encode(await image.read()).decode("utf-8")
        ext = image.filename.split(".")[-1].lower()
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": f"image/{ext}", "data": image_data},
        })
    
    # Add the text question
    content.append({"type": "text", "text": question})
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
    )
    
    return {"answer": response.content[0].text}
```

---

## Image Limitations

| Limitation | Detail |
|-----------|--------|
| Max file size | ~5 MB per image (varies by provider) |
| Supported formats | PNG, JPEG, GIF, WEBP |
| No video (yet) | Most models cannot process video frames |
| OCR quality | Works well on printed text, less reliable on messy handwriting |
| Cannot generate images | Claude analyzes images but does not create them |

---

## Summary

| Feature | What It Does | Input |
|---------|-------------|-------|
| Image analysis | Answers questions about an image | Image + question |
| OCR | Extracts text from images | Image of text |
| Error diagnosis | Analyzes error screenshots | Screenshot |
| Diagram explanation | Explains flowcharts, ER diagrams | Diagram image |
| Code reading | Reads code from screenshots | Code screenshot |
| Document analysis | Extracts info from forms/invoices | Document image |

| Best Practice | Why |
|--------------|-----|
| Compress large images before sending | Saves tokens and money |
| Be specific in your question | "What error is shown?" is better than "What is this?" |
| Handle missing images gracefully | Not all messages will have images |
| Use base64 encoding for local files | Most reliable method |
