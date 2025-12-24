import streamlit as st
import requests
from datetime import datetime

# Configure the page
st.set_page_config(page_title="Trackster", page_icon="📝", layout="wide")

# API base URL (adjust if your FastAPI runs on a different port)
API_URL = "http://localhost:8000"

# Title
st.title("📝 Trackster - Message Tracker")

# Create two columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Send a Message")

    # Input form
    message_text = st.text_input("Enter your message:", key="message_input")

    if st.button("Send Message", type="primary", use_container_width=True):
        if message_text:
            try:
                response = requests.post(
                    f"{API_URL}/message",
                    json={"text": message_text}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Message sent! Total: {data['total_messages']}")
                    # Clear the input by rerunning
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot connect to API. Make sure FastAPI server is running!")
        else:
            st.warning("Please enter a message first!")

    # Test connection button
    st.divider()
    if st.button("Test API Connection", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/hello")
            if response.status_code == 200:
                data = response.json()
                st.info(f"✅ API Connected: {data['message']}")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ FastAPI server is not running!")

with col2:
    st.subheader("All Messages")

    # Refresh button
    if st.button("🔄 Refresh Messages", use_container_width=True):
        st.rerun()

    # Fetch and display messages
    try:
        response = requests.get(f"{API_URL}/messages")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])

            if messages:
                st.write(f"**Total Messages:** {len(messages)}")
                st.divider()

                # Display each message
                for i, msg in enumerate(reversed(messages), 1):
                    with st.container():
                        # Check if message is a string (old format) or dict (new format)
                        if isinstance(msg, dict):
                            text = msg.get("text", "")
                            timestamp = msg.get("timestamp", "")

                            # Parse and format timestamp
                            try:
                                dt = datetime.fromisoformat(timestamp)
                                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                            except:
                                formatted_time = timestamp

                            st.markdown(f"**{len(messages) - i + 1}.** {text}")
                            st.caption(f"🕒 {formatted_time}")
                        else:
                            # Old format - just a string
                            st.markdown(f"**{len(messages) - i + 1}.** {msg}")

                        st.divider()
            else:
                st.info("No messages yet. Send your first message!")
        else:
            st.error(f"Error fetching messages: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Cannot connect to API. Please start the FastAPI server with:\n\n`uvicorn main:app --reload`")

# Footer with instructions
st.divider()
st.caption("💡 **How to use:** Make sure your FastAPI server is running with `uvicorn main:app --reload`")

# Navigation hint
st.info("📊 Check out the **Stats** page in the sidebar for analytics and experiments!")
