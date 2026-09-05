"""
AI 资讯数据源配置列表 (RSS / APIs)
覆盖国际顶尖 Labs、学术前沿、开源社区及科技媒体
"""

SOURCES = [
    # --- 国际顶尖 AI 实验室 ---
    {
        "name": "OpenAI News",
        "category": "行业巨头",
        "url": "https://openai.com/news/rss.xml",
        "type": "rss"
    },
    {
        "name": "Anthropic News",
        "category": "行业巨头",
        "url": "https://www.anthropic.com/news/rss.xml",
        "type": "rss"
    },
    {
        "name": "Google AI Blog",
        "category": "行业巨头",
        "url": "https://blog.google/technology/ai/rss/",
        "type": "rss"
    },

    # --- 产业与科技商业 ---
    {
        "name": "TechCrunch AI",
        "category": "产业与商业",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "type": "rss"
    },
    {
        "name": "The Verge AI",
        "category": "产业与商业",
        "url": "https://www.theverge.com/rss/artificial-intelligence/index.xml",
        "type": "rss"
    },
    {
        "name": "MIT Technology Review AI",
        "category": "前沿洞察",
        "url": "https://www.technologyreview.com/feed/",
        "type": "rss"
    },
    {
        "name": "MarkTechPost AI",
        "category": "学术与开源",
        "url": "https://www.marktechpost.com/feed/",
        "type": "rss"
    },
    
    # --- 前沿研究与技术专家 ---
    {
        "name": "Simon Willison AI Blog",
        "category": "专家实践",
        "url": "https://simonwillison.net/atom/everything/",
        "type": "rss"
    },
    {
        "name": "arXiv CS.AI (人工智能)",
        "category": "前沿论文",
        "url": "https://rss.arxiv.org/rss/cs.AI",
        "type": "rss"
    },
    {
        "name": "arXiv CS.CL (语言与大模型)",
        "category": "前沿论文",
        "url": "https://rss.arxiv.org/rss/cs.CL",
        "type": "rss"
    },

    # --- 国内优质 AI 资讯 ---
    {
        "name": "机器之心 (Synced)",
        "category": "国内前沿",
        "url": "https://www.jiqizhixin.com/rss",
        "type": "rss"
    },
    {
        "name": "InfoQ 人工智能",
        "category": "工程实践",
        "url": "https://www.infoq.cn/feed",
        "type": "rss"
    }
]
