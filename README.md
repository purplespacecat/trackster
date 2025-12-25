# Trackster

A personal note-taking journal application built with FastAPI backend and Reflex UI. Capture notes with timestamps, delete them easily, and manage your personal log in a clean, Python-only stack.

## Project Structure

```
trackster/
├── main.py              # FastAPI backend (REST API)
├── database.py          # SQLAlchemy database models
├── app_reflex/          # Reflex UI (frontend)
│   └── app_reflex.py    # Main Reflex application
├── rxconfig.py          # Reflex configuration
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

You need to run **both** the backend and frontend:

### 1. Start the FastAPI backend (Terminal 1):
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`

### 2. Start the Reflex UI (Terminal 2):
```bash
reflex run
```
The UI will open automatically in your browser at `http://localhost:3000`

## Features

- **Note-taking** with automatic timestamps
- **Delete notes** with dedicated delete buttons next to each note
- **FastAPI backend** for robust REST API
- **Reflex UI** for modern, reactive interface (pure Python, no HTML/CSS/JS needed!)
- **Real-time updates** with refresh functionality
- **SQLite database** for persistent note storage
- **Clean, centered, minimal layout**

## API Endpoints

- `GET /hello` - Test endpoint returning a greeting
- `POST /note` - Add a new note with timestamp
  - Body: `{"text": "your note"}`
  - Returns: `{"received": "...", "timestamp": "...", "total_notes": N}`
- `GET /notes` - Retrieve all notes with timestamps and IDs
  - Returns: `{"notes": [{"id": 1, "text": "...", "timestamp": "..."}, ...]}`
- `DELETE /note/{note_id}` - Delete a note by ID
  - Returns: `{"success": true/false, "message": "..."}`

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs` (test endpoints directly)
- **ReDoc**: `http://localhost:8000/redoc` (alternative documentation view)

## Tech Stack

- **Backend**: FastAPI + Pydantic + SQLAlchemy
- **Frontend**: Reflex (Python-based reactive web framework)
- **Database**: SQLite
- **Language**: Python 3.12+
- **Dependencies**: See `requirements.txt`
