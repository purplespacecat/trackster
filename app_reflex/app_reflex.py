import reflex as rx
import httpx
from datetime import datetime

# API base URL
API_URL = "http://localhost:8000"


class State(rx.State):
    """The app state."""
    messages: list[dict] = []
    message_input: str = ""
    send_status: str = ""
    test_status: str = ""
    delete_status: str = ""

    async def load_messages(self):
        """Load messages from the API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/messages")
                if response.status_code == 200:
                    data = response.json()
                    self.messages = data.get("messages", [])
                else:
                    self.messages = []
        except Exception as e:
            self.messages = []

    async def send_message(self):
        """Send a message to the API"""
        if not self.message_input:
            self.send_status = "Please enter a message first!"
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/message",
                    json={"text": self.message_input}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.send_status = f"Message sent! Total: {data['total_messages']}"
                    self.message_input = ""
                    await self.load_messages()
                else:
                    self.send_status = f"Error: {response.status_code}"
        except Exception as e:
            self.send_status = "Cannot connect to API. Make sure FastAPI server is running!"

    async def delete_message(self, message_id: int):
        """Delete a message by ID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{API_URL}/message/{message_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.delete_status = "Message deleted successfully!"
                    else:
                        self.delete_status = "Message not found"
                    await self.load_messages()
                else:
                    self.delete_status = f"Error: {response.status_code}"
        except Exception as e:
            self.delete_status = "Cannot connect to API"

    async def test_connection(self):
        """Test API connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/hello")
                if response.status_code == 200:
                    data = response.json()
                    self.test_status = f"API Connected: {data['message']}"
                else:
                    self.test_status = f"Error: {response.status_code}"
        except Exception as e:
            self.test_status = "FastAPI server is not running!"


def message_card(msg) -> rx.Component:
    """Render a message card with delete button"""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    msg["text"],
                    font_weight="bold",
                    margin_bottom="5px",
                ),
                rx.text(
                    msg["timestamp"],
                    font_size="0.85em",
                    color="#666",
                ),
                align_items="start",
                spacing="1",
                flex="1",
            ),
            rx.button(
                "Delete",
                on_click=State.delete_message(msg["id"]),
                color_scheme="red",
                size="2",
            ),
            spacing="4",
            align_items="center",
        ),
        padding="15px",
        margin="10px 0",
        border="1px solid #ddd",
        border_radius="8px",
        background_color="#f9f9f9",
    )


def index() -> rx.Component:
    """The main app page"""
    return rx.center(
        rx.container(
            # Header with title and test button
            rx.hstack(
                rx.heading("Trackster - Message Tracker", size="8"),
                rx.button(
                    "Test API Connection",
                    on_click=State.test_connection,
                    size="2",
                ),
                justify="between",
                align_items="center",
                margin_bottom="20px",
            ),
            rx.cond(
                State.test_status != "",
                rx.text(State.test_status, color="#666", margin_bottom="10px"),
            ),
            rx.divider(margin_y="20px"),

            # Send message section
            rx.heading("Send a Message", size="5", margin_bottom="10px"),
            rx.hstack(
                rx.input(
                    placeholder="Type your message here...",
                    value=State.message_input,
                    on_change=State.set_message_input,
                    width="100%",
                    size="3",
                ),
                rx.button(
                    "Send Message",
                    on_click=State.send_message,
                    size="3",
                    color_scheme="blue",
                ),
                spacing="4",
                width="100%",
                margin_bottom="10px",
            ),
            rx.cond(
                State.send_status != "",
                rx.text(State.send_status, margin_bottom="10px"),
            ),
            rx.divider(margin_y="20px"),

            # All messages section
            rx.heading("All Messages", size="5", margin_bottom="10px"),
            rx.button(
                "🔄 Refresh Messages",
                on_click=State.load_messages,
                size="2",
                margin_bottom="15px",
            ),
            rx.cond(
                State.delete_status != "",
                rx.text(State.delete_status, margin_bottom="10px"),
            ),
            rx.cond(
                State.messages.length() > 0,
                rx.vstack(
                    rx.text(f"Total Messages: {State.messages.length()}", font_weight="bold"),
                    rx.foreach(
                        State.messages.reverse(),
                        message_card,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.text("No messages yet. Send your first message!"),
            ),
            rx.divider(margin_y="20px"),
            rx.text(
                "💡 How to use: Make sure your FastAPI server is running with uvicorn main:app --reload",
                color="#666",
                font_size="0.9em",
            ),
            padding="40px",
            max_width="800px",
            on_mount=State.load_messages,
        ),
    )


# Create the app
app = rx.App()
app.add_page(index)
