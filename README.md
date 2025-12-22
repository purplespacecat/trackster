# Trackster

A message tracking application built with FastAPI backend and Streamlit UI. Track messages with timestamps in a clean, Python-only stack.

## Project Structure

```
trackster/
├── main.py          # FastAPI backend (REST API)
├── app.py           # Streamlit UI (frontend)
├── requirements.txt # Python dependencies
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

### 2. Start the Streamlit UI (Terminal 2):
```bash
streamlit run app.py
```
The UI will open automatically in your browser at `http://localhost:8501`

## Features

- **Message tracking** with automatic timestamps
- **FastAPI backend** for robust REST API
- **Streamlit UI** for easy interaction (no HTML/JS needed!)
- **Real-time updates** with refresh functionality
- **In-memory storage** (messages reset on server restart)

## API Endpoints

- `GET /hello` - Test endpoint returning a greeting
- `POST /message` - Add a new message with timestamp
  - Body: `{"text": "your message"}`
  - Returns: `{"received": "...", "timestamp": "...", "total_messages": N}`
- `GET /messages` - Retrieve all messages with timestamps
  - Returns: `{"messages": [{"text": "...", "timestamp": "..."}, ...]}`

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs` (test endpoints directly)
- **ReDoc**: `http://localhost:8000/redoc` (alternative documentation view)

## Tech Stack

- **Backend**: FastAPI + Pydantic
- **Frontend**: Streamlit
- **Language**: Python 3.12+
- **Dependencies**: See `requirements.txt`
