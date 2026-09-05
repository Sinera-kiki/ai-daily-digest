import datetime
import html
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import feedparser
import requests
from sources import SOURCES

def clean_html(text: str) -> str:
    """去除 HTML 标签并清理空白字符"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_entry_date(entry) -> datetime.datetime:
    """解析条目的发布时间，解析失败则返回当前时间"""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime.datetime(*entry.updated_parsed[:6], tzinfo=datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc)

def fetch_feed(source: dict, hours_ago: int = 48, max_per_source: int = 5) -> list[dict]:
    """抓取单个 RSS 源最近指定小时内的数据"""
    results = []
    cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours_ago)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(source["url"], headers=headers, timeout=8)
        if response.status_code != 200:
            return results
        
        feed = feedparser.parse(response.content)
        for entry in feed.entries:
            pub_date = parse_entry_date(entry)
            
            # 时间过滤：只保留指定时间窗口内的文章（如无明确时间则默认保留）
            if pub_date and pub_date < cutoff_time:
                continue

            title = clean_html(getattr(entry, "title", ""))
            summary = clean_html(getattr(entry, "summary", getattr(entry, "description", "")))
            link = getattr(entry, "link", "")

            if not title or not link:
                continue

            results.append({
                "title": title,
                "link": link,
                "summary": summary[:400],
                "published_at": pub_date.strftime("%Y-%m-%d %H:%M"),
                "source": source["name"],
                "category": source["category"]
            })
            if len(results) >= max_per_source:
                break
    except Exception as e:
        # print(f"[-] 抓取源 {source['name']} 超时或跳过: {e}")
        pass
    
    return results

def collect_all_news(hours_ago: int = 48, max_per_source: int = 5) -> list[dict]:
    """并发抓取并汇聚所有来源的资讯，并去重"""
    all_articles = []
    seen_titles = set()

    print(f"[*] 开始并发请求 {len(SOURCES)} 个前沿 AI 资讯渠道...")

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_feed, src, hours_ago, max_per_source): src for src in SOURCES}
        for future in as_completed(futures):
            src = futures[future]
            try:
                articles = future.result()
                if articles:
                    print(f"[+] [{src['name']}] 成功获取 {len(articles)} 条资讯")
                    for art in articles:
                        norm_title = art["title"].lower().strip()[:30]
                        if norm_title in seen_titles:
                            continue
                        seen_titles.add(norm_title)
                        all_articles.append(art)
                else:
                    print(f"[-] [{src['name']}] 暂无更新或连接受限")
            except Exception as exc:
                print(f"[-] [{src['name']}] 请求发生异常: {exc}")

    print(f"[*] 汇总完成，共收集到 {len(all_articles)} 条有效候选资讯。")
    return all_articles
