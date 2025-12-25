from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API with the new SDK
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the client
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def generate_notes_summary(notes: list[dict], count: int = 6) -> str:
    """
    Generate an AI summary of the last N notes using Gemini.

    Args:
        notes: List of note dictionaries with 'text' and 'timestamp' fields
        count: Number of notes that were summarized

    Returns:
        str: AI-generated summary text
    """
    if not client:
        return "Error: GEMINI_API_KEY not found in environment variables. Please add it to your .env file."

    if not notes:
        return "No notes available to summarize."

    # Format notes for the prompt
    notes_text = ""
    for i, note in enumerate(notes, 1):
        timestamp = note.get("timestamp", "")
        text = note.get("text", "")
        notes_text += f"{i}. [{timestamp}] {text}\n"

    # Create the prompt
    prompt = f"""You are analyzing a personal journal. Here are the last {len(notes)} entries:

{notes_text}

Please provide a thoughtful summary that includes:
- A brief overview (2-3 sentences)
- Main themes or recurring topics
- Overall mood or sentiment
- Any notable patterns or insights

Keep the summary concise but insightful."""

    try:
        # gemini-2.5-flash-lite
        #  (most stable free model)
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        )
        return response.text

    except Exception as e:
        # Return the raw error from the API
        return f"API Error: {str(e)}"
