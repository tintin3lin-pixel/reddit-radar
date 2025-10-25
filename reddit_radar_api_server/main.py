
# main.py — FastAPI backend for Reddit Radar
import os, time, random
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dateutil import parser as dateparser
import praw

# ---------- CORS ----------
app = FastAPI(title="Reddit Radar API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def make_reddit():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "RedditRadar/0.1 by YOUR_USERNAME")
    if not client_id or not client_secret:
        raise RuntimeError("Missing Reddit API creds (REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET)")
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        requestor_kwargs={"timeout": 30},
        ratelimit_seconds=60,
    )
    return reddit

def to_ts(s: str) -> int:
    return int(dateparser.parse(s).timestamp())

class SearchRequest(BaseModel):
    subreddits: Optional[str] = ""  # comma separated
    keywords: Optional[str] = ""
    after: Optional[str] = "2024-01-01"
    before: Optional[str] = datetime.utcnow().strftime("%Y-%m-%d")
    min_score: int = 3
    min_comments: int = 1
    max_posts: int = 100
    sort_by: str = "score"  # score | num_comments | created_utc

@app.get("/ping")
def ping():
    return {"ok": True, "time": datetime.utcnow().isoformat()}

@app.get("/api/trending")
def api_trending(subreddits: Optional[str] = Query(default="ADHD,ADHDWomen,Productivity"),
                 limit_per_feed: int = Query(default=40)):
    reddit = make_reddit()
    subs = [s.strip() for s in (subreddits or "").split(",") if s.strip()]
    items = []
    for sub in subs:
        s = reddit.subreddit(sub)
        feeds = [
            ("hot", s.hot(limit=limit_per_feed)),
            ("rising", s.rising(limit=limit_per_feed)),
            ("controversial", s.controversial(limit=limit_per_feed)),
        ]
        for feed_name, gen in feeds:
            for it in gen:
                created = int(getattr(it, "created_utc", 0) or 0)
                items.append({
                    "feed": feed_name,
                    "subreddit": sub,
                    "id": it.id,
                    "title": it.title or "",
                    "score": int(getattr(it, "score", 0) or 0),
                    "num_comments": int(getattr(it, "num_comments", 0) or 0),
                    "created_utc": created,
                    "created_iso": datetime.utcfromtimestamp(created).strftime("%Y-%m-%d %H:%M:%S"),
                    "permalink": f"https://www.reddit.com{it.permalink}",
                })
        time.sleep(1.0)
    # 简单排序：按得分倒序
    items.sort(key=lambda r: r.get("score", 0), reverse=True)
    return {"items": items[: 3 * limit_per_feed]}

@app.post("/api/search")
def api_search(req: SearchRequest):
    reddit = make_reddit()
    after_ts = to_ts(req.after)
    before_ts = to_ts(req.before)
    subs = [s.strip() for s in (req.subreddits or "ADHD").split(",") if s.strip()]
    kws = [k.strip().lower() for k in (req.keywords or "").split(",") if k.strip()]
    q = " OR ".join([f'\"{k}\"' if " " in k else k for k in kws]) if kws else ""

    all_rows = []
    seen = set()
    search_sorts = ["relevance","comments","top"]
    per_sub_cap = max(400, req.max_posts * 4)

    for sub in subs:
        s = reddit.subreddit(sub)
        for sort_mode in search_sorts:
            gen = s.search(query=q or "*", sort=sort_mode, time_filter="all", limit=per_sub_cap)
            for it in gen:
                sid = it.id
                if sid in seen: continue
                created = int(getattr(it, "created_utc", 0) or 0)
                if not (after_ts <= created <= before_ts): continue
                title = it.title or ""
                selftext = it.selftext or ""
                text = (title + "\n" + selftext).lower()
                if kws and not any(k in text for k in kws): continue
                score = int(getattr(it, "score", 0) or 0)
                num_comments = int(getattr(it, "num_comments", 0) or 0)
                if score < req.min_score or num_comments < req.min_comments: continue
                all_rows.append({
                    "id": sid,
                    "subreddit": str(getattr(it, "subreddit", "")),
                    "title": title,
                    "selftext": selftext,
                    "score": score,
                    "num_comments": num_comments,
                    "created_utc": created,
                    "created_iso": datetime.utcfromtimestamp(created).strftime("%Y-%m-%d %H:%M:%S"),
                    "permalink": f"https://www.reddit.com{it.permalink}",
                    "url": getattr(it, "url", None),
                })
                seen.add(sid)
            if len(all_rows) >= req.max_posts * 3:
                break

    key = req.sort_by if req.sort_by in {"score","num_comments","created_utc"} else "score"
    all_rows.sort(key=lambda r: r.get(key, 0), reverse=True)
    return {"posts": all_rows[: req.max_posts]}
