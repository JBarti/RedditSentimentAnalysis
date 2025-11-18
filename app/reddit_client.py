from praw import Reddit
import tomllib


with open("secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

    if not secrets.get("reddit"):
        raise ValueError("Reddit credentials not found in secrets.toml")

    client = Reddit(
        client_id=secrets["reddit"]["client_id"],
        client_secret=secrets["reddit"]["client_secret"],
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
