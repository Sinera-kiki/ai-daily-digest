import os
import json
from openai import OpenAI

SYSTEM_PROMPT = """你是一位顶尖的 AI 科技智库主编与资深 AI 产品经理。
你的任务是将当天从全球和国内收集到的 AI 资讯进行深度清洗、筛选与精炼，制作成一份高质量的《全球 AI 前沿早报》。

请遵循以下处理准则：
1. 【严格筛选】：从提供的候选资讯中，筛选出最具行业影响力、技术突破性或产品价值的 6-10 条核心要闻。
2. 【中文精炼】：无论原文是英文还是中文，一律输出高信息密度的专业中文。不要机器翻译感，用通俗地道、严谨的产研与科技语感。
3. 【模块划分】：将选出的条目归类到以下板块之一：
   - "重磅头条 & 产业大事件" (重大模型发布、科技巨头战略、行业风向标)
   - "前沿研究与学术演进" (新架构、顶会/arXiv 突破性论文、算法演进)
   - "开源生态与产品落地" (开源项目、AI Agent 应用、开发者工具、杀手级产品)
4. 【结构化格式】：必须严格输出合法的 JSON 格式，不要添加任何 markdown 代码块外部的闲聊文字。

JSON Schema 结构如下：
{
  "date_str": "YYYY年MM月DD日",
  "daily_overview": "用一两句极具前瞻性的话总结今日 AI 领域的最大看点与核心风向",
  "sections": [
    {
      "section_name": "板块名称",
      "news_items": [
        {
          "title": "中文精炼标题（清晰有力）",
          "tag": "标签（如 #LLM / #Agent / #多模态 / #开源 / #商业化）",
          "source": "原始来源名称",
          "link": "原始链接",
          "takeaway": "核心看点（一句话点出关键突破）",
          "content": "深度解读（2-3句话：具体做了什么、关键亮点、对行业或开发者的意义）"
        }
      ]
    }
  ]
}
"""

def summarize_with_deepseek(articles: list[dict], api_key: str | None = None) -> dict:
    """使用 DeepSeek 大模型对收集到的资讯进行提炼与结构化总结"""
    key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("未找到 DEEPSEEK_API_KEY 环境变量或配置！")

    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    client = OpenAI(
        api_key=key,
        base_url=base_url
    )

    # 组装 Prompt
    articles_text = ""
    for idx, art in enumerate(articles, 1):
        articles_text += f"\n[{idx}] 标题: {art['title']}\n来源: {art['source']} ({art['category']})\n链接: {art['link']}\n摘要: {art['summary']}\n"

    user_prompt = f"""以下是过去 24-48 小时内收集到的 AI 资讯候选列表（共 {len(articles)} 条）：
----------------------------------------
{articles_text}
----------------------------------------

请按照系统提示要求，筛选出最精选的 6-10 条核心要闻，提炼今日 AI 早报，并以纯 JSON 格式返回。"""

    print("[*] 正在调用 DeepSeek-Chat 模型进行智能筛选与深度提炼...")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    raw_content = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw_content)
        print("[+] DeepSeek 结构化总结生成成功！")
        return data
    except Exception as e:
        print(f"[-] JSON 解析失败: {e}\n原始输出内容:\n{raw_content}")
        raise
