# Trackster

A general life tracking application that syncs tasks from voice input via Gemini AI. Built with FastAPI for the backend APIs and functionality, with Streamlit for the UI.

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

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Features

- Voice-to-task syncing via Gemini AI
- FastAPI backend for robust API functionality
- Streamlit-based UI for quick prototyping
- Life tracking capabilities (tasks, habits, activities, etc.)

## API Endpoints

- `GET /hello` - Test endpoint
- `POST /message` - Add a message
- `GET /messages` - Retrieve all messages

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
