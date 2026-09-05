import datetime
import os
import sys
from dotenv import load_dotenv

from collector import collect_all_news
from summarizer import summarize_with_deepseek
from mailer import render_html, send_email

def main():
    # 加载本地 .env 文件（如果在本地运行）
    load_dotenv()

    today_str = datetime.datetime.now().strftime("%Y年%m月%d日")
    print(f"==========================================")
    print(f"🚀 AI Daily Digest - 全球前沿要闻早报调度")
    print(f"📅 当前日期: {today_str}")
    print(f"==========================================")

    # 1. 抓取资讯
    articles = collect_all_news(hours_ago=36, max_per_source=5)
    if not articles:
        print("[-] 未获取到任何资讯，流程终止。")
        sys.exit(1)

    # 2. 调用 DeepSeek 提炼
    summary_data = summarize_with_deepseek(articles)
    if "date_str" not in summary_data or not summary_data["date_str"]:
        summary_data["date_str"] = today_str

    # 3. 渲染 HTML
    html_content = render_html(summary_data)

    # 保存一份本地预览
    os.makedirs("dist", exist_ok=True)
    with open("dist/preview.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[+] 已生成本地 HTML 预览文件: dist/preview.html")

    # 4. 发送邮件（如果在本地测试且没有配置邮箱，可跳过）
    if os.getenv("SMTP_USER") and os.getenv("SMTP_PASSWORD"):
        send_email(html_content, subject_date=summary_data.get("date_str", today_str))
    else:
        print("[!] 未检测到 SMTP 配置，已跳过邮件发送步骤（仅生成本地预览）。")

    print("\n🎉 全球 AI 前沿要闻早报任务全部执行完成！")

if __name__ == "__main__":
    main()
