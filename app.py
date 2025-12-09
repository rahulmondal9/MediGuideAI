# app.py (or your top-level file)
import streamlit as st

# MUST be first Streamlit call in the process
st.set_page_config(
    page_title="MediGuideAI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import the rest of your app
from ui import main

if __name__ == "__main__":
    main()
