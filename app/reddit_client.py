from praw import Reddit


client = Reddit(
    client_id="k8a8tz48Q_B3eK8WDfMkng",
    client_secret="ZNzO37w4GbIx_S0rBzE2JUOTR9opIw",
    user_agent="Comment Extraction (by u/JaSamBatak)",
)

client.read_only = True

def _extract_comments(submission):
    submission.comments.replace_more(limit=None)
    comments = submission.comments.list()
    return [
        {
            "id": comment.id,
            "author": comment.author.name if comment.author else "[deleted]",
            "body": comment.body,
            "score": comment.score,
            "depth": comment.depth,
        }
        for comment in comments
    ]

def get_reddit_post(url):
    submission = client.submission(url=url)
    submission.comments.replace_more(limit=None)
    post_data = {
        "id": submission.id,
        "title": submission.title,
        "author": submission.author.name if submission.author else "[deleted]",
        "body": submission.selftext,
        "comments": _extract_comments(submission),
        "score": submission.score,
    }
    return post_data
