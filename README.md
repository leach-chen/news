# 每日科技资讯推送

每天早上自动抓取科技资讯并推送到微信的工作流。

## 功能

- 自动抓取过去24小时的科技资讯
- 支持多个RSS源：36氪、虎嗅、爱范儿、TechCrunch
- 每天早上7点自动运行
- 通过Server酱推送到微信

## 部署步骤

### 第一步：注册 Server酱

1. 打开 [Server酱官网](https://sct.ftqq.com/)，使用GitHub账号登录
2. 登录后，在首页找到 **"消息通道"** → **"微信通知"**
3. 扫码关注 Server酱 的微信公众号（必须步骤，否则收不到推送）
4. 返回页面，点击 **"生成SendKey"**
5. 复制保存好你的 SendKey（格式类似 `SCTxxxxxxxxxxxxx`）

### 第二步：配置 GitHub Secrets

1. 打开仓库页面：https://github.com/wudengyao/news
2. 点击 **Settings**（设置）
3. 在左侧找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 填写：
   - **Name**: `SEND_KEY`
   - **Secret**: 粘贴你刚才复制的 SendKey
6. 点击 **Add secret** 保存

如图所示：
```
┌─────────────────────────────────────┐
│  Secrets and variables / Actions   │
│  ┌───────────────────────────────┐  │
│  │ Name: SEND_KEY                │  │
│  │ Secret: SCTxxxxxxxxxxxxx      │  │
│  └───────────────────────────────┘  │
│           [Add secret]              │
└─────────────────────────────────────┘
```

### 第三步：手动测试

1. 进入仓库的 **Actions** 页面：
   https://github.com/wudengyao/news/actions

2. 在左侧找到 **"每日科技资讯推送"**

3. 点击进入后，点击 **"Run workflow"**
   ```
   ┌─────────────────────────────┐
   │  每日科技资讯推送            │
   │  ┌─────────────────────┐    │
   │  │ Run workflow  ▼    │    │
   │  └─────────────────────┘    │
   └─────────────────────────────┘
   ```

4. 选择分支（默认 main），点击 **"Run workflow"** 确认

5. 等待几秒钟，刷新页面，点击最新的运行记录

6. 查看运行结果：
   - 如果看到绿色的 ✅ ，说明推送成功
   - 如果看到红色的 ❌ ，点击查看错误信息

### 第四步：验证微信推送

检查你的微信是否收到推送消息。如果没有收到：
1. 确认是否已关注 Server酱 微信公众号
2. 检查 SendKey 是否正确配置
3. 查看 Actions 运行日志中的错误信息

## 文件说明

```
news/
├── fetch_news.py              # Python 抓取脚本
├── requirements.txt           # Python 依赖
├── README.md                  # 说明文档
└── .github/workflows/
    └── daily_tech_news.yml   # GitHub Actions 工作流
```

## 定时任务

工作流每天 **北京时间早上7点** 自动运行。

如需调整时间，修改 `.github/workflows/daily_tech_news.yml` 中的 cron 表达式：

```yaml
schedule:
  # 每天7点运行 (UTC 23:00 = 北京时间 7:00)
  - cron: '0 23 * * *'
```

常见时间对照表：

| 北京时间 | UTC时间   | cron表达式      |
|---------|----------|----------------|
| 6:00    | 22:00    | `0 22 * * *`   |
| 7:00    | 23:00    | `0 23 * * *`   |
| 8:00    | 0:00     | `0 0 * * *`    |
| 9:00    | 1:00     | `0 1 * * *`    |

如需了解 cron 表达式格式，请参考 [GitHub Actions 文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)。

## 本地运行（可选）

如果你想在本地测试脚本：

```bash
# 1. 克隆仓库
git clone https://github.com/wudengyao/news.git
cd news

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置环境变量（Linux/Mac）
export SEND_KEY="你的SendKey"

# 4. 运行脚本
python fetch_news.py
```

Windows 用户使用：
```cmd
# 设置环境变量
set SEND_KEY=你的SendKey

# 运行脚本
python fetch_news.py
```

## RSS 源

- 36氪: <https://www.36kr.com/feed/>
- 虎嗅网: <https://www.huxiu.com/rss.xml>
- 爱范儿: <https://www.ifanr.com/feed/>
- TechCrunch: <https://techcrunch.com/feed/>

如需添加更多RSS源，修改 `fetch_news.py` 中的 `RSS_SOURCES` 列表。

## 常见问题

**Q: 为什么收不到微信推送？**
A: 请确认已关注 Server酱 微信公众号，并检查 SendKey 是否正确。

**Q: 可以修改推送时间吗？**
A: 可以，修改工作流文件中的 cron 表达式即可。

**Q: 如何查看历史推送记录？**
A: 在 Actions 页面点击对应的运行记录即可查看。

**Q: 推送失败怎么办？**
A: 查看 Actions 运行日志中的错误信息，常见问题是 SendKey 无效或网络超时。
