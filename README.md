# ⚡ AI Daily Digest (全球 AI 前沿早报自动化推送)

基于 **Python + DeepSeek 大模型 + 163 邮箱 SMTP + GitHub Actions** 的零成本、全自动 Serverless AI 要闻日报推送系统。

每天早上 **10:00（北京时间）** 自动聚合全球顶级 AI Labs（OpenAI, Anthropic 等）、前沿学术论文（HuggingFace, arXiv）及国内外科技产业动态，经 DeepSeek 深度清洗提炼后，排版成高颜值响应式 HTML 早报发送至你的个人邮箱。

---

## 🌟 核心特性

- **多源智能聚合**：覆盖 OpenAI, Anthropic, TechCrunch AI, HuggingFace Daily Papers, arXiv (AI/CL), 机器之心, 量子位, 36氪等顶尖渠道。
- **DeepSeek 智能提炼**：拒绝机翻与流水账，自动去重、提炼核心突破（Takeaways）、深度解读与产业/技术标签分类。
- **高颜值响应式排版**：Linear / Vercel 极简现代风格 HTML 邮件模板，移动端与 PC 端自适应舒适阅读。
- **0 成本 Serverless 运行**：依托 GitHub Actions 定时调度 Cron，无需自建或租用云服务器，开箱即用。

---

## 🛠️ 技术栈与目录结构

```text
ai-daily-digest/
├── .github/
│   └── workflows/
│       └── daily_digest.yml   # GitHub Actions 定时触发工作流 (每天 10:00 AM)
├── templates/
│   └── email.html             # 高颜值响应式 HTML 早报邮件模板
├── sources.py                 # 资讯订阅源配置 (RSS / 媒体列表)
├── collector.py               # 多源抓取、时间窗口过滤与文本清洗
├── summarizer.py              # DeepSeek API 结构化提炼
├── mailer.py                  # HTML 模板渲染与 163 SMTP 邮件投递
├── main.py                    # 主执行入口
├── requirements.txt           # Python 依赖清单
├── .env.example               # 本地环境变量配置参考
└── README.md                  # 项目说明与部署指南
```

---

## 🚀 极速部署指南（5 分钟完成）

### 第一步：准备必要凭证

#### 1. 获取 163 邮箱 SMTP 授权码
1. 电脑端登录 [163 邮箱网页版](https://mail.163.com/)。
2. 点击顶部导航栏的 **「设置」** → **「POP3/SMTP/IMAP」**。
3. 勾选并开启 **「POP3/SMTP服务」**。
4. 点击 **「新增授权密码」**（按提示发送短信验证），系统会生成一串 **16 位字母授权码**（妥善保存，这就是 `SMTP_PASSWORD`，**不是**邮箱的登录密码）。

#### 2. 获取 DeepSeek API Key
1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)。
2. 在左侧菜单点击 **「API Keys」** → 创建并复制你的 `API Key`。

---

### 第二步：上传代码至你的 GitHub 仓库

1. 在 GitHub 上新建一个仓库（例如命名为 `ai-daily-digest`）。
2. 将本项目代码推送到该仓库：

```bash
git init
git add .
git commit -m "feat: init AI Daily Digest system"
git branch -M main
git remote add origin https://github.com/你的GitHub用户名/ai-daily-digest.git
git push -u origin main
```

---

### 第三步：在 GitHub 仓库配置 Secrets（安全环境变量）

进入你的 GitHub 仓库页面：
1. 点击顶部菜单的 **`Settings`**。
2. 在左侧栏点击 **`Secrets and variables`** → **`Actions`**。
3. 点击绿色按钮 **`New repository secret`**，逐一添加以下 4 个密钥：

| Secret 名称 | 说明与示例值 |
| :--- | :--- |
| `DEEPSEEK_API_KEY` | 你的 DeepSeek API Key（如 `sk-xxxxxx`） |
| `SMTP_USER` | 你的 163 邮箱账号（如 `dwt15229556298@163.com`） |
| `SMTP_PASSWORD` | 第一步获取的 **16 位 SMTP 授权码** |
| `RECEIVER_EMAIL` | 接收早报的邮箱地址（如 `dwt15229556298@163.com`） |

*(注：如果需要修改 DeepSeek 接口地址，可额外添加 `DEEPSEEK_BASE_URL`，默认为 `https://api.deepseek.com`)*

---

### 第四步：立即手动测试运行

1. 进入 GitHub 仓库的 **`Actions`** 选项卡。
2. 在左侧点击工作流 **`AI Daily Digest Push`**。
3. 点击右侧的 **`Run workflow`** 下拉按钮 → 点击绿色的 **`Run workflow`**。
4. 等待 30~60 秒左右运行完毕，打开你的 163 邮箱，即可看到第一封精美的《全球 AI 前沿早报》！

---

## ⏰ 定时任务说明与个性化定制

- **推送时间**：默认在 `.github/workflows/daily_digest.yml` 中配置为每天北京时间 **10:00**（即 UTC 时间 `02:00`，cron: `'0 2 * * *'`）。
- **增加/修改订阅源**：直接编辑 `sources.py` 文件，添加你感兴趣的 RSS 订阅地址即可。
- **调整总结偏好**：可以在 `summarizer.py` 的 `SYSTEM_PROMPT` 中调整关注板块、语言风格或筛选条数。
