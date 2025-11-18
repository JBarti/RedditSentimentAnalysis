import json
import streamlit as st

def load_example_analysis():
    """Load example sentiment analysis data from a JSON file into the session state."""
    try:
        with open("example_sentiment_analysis.json", "r") as f:
            data = json.load(f)
            st.session_state.update(
                {
                    "reddit_post": data["post"],
                    "comments": data["comments"],
                }
            )
    except FileNotFoundError:
        pass
