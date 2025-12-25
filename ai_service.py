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
        # Try multiple models in order of preference
        models_to_try = [
            'gemini-1.5-flash',      # Most stable free model
            'gemini-1.5-flash-8b',   # Smaller, faster variant
            'gemini-2.0-flash-exp',  # Experimental (may not be available)
        ]

        last_error = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                last_error = e
                continue

        # If all failed
        error_msg = str(last_error)
        if "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return "Error: Your API key quota is at 0. Please:\n1. Go to https://aistudio.google.com/apikey\n2. Delete your current API key\n3. Create a NEW API key\n4. Update your .env file with the new key\n5. Restart the server"
        else:
            return f"Error: {error_msg}"

    except Exception as e:
        return f"Error generating summary: {str(e)}"
