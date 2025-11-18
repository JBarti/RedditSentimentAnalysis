import streamlit as st
import pandas as pd
from app.dashboard_helpers.avatar import avatar
from plotly import express as px
from wordcloud import WordCloud

from app.dashboard_helpers.load_example_analysis import load_example_analysis
from app.dashboard_helpers.run_sentiment_analysis import run_sentiment_analysis
from app.dashboard_helpers.mappings import sentiment_color_map, sentiment_emoji_map, sentiment_groups


load_example_analysis()

reddit_post = st.session_state.get("reddit_post")
comments = st.session_state.get("comments", [])
comments_df = pd.DataFrame(comments)


# -------
# Sidebar
# ------- 

with st.sidebar:
    min_depth = int(comments_df["depth"].min())
    max_depth = int(comments_df["depth"].max())

    min_depth_select, max_depth_select = st.select_slider(
        label="Comment depth",
        options=list(range(min_depth, max_depth + 1)),
        value=(min_depth, max_depth),
    )

    st.markdown("---")
    st.title("Table Of Contents")
    st.markdown("""
                - [Input and Run Button](#run)
                - [Reddit Post](#reddit-post)
                - [Number of posts per Sentiment](#posts-per-sentiment)
                - [Score Distribution by Sentiment](#score-distribution)
                - [Comment Score vs Sentiment](#score-vs-sentiment)
                - [Word Clouds by Sentiment](#word-clouds)

                ### Reach out
                 - [Contact](#contact)
                """)
    st.sidebar.markdown("---")
    st.sidebar.write("© 2025 Josip Bartulović")

# -------------------------------
# Section 1: Input and Run Button
# -------------------------------

st.title("Analyze the sentiment of your Reddit post", anchor="run")
st.markdown(avatar(
    image_url="https://media.licdn.com/dms/image/v2/D4D03AQG7LSfIv_BqjA/profile-displayphoto-crop_800_800/B4DZoQi_VRIAAI-/0/1761214199526?e=1764806400&v=beta&t=W7tN9vlkhI-5JFmx5PQssbS-mdsVZJd3bPpnonJI9Ic",
    name="Josip Bartulović",
    occupation="Data Specialist | Automation Enthusiast | Tech Nerd",
    size=40,
), unsafe_allow_html=True)
st.divider()
st.write("""
         Enter the URL to a post and this tool will analyze the sentiment of the post and the comments.
         Click "Run" to see the sentiment analysis results.
         """)

st.text_input("Link to reddit post", key="post_url")
run_button = st.button("Run", key="run_button")

if run_button:
    progress_bar = st.progress(0.1, text="Running sentiment analysis...")
    st.query_params["url"] = st.session_state.post_url
    run_sentiment_analysis(st.session_state.post_url, progress_bar)


st.divider()

# ----------------------
# Section 2: Reddit Post 
# ----------------------

if reddit_post:
    post_container = st.container(border=True)
    post_container.header(f"{reddit_post["title"]}", anchor="reddit-post")
    post_container.write(f"_By: {reddit_post["author"]}_")
    post_container.write(f"[Original Post]({reddit_post["url"]})")
    post_container.write(f"{reddit_post["body"]}")

    score = reddit_post.get("score", 0)
    score_color = "green" if score >= 0 else "red"
    score_badge = f":{score_color}-badge[:material/thumbs_up_down: {score}]"

    post_sentiment = reddit_post["sentiment"]
    sentiment_emoji = sentiment_emoji_map.get(post_sentiment, "❓")
    sentiment_color = sentiment_color_map.get(post_sentiment, "gray")
    sentiment_badge = f":{sentiment_color}-badge[{sentiment_emoji} {post_sentiment}]"

    post_container.write(f"{score_badge} {sentiment_badge}")

# ----------------------
# Section 3: Key Metrics
# ----------------------

sentiment_groups_list = [
    sentiment_groups.get(comment["sentiment"], "neutral")
    for comment in comments
]
sentiment_group_counts = pd.Series(sentiment_groups_list).value_counts()

col1, col2, col3 = st.columns(3)
col1.metric("Total Comments", len(comments))
col2.metric("Positive Comments", sentiment_group_counts.get("positive", 0))
col3.metric("Negative Comments", sentiment_group_counts.get("negative", 0))
st.divider()



comments_df = comments_df[
    (comments_df["depth"] >= min_depth_select)
    & (comments_df["depth"] <= max_depth_select)
]

# -----------------------------------------
# Section 4: Overall Sentiment Distribution
# -----------------------------------------

