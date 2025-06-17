import requests
import pandas as pd
from datetime import datetime

SUBREDDIT = "SMU_Singapore"
URL       = f"https://old.reddit.com/r/{SUBREDDIT}/.json"
HEADERS   = {"User-Agent": "Mozilla/5.0 (HPBInsightsBot/1.0)"}

def fetch_reddit_json(limit=100):
    params = {"limit": limit}
    r = requests.get(URL, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()["data"]["children"]

def normalize(post):
    d = post["data"]
    return {
        "timestamp":    datetime.utcfromtimestamp(d["created_utc"])
                             .strftime("%Y-%m-%d %H:%M:%S"),
        "author":       d.get("author"),
        "title":        d.get("title"),
        "body":         d.get("selftext", ""),         # ← full post text
        "flair":        d.get("link_flair_text") or "",
        "score":        d.get("score"),
        "num_comments": d.get("num_comments"),
        "url":          d.get("permalink", "").join(( "https://old.reddit.com", d.get("permalink","") ))
    }

if __name__ == "__main__":
    posts = fetch_reddit_json(limit=200)
    print(f"🔍 Fetched {len(posts)} items")

    records = [normalize(p) for p in posts]
    df = pd.DataFrame(records)
    
    # reorder to taste
    df = df[[
        "timestamp","author","title","body",
        "flair","score","num_comments","url"
    ]]

    df.to_csv("smu_reddit_full_with_body.csv", index=False)
    print("✅ Written smu_reddit_full_with_body.csv")
