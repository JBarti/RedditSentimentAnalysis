import streamlit as st
from app.reddit_client import get_reddit_post


def run_sentiment_analysis(url: str, progress_bar):
    """Run sentiment analysis on the given Reddit post URL and update the session state."""
    from app.sentiment import classify_sentiment

    progress_bar.progress(
        0,
        text=f"Fetching reddit post and comments...",
    )
    reddit_post = get_reddit_post(url)

    reddit_post = {
        **reddit_post,
        "sentiment": classify_sentiment(reddit_post["body"])["label"],
        "url": url,
    }

    comments = []
    progess_chunk = 1 / max(len(reddit_post["comments"]), 1)

    for i, comment in enumerate(reddit_post["comments"]):
        progress_bar.progress(
            (i + 1) * progess_chunk,
            text=f"Analyzing comment {len(comments)+1}/{len(reddit_post['comments'])}",
        )
        comment_sentiment = classify_sentiment(comment["body"])["label"]
        comments.append({**comment, "sentiment": comment_sentiment})

    st.session_state.update(
        {
            "reddit_post": reddit_post,
            "comments": comments,
        }
    )
