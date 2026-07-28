# Voice AI

**Module 12 -- AI Chatbots | Topic 5**

---

## What is Voice AI?

Voice AI lets chatbots listen to spoken words and respond with speech. It combines two technologies:
- **Speech-to-Text (STT)**: Converts spoken audio into text (what the user said)
- **Text-to-Speech (TTS)**: Converts text into spoken audio (the bot's response)

**Analogy:** Think of Voice AI like a translator at TechPath Institute. When a student speaks in English, the translator writes it down (STT). When the bot types a reply, the translator reads it aloud (TTS).

```
Student speaks: "What is the Python course fee?"
       |
  [Speech-to-Text] --> "What is the Python course fee?" (text)
       |
  [Chatbot processes] --> "The fee is Rs 49,999" (text)
       |
  [Text-to-Speech] --> audio response plays
       |
Student hears: "The fee is Rs 49,999"
```

---

## Speech-to-Text (STT)

### OpenAI Whisper (Most Popular)

Whisper is OpenAI's speech recognition model. It supports many languages including Hindi and English.

```python
from openai import OpenAI

client = OpenAI()

def speech_to_text(audio_file_path: str) -> str:
    """Convert audio file to text using Whisper."""
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en",    # Use "hi" for Hindi
        )
    return transcript.text

# Usage
text = speech_to_text("student_question.mp3")
print(f"Student said: {text}")
# "Student said: What is the fee for Python Full Stack course?"
```

### Supported Audio Formats

| Format | Extension | Max Size |
|--------|-----------|----------|
| MP3 | `.mp3` | 25 MB |
| WAV | `.wav` | 25 MB |
| M4A | `.m4a` | 25 MB |
| WEBM | `.webm` | 25 MB |
| MP4 | `.mp4` | 25 MB |

### Local STT with Whisper (Free)

Run Whisper on your own computer -- no API key, no cost:

```python
# pip install openai-whisper
import whisper

model = whisper.load_model("base")    # Options: tiny, base, small, medium, large
result = model.transcribe("student_question.mp3")
print(result["text"])
```

| Model Size | Accuracy | Speed | RAM Needed |
|-----------|---------|-------|-----------|
| tiny | Low | Very fast | 1 GB |
| base | Good | Fast | 1 GB |
| small | Better | Medium | 2 GB |
| medium | Very good | Slow | 5 GB |
| large | Best | Very slow | 10 GB |

---

## Text-to-Speech (TTS)

### ElevenLabs (Best Quality)

ElevenLabs produces the most natural-sounding voices. Great for professional chatbots.

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your-api-key")

def text_to_speech(text: str, output_file: str = "response.mp3") -> str:
    """Convert text to speech using ElevenLabs."""
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",    # George voice
        model_id="eleven_multilingual_v2",    # Supports Hindi too
    )
    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_file

# Usage
text_to_speech("Welcome to TechPath Institute. How can I help you today?")
```

### OpenAI TTS

```python
from openai import OpenAI

client = OpenAI()

def openai_tts(text: str, output_file: str = "response.mp3") -> str:
    """Convert text to speech using OpenAI TTS."""
    response = client.audio.speech.create(
        model="tts-1",          # or "tts-1-hd" for higher quality
        voice="alloy",          # Options: alloy, echo, fable, onyx, nova, shimmer
        input=text,
    )
    response.stream_to_file(output_file)
    return output_file
```

### pyttsx3 (Free, Offline)

For offline use -- no API key needed, runs entirely on your computer:

```python
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)      # Speed (words per minute)
engine.setProperty("volume", 0.9)    # Volume (0.0 to 1.0)

def offline_tts(text: str):
    """Speak text using the system's built-in voice."""
    engine.say(text)
    engine.runAndWait()

offline_tts("Welcome to TechPath Institute Bhopal")
```

### TTS Comparison

| Service | Quality | Cost | Hindi Support | Offline |
|---------|---------|------|--------------|---------|
| ElevenLabs | Excellent | Free tier (10K chars/month) | Yes | No |
| OpenAI TTS | Good | ~$15/1M chars | No | No |
| Google Cloud TTS | Good | Free tier (4M chars/month) | Yes | No |
| pyttsx3 | Basic | Free | No | Yes |

---

## Building a Voice-Enabled Chatbot

### FastAPI Backend with Audio Support

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import anthropic
from openai import OpenAI

app = FastAPI()
anthropic_client = anthropic.Anthropic()
openai_client = OpenAI()

@app.post("/voice-chat")
async def voice_chat(audio: UploadFile = File(...)):
    # Step 1: Save uploaded audio
    audio_path = f"temp/{audio.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())
    
    # Step 2: Speech-to-Text
    with open(audio_path, "rb") as f:
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1", file=f
        )
    user_text = transcript.text
    
    # Step 3: Get chatbot response
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": user_text}],
    )
    bot_text = response.content[0].text
    
    # Step 4: Text-to-Speech
    audio_response = openai_client.audio.speech.create(
        model="tts-1", voice="nova", input=bot_text
    )
    output_path = "temp/response.mp3"
    audio_response.stream_to_file(output_path)
    
    return {
        "user_text": user_text,
        "bot_text": bot_text,
        "audio_url": "/audio/response.mp3",
    }
```

### Frontend: Recording Audio

```javascript
let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    
    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };
    
    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.webm");
        
        const response = await fetch("/voice-chat", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        
        // Display text and play audio
        document.getElementById("user-text").innerText = data.user_text;
        document.getElementById("bot-text").innerText = data.bot_text;
        new Audio(data.audio_url).play();
    };
    
    mediaRecorder.start();
}

function stopRecording() {
    mediaRecorder.stop();
}
```

---

## Hindi Language Support

For supporting Hindi-speaking students:

```python
# Speech-to-Text in Hindi
transcript = openai_client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="hi",    # Hindi
)

# Text-to-Speech in Hindi (ElevenLabs)
audio = elevenlabs_client.text_to_speech.convert(
    text="TechPath Institute mein aapka swagat hai",
    voice_id="hindi-voice-id",
    model_id="eleven_multilingual_v2",
)
```

---

## Summary

| Component | What It Does | Best Tool |
|-----------|-------------|-----------|
| Speech-to-Text | Audio -> Text | Whisper (OpenAI API or local) |
| Text-to-Speech | Text -> Audio | ElevenLabs (best quality) |
| Voice chatbot | Complete pipeline | STT -> Chatbot -> TTS |
| Hindi support | Indian language processing | Whisper + ElevenLabs multilingual |
| Offline option | No internet needed | Local Whisper + pyttsx3 |
