import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from jinja2 import Environment, FileSystemLoader

def render_html(data: dict) -> str:
    """使用 Jinja2 模板渲染 HTML 邮件"""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("email.html")
    return template.render(data=data)

def send_email(html_content: str, subject_date: str) -> None:
    """通过 163 邮箱 SMTP 服务发送邮件"""
    smtp_server = os.getenv("SMTP_SERVER", "smtp.163.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    
    sender_email = os.getenv("SMTP_USER")
    sender_password = os.getenv("SMTP_PASSWORD")  # 163 授权码
    receiver_email = os.getenv("RECEIVER_EMAIL", sender_email)
    receiver_name = os.getenv("RECEIVER_NAME", "婉婷")

    if not sender_email or not sender_password:
        raise ValueError("未配置 SMTP_USER 或 SMTP_PASSWORD (邮箱授权码)！")

    subject = f"⚡ 全球 AI 前沿早报 | {subject_date}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(subject, "utf-8")
    # 使用标准 formataddr 规范发件人和收件人昵称
    msg["From"] = formataddr((str(Header("AI 前沿早报", "utf-8")), sender_email))
    msg["To"] = formataddr((str(Header(receiver_name, "utf-8")), receiver_email))

    # 邮件正文 (HTML)
    html_part = MIMEText(html_content, "html", "utf-8")
    msg.attach(html_part)

    print(f"[*] 正在通过 {smtp_server}:{smtp_port} 连接 SMTP 服务器...")
    
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
            server.starttls()
            
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()
        print(f"[+] 邮件发送成功！已成功投递至: {receiver_email} ({receiver_name})")
    except Exception as e:
        print(f"[-] 邮件发送失败: {e}")
        raise
