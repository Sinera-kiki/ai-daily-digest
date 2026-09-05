# AI Daily Digest

一个基于 Python 与 GitHub Actions 的轻量级 AI 资讯自动化整理与邮件推送工具。

系统每日定时从各大技术媒体、官方博客和论文预印本平台抓取最新的 AI 相关资讯，调用 DeepSeek 模型进行去重、筛选与摘要生成，并排版为 HTML 邮件发送至指定邮箱。

---

## 功能特性

- **多源数据采集**：支持主流 AI 实验室（OpenAI、Anthropic 等）、科技媒体（TechCrunch、MIT Tech Review 等）及学术预印本（arXiv）的 RSS 订阅。
- **结构化摘要生成**：利用 DeepSeek 模型对候选资讯进行清洗与提炼，输出包含核心要点与背景说明的结构化内容。
- **HTML 邮件推送**：支持响应式邮件模板，清晰呈现分类资讯与原文链接。
- **定时自动化调度**：基于 GitHub Actions 定时触发（Cron），无需独立部署常驻服务器。

---

## 目录结构

```text
ai-daily-digest/
├── .github/
│   └── workflows/
│       └── daily_digest.yml   # GitHub Actions 定时工作流配置
├── templates/
│   └── email.html             # HTML 邮件模板
├── sources.py                 # 订阅源列表配置
├── collector.py               # RSS 抓取与文本过滤模块
├── summarizer.py              # LLM 摘要与结构化处理模块
├── mailer.py                  # SMTP 邮件发送模块
├── main.py                    # 主执行入口
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量配置示例
└── README.md                  # 项目说明
```

---

## 部署与配置说明

### 1. 准备配置项

- **DeepSeek API Key**：在 [DeepSeek 开放平台](https://platform.deepseek.com/) 申请。
- **SMTP 服务凭证**：开启邮箱的 SMTP 服务并获取授权码（如 163 邮箱的客户端授权密码）。

### 2. 配置 GitHub Actions Secrets

在 GitHub 仓库中进入 `Settings` -> `Secrets and variables` -> `Actions`，添加以下环境变量：

| 变量名 | 说明 |
| :--- | :--- |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `SMTP_USER` | 发件邮箱账号 |
| `SMTP_PASSWORD` | 发件邮箱 SMTP 授权码 |
| `RECEIVER_EMAIL` | 接收资讯的邮箱地址 |
| `RECEIVER_NAME` | 收件人名称（可选，默认「婉婷」） |

### 3. 定时调度说明

工作流默认配置在 `.github/workflows/daily_digest.yml` 中：
- 触发时间：每天北京时间 10:00（UTC 02:00）。
- 支持在 GitHub 仓库的 `Actions` 页面手动触发执行（`workflow_dispatch`）。
