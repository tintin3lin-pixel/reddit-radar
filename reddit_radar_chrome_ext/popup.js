
async function getBaseUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get({ apiBase: "http://localhost:8000" }, (res) => {
      resolve(res.apiBase.replace(/\/$/, ""));
    });
  });
}

function val(id){return document.getElementById(id).value.trim();}

function renderPosts(list) {
  const el = document.getElementById("result");
  el.innerHTML = "";
  if (!Array.isArray(list) || list.length === 0) {
    el.innerHTML = '<div class="small muted">没有结果</div>';
    return;
  }
  list.forEach(p => {
    const d = document.createElement("div");
    d.className = "item";
    d.innerHTML = `
      <div class="sub">r/${p.subreddit} • <span class="muted">${p.created_iso || ""}</span></div>
      <div class="title">${p.title || ""}</div>
      <div class="meta">score: ${p.score} • comments: ${p.num_comments}</div>
      <div class="link"><a href="${p.permalink}" target="_blank">打开帖子</a></div>
    `;
    el.appendChild(d);
  });
}

document.getElementById("btnSearch").addEventListener("click", async () => {
  const btn = document.getElementById("btnSearch");
  btn.disabled = true; btn.textContent = "查询中...";
  try {
    const base = await getBaseUrl();
    const body = {
      subreddits: val("subreddits"),
      keywords: val("keywords"),
      after: val("after"),
      before: val("before"),
      min_score: parseInt(val("min_score") || "3", 10),
      min_comments: parseInt(val("min_comments") || "1", 10),
      max_posts: parseInt(val("max_posts") || "100", 10),
      sort_by: document.getElementById("sort_by").value
    };
    const resp = await fetch(base + "/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await resp.json();
    renderPosts(data.posts || []);
  } catch(e) {
    document.getElementById("result").innerHTML = '<div class="small">请求失败：' + (e.message || e) + '</div>';
  } finally {
    btn.disabled = false; btn.textContent = "搜索帖子（官方 API）";
  }
});

document.getElementById("btnTrending").addEventListener("click", async () => {
  const btn = document.getElementById("btnTrending");
  btn.disabled = true; btn.textContent = "抓取中...";
  try {
    const base = await getBaseUrl();
    const subs = val("subreddits");
    const url = new URL(base + "/api/trending");
    if (subs) url.searchParams.set("subreddits", subs);
    const resp = await fetch(url.toString());
    const data = await resp.json();
    renderPosts(data.items || []);
  } catch(e) {
    document.getElementById("result").innerHTML = '<div class="small">请求失败：' + (e.message || e) + '</div>';
  } finally {
    btn.disabled = false; btn.textContent = "抓取热门（hot / rising / controversial）";
  }
});