sentiment_counts = comments_df["sentiment"].value_counts()

st.subheader("Number of posts per Sentiment", anchor="posts-per-sentiment")
st.write("""
         How many comments belong to each sentiment category.
         This gives an overview of the emotional tone of the discussion.
         """)

chart_tab, table_tab = st.tabs(["📊 Chart", "📄 Table"])

col1, col2 = chart_tab.columns([3, 1], vertical_alignment="center")
fig_pie = px.pie(
    names=sentiment_counts.index,
    values=sentiment_counts.values,
    color=sentiment_counts.index,
    color_discrete_map=sentiment_color_map,
)
col1.plotly_chart(fig_pie)

col2.table(sentiment_counts)

st.divider()

table_tab.dataframe(comments_df[["sentiment", "body", "author", "score", "depth"]], hide_index=True)


# ---------------------------------------------
# Section 5: Comment Sentiment Score Distribution
# ---------------------------------------------

st.subheader("Score Distribution by Sentiment", anchor="score-distribution")
st.write("""
         How comment scores vary across different sentiment categories.
         This can help identify which sentiments resonate more with the community.

         Even if there is less comments of a certain sentiment,
         they might have higher scores, meaning they are more impactful.
         """)
sentiment_scores = comments_df.groupby("sentiment")["score"] \
    .agg(["mean", "max", "sum"])
sentiment_scores["mean"] = sentiment_scores["mean"].round(2).map("{:.2f}".format)

col1, col2 = st.columns([5, 3], vertical_alignment="center")

fig_bar = px.histogram(
    comments_df,
    y="score",
    x="sentiment",
    color="sentiment",
    color_discrete_map=sentiment_color_map,
    labels={"sentiment": "Sentiment", "count": "Number of Comments"},
)
col1.plotly_chart(fig_bar)
col2.table(sentiment_scores)

st.divider()

# -------------------------------
# Section 6: Comment Score vs Sentiment
# -------------------------------

st.subheader("Comment Score vs Sentiment", anchor="score-vs-sentiment")

st.write("""
         Explore the relationship between comment length and score across different sentiments.
         Longer comments might provide more context and could be rated differently based on their sentiment.
         """)

comments_df_post_length = comments_df.assign(body_length=comments_df["body"].str.len())
fig_scatter = px.scatter(
    comments_df_post_length,
    x="body_length",
    y="score",  # just for visualization, can use jitter if needed
    color="sentiment",
    hover_data=["author", "sentiment", "score"],
    color_discrete_map=sentiment_color_map,
)
st.plotly_chart(fig_scatter)
st.divider()

# -------------------------------------
# Section 7: Word Clouds per Sentiment
# -------------------------------------

st.subheader("Word Clouds by Sentiment", anchor="word-clouds")
st.write("""
         Visualize the most common words used in comments for each sentiment category.
         This helps identify prevalent themes and topics associated with different emotions.
         """)
worldcloud_layout = [
    *st.columns(2, border=True),
    *st.columns(2, border=True),
    *st.columns(2, border=True),
    *st.columns(1, border=True, width=400),
]
for i, sentiment in enumerate(sentiment_color_map.keys()):
    column = worldcloud_layout[i]
    text = " ".join([c["body"] for c in comments if c["sentiment"] == sentiment]) or "NONE"
    if text:
        wordcloud = WordCloud(width=400, height=200, background_color="white").generate(text)
        column.write(f"**{sentiment.capitalize()} comments**")
        column.image(wordcloud.to_array())

# ----------------
# Section 8: Contact
# ----------------

st.write("""
         <section style="background-color: #f8fafc; padding: 3rem 1rem; text-align: center; border-radius: 1rem; max-width: 800px; margin: 2rem auto; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
         <h2 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem; color: #111827;">
         I make data easy to find, trust, and use.
         </h2>
         <p style="font-size: 1.1rem; color: #374151; margin-bottom: 2rem;">
         Hi, my name is <u>Josip Bartulović</u>. I help businesses streamline their data processes, automate repetitive tasks and build data products that drive growth.
         <br>
         If you're tired of chasing reports and messy spreadsheets, let’s talk about automating it all.
         </p>
         <a href="https://calendly.com/josip-bartulovic3/30min" style="background-color: #2563eb; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; transition: background-color 0.3s;">
         Book a Call
         </a>
         <a href="mailto:josip.bartulovic3@gmail.com" style="margin-left: 10px; background-color: #10b981; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; transition: background-color 0.3s;">
         Email me
         </a>
         </section>
         """, unsafe_allow_html=True)
