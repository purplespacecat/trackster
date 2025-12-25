# AI Summary Feature Setup Guide

## Overview
The AI summary feature uses Google's Gemini API to generate intelligent summaries of your last 6 notes, providing insights into themes, mood, and patterns.

## Setup Steps

### 1. Get a Gemini API Key

1. Go to **Google AI Studio**: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"** or **"Create API Key"**
3. If prompted, create a new project or select an existing one
4. Click **"Create API key in new project"** (or select existing project)
5. Copy the API key (it will look like: `AIzaSyA...`)

**Important**: Keep this key secret! Don't share it or commit it to git.

### 2. Add API Key to Environment

1. Open the `.env` file in the root of your project (create it if it doesn't exist)
2. Add this line:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with your actual API key
4. Save the file

**Example `.env` file:**
```
GEMINI_API_KEY=AIzaSyBcD1eFgH2iJkLmNoP3qRsTuVwXyZ
```

### 3. Restart Your Servers

The `.env` file is loaded when the servers start, so you need to restart them:

**Terminal 1 - Stop and restart FastAPI:**
- Press `Ctrl+C` to stop
- Run: `uvicorn main:app --reload`

**Terminal 2 - Stop and restart Reflex:**
- Press `Ctrl+C` to stop
- Run: `reflex run`

### 4. Test the Feature

1. Open `http://localhost:3000` in your browser
2. Make sure you have at least a few notes saved
3. Click the **"✨ Generate Summary (Last 6 Notes)"** button
4. Wait a few seconds for the AI to generate the summary
5. The summary will appear in a purple-bordered box above your notes
6. The summary is saved in the database and will persist until you generate a new one

## How It Works

- **On Demand**: Click the button when you want a fresh summary
- **Last Generated**: The most recent summary is loaded when you open the app
- **Persistent**: Summaries are stored in the database (`summaries` table)
- **Smart**: Gemini analyzes your notes for themes, mood, patterns, and insights

## Troubleshooting

### "Error: GEMINI_API_KEY not found"
- Make sure you added the key to `.env` file
- Make sure you restarted both servers after adding the key
- Check that the file is named `.env` (not `.env.txt`)

### "Error generating summary"
- Check your internet connection
- Verify your API key is valid at https://makersuite.google.com/app/apikey
- Make sure you have notes in your database
- Check the FastAPI console for detailed error messages

### Summary takes too long
- This is normal! AI generation can take 5-10 seconds
- The button shows a loading spinner while processing
- Be patient and don't click multiple times

## API Limits

Google Gemini has a free tier with generous limits:
- **Free tier**: 60 requests per minute
- More than enough for personal note-taking use
- Check current limits at: https://ai.google.dev/pricing

## Privacy Note

Your notes are sent to Google's Gemini API for summary generation. If you have privacy concerns about sensitive notes, you may want to:
- Use this feature sparingly
- Only use it for non-sensitive notes
- Consider self-hosting an alternative AI model

---

Enjoy your AI-powered journal summaries! 📝✨
