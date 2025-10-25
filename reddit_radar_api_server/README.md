
# Reddit Radar API Server (FastAPI)

## Setup
```bash
pip install -r requirements.txt
export REDDIT_CLIENT_ID=your_id
export REDDIT_CLIENT_SECRET=your_secret
export REDDIT_USER_AGENT="RedditRadar/0.1 by YOUR_USERNAME"
uvicorn main:app --reload --port 8000
```

## Endpoints
- `GET /ping` → health check
- `GET /api/trending?subreddits=ADHD,Productivity` → hot/rising/controversial aggregated
- `POST /api/search` → JSON body:
```json
{
  "subreddits": "ADHD,ADHDWomen",
  "keywords": "ADHD, focus, pain point",
  "after": "2022-01-01",
  "before": "2025-10-25",
  "min_score": 3,
  "min_comments": 1,
  "max_posts": 100,
  "sort_by": "score"
}
```
- CORS 已开启，默认允许来自所有来源（便于浏览器扩展调用）。
