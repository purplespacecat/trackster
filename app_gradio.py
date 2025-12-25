import gradio as gr
import requests
from datetime import datetime

# API base URL
API_URL = "http://localhost:8000"


def send_message(message_text):
    """Send a message to the API"""
    if not message_text:
        return "Please enter a message first!", None

    try:
        response = requests.post(
            f"{API_URL}/message",
            json={"text": message_text}
        )
        if response.status_code == 200:
            data = response.json()
            return f"Message sent! Total: {data['total_messages']}", ""
        else:
            return f"Error: {response.status_code}", message_text
    except requests.exceptions.ConnectionError:
        return "Cannot connect to API. Make sure FastAPI server is running!", message_text


def get_messages():
    """Fetch all messages from the API"""
    try:
        response = requests.get(f"{API_URL}/messages")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])

            if not messages:
                return "No messages yet. Send your first message!"

            # Format messages for display
            output = f"**Total Messages: {len(messages)}**\n\n"
            output += "---\n\n"

            for i, msg in enumerate(reversed(messages), 1):
                text = msg.get("text", "")
                timestamp = msg.get("timestamp", "")

                # Parse and format timestamp
                try:
                    dt = datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp

                output += f"**{len(messages) - i + 1}.** {text}\n"
                output += f"*{formatted_time}*\n\n"
                output += "---\n\n"

            return output
        else:
            return f"Error fetching messages: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Cannot connect to API. Please start the FastAPI server with: `uvicorn main:app --reload`"


def test_connection():
    """Test API connection"""
    try:
        response = requests.get(f"{API_URL}/hello")
        if response.status_code == 200:
            data = response.json()
            return f"API Connected: {data['message']}"
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "FastAPI server is not running!"


# Build the Gradio interface
with gr.Blocks(title="Trackster", theme=gr.themes.Soft()) as app:
    # Header with title and API test button
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("# Trackster - Message Tracker")
        with gr.Column(scale=1):
            test_btn = gr.Button("Test API Connection", size="sm")
            test_status = gr.Textbox(label="", interactive=False, lines=1, show_label=False, container=False)

    gr.Markdown("---")

    # Top section - Send message
    send_btn = gr.Button("Send Message", variant="primary", size="lg")
    message_input = gr.Textbox(
        label="",
        placeholder="Type your message here...",
        lines=1,
        show_label=False
    )
    send_status = gr.Textbox(label="", interactive=False, lines=1, show_label=False, container=False)

    gr.Markdown("---")

    # Middle section - Display messages
    gr.Markdown("### All Messages")
    messages_display = gr.Markdown(
        value="Click 'Refresh Messages' to load messages"
    )
    refresh_btn = gr.Button("🔄 Refresh Messages", size="sm")

    gr.Markdown("---")
    gr.Markdown("💡 **How to use:** Make sure your FastAPI server is running with `uvicorn main:app --reload`")

    # Event handlers
    send_btn.click(
        fn=send_message,
        inputs=[message_input],
        outputs=[send_status, message_input]
    ).then(
        fn=get_messages,
        outputs=[messages_display]
    )

    refresh_btn.click(
        fn=get_messages,
        outputs=[messages_display]
    )

    test_btn.click(
        fn=test_connection,
        outputs=[test_status]
    )

    # Load messages on startup
    app.load(
        fn=get_messages,
        outputs=[messages_display]
    )


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
