# 🚀 Reddit Radar — 你的 Reddit 热点雷达插件 | Lightweight Reddit Trend Radar

> 用最简单的方式，快速追踪 Reddit 上的热点话题、真实痛点与上升趋势。  
> Track trending topics, real user pain points, and rising discussions on Reddit.

---

## ✨ 功能 / Features
- 🔍 关键词热帖检索（子板块/时间/分数/评论阈值）  
- 📈 热门流：hot / rising / controversial  
- 🧠 趋势信号：活跃小组、上升话题、痛点讨论  
- 🧩 轻量架构：Chrome 插件 + FastAPI 后端（官方 Reddit API）  
- 🪄 开源可扩展 / Open source & extensible

---

## 📦 目录 / Structure

```plaintext
reddit-radar/
├── extension/      # Chrome Extension front-end
├── api-server/     # FastAPI backend (official Reddit API)
└── assets/         # screenshots & diagrams
```

---

## 🧭 系统结构 / System Diagram

```plaintext
Chrome Extension  →  FastAPI Backend  →  Reddit Official API
(Keyword UI)         (HTTP JSON)         (hot/rising/search)
```

---

## 🪄 快速开始 / Quick Start

### 🖥️ 后端 / Backend

```bash
pip install -r api-server/requirements.txt
export REDDIT_CLIENT_ID=your_id
export REDDIT_CLIENT_SECRET=your_secret
export REDDIT_USER_AGENT="RedditRadar/0.1"
uvicorn main:app --reload --port 8000
```

---

### 🧩 插件 / Extension

1. 打开 `chrome://extensions/`  
2. 开启「开发者模式」 / Enable Developer Mode  
3. 点击「加载已解压的扩展」 / Load unpacked  
4. 选择 `extension` 文件夹

---

## 🚀 使用 / Use

- 输入 `subreddits` 和 `keywords`  
- 点击 “Search” 或 “Trending”  
- 浏览结果

```plaintext
Enter `subreddits` & `keywords` → Hit “Search” or “Trending” → browse results
```

---

## ☁️ 可选：云端部署 / Optional Deploy

- 使用 [Railway](https://railway.app) 或 [Render](https://render.com) 免费托管后端  
- 把插件 Options 里的 API Base 改为你的云端地址

---

## 📸 截图 / Screenshots

（把图片放到 ./assets/，然后在这里插入）

```markdown
![popup](./assets/popup.png)
![options](./assets/options.png)
![trending](./assets/trending.png)
```

---

## 🪪 License

MIT License · 欢迎 fork、共创和迭代 🚀

---

## 📬 联系方式 / Contact

- 😎 作者 / Author: **@chouchou_ai**  
- 📮 邮箱 / Email: `tintin3lin@gmail.com`  
- 🧠 Issue: 欢迎提出建议 / 反馈
