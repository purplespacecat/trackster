import streamlit as st

# Configure the page
st.set_page_config(page_title="Stats - Trackster", page_icon="📊", layout="wide")

# Title
st.title("📊 Stats")

st.write("This is a blank stats page for experimenting with Streamlit components!")

# Add some basic sections to get you started
st.divider()

st.subheader("Experiment Area")
st.write("Try adding different Streamlit components here:")

# Example placeholder areas
col1, col2 = st.columns(2)

with col1:
    st.info("Column 1 - Add your components here")

with col2:
    st.info("Column 2 - Add your components here")

st.divider()

# Footer
st.caption("💡 Check out the [Streamlit docs](https://docs.streamlit.io) for component examples!")
