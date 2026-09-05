import os
import json
from openai import OpenAI

SYSTEM_PROMPT = """你是一个专业的 AI 资讯分析助手。请对当天收集到的 AI 相关资讯进行清洗、筛选与摘要整理。

处理要求：
1. 【客观筛选】：从候选列表中筛选出 6-8 条具有技术演进、产品落地或行业参考价值的内容。
2. 【语言风格】：语言客观平实、严谨简洁，避免夸张、修饰性或炒作类词汇（如“重磅”、“突发”、“颠覆”等）。准确传达事件或论文的核心事实与结论。
3. 【分类归纳】：将内容归类至以下三个板块之一：
   - "行业与产品动态"（产品发布、公司动态、行业合作）
   - "技术研究与论文"（模型架构、算法演进、论文成果）
   - "开源项目与工具"（开源模型、开发者工具、应用框架）
4. 【输出格式】：必须严格输出 JSON 格式，不要包含多余的闲聊文字。

JSON Schema：
{
  "date_str": "YYYY年MM月DD日",
  "daily_overview": "用 1-2 句话客观概括今日主要动态与核心关注点",
  "sections": [
    {
      "section_name": "板块名称",
      "news_items": [
        {
          "title": "中文标题（客观准确，概括核心事实）",
          "tag": "标签（如 #大模型 / #Agent / #多模态 / #开源 / #工具）",
          "source": "原始来源名称",
          "link": "原始链接",
          "takeaway": "核心要点（1 句话概括关键信息）",
          "content": "内容说明（2-3 句话：具体内容、技术/业务特点及背景说明）"
        }
      ]
    }
  ]
}
"""

def summarize_with_deepseek(articles: list[dict], api_key: str | None = None) -> dict:
    """使用 DeepSeek 模型对收集到的资讯进行结构化摘要整理"""
    key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("未找到 DEEPSEEK_API_KEY 配置！")

    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    client = OpenAI(
        api_key=key,
        base_url=base_url
    )

    articles_text = ""
    for idx, art in enumerate(articles, 1):
        articles_text += f"\n[{idx}] 标题: {art['title']}\n来源: {art['source']} ({art['category']})\n链接: {art['link']}\n摘要: {art['summary']}\n"

    user_prompt = f"""以下是收集到的资讯候选列表（共 {len(articles)} 条）：
----------------------------------------
{articles_text}
----------------------------------------

请按要求筛选 6-8 条内容并生成结构化 JSON 摘要。"""

    print("[*] 正在调用 DeepSeek 生成结构化摘要...")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )

    raw_content = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw_content)
        print("[+] 结构化摘要生成成功！")
        return data
    except Exception as e:
        print(f"[-] JSON 解析失败: {e}\n原始输出内容:\n{raw_content}")
        raise
