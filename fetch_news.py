#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import feedparser
from datetime import datetime, timedelta
import time
import os

# Server酱配置 - 从环境变量获取
SEND_KEY = os.environ.get("SEND_KEY", "")

if not SEND_KEY:
    print("错误: 请设置SEND_KEY环境变量")
    exit(1)

# 科技资讯RSS源
RSS_SOURCES = [
    {"name": "36氪", "url": "https://www.36kr.com/feed/"},
    {"name": "虎嗅网", "url": "https://www.huxiu.com/rss.xml"},
    {"name": "爱范儿", "url": "https://www.ifanr.com/feed/"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
]

def get_rss_news(source, hours=24):
    """抓取RSS源过去24小时的新闻"""
    news_list = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(source["url"], headers=headers, timeout=10)
        response.encoding = 'utf-8'

        feed = feedparser.parse(response.text)
        cutoff_time = datetime.now() - timedelta(hours=hours)

        for entry in feed.entries[:15]:
            if hasattr(entry, 'published') and entry.published:
                try:
                    published = datetime(*entry.published_parsed[:6])
                    if published > cutoff_time:
                        news_list.append({
                            "title": entry.title,
                            "link": entry.link,
                            "source": source["name"],
                            "time": published.strftime("%H:%M")
                        })
                except:
                    pass
    except Exception as e:
        print(f"抓取 {source['name']} 失败: {e}")

    return news_list

def send_to_wechat(title, desp):
    """通过Server酱推送消息到微信"""
    url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"

    data = {
        "text": title,
        "desp": desp,
        "channel": 9
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            print("微信推送成功!")
            return True
        else:
            print(f"推送失败: {result}")
            return False
    except Exception as e:
        print(f"推送异常: {e}")
        return False

def main():
    print("开始抓取科技资讯...")
    all_news = []

    for source in RSS_SOURCES:
        news = get_rss_news(source)
        all_news.extend(news)
        time.sleep(1)

    all_news.sort(key=lambda x: x["time"], reverse=True)

    if not all_news:
        print("未获取到最新资讯")
        return

    title = f"科技资讯 {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    desp_lines = ["## 今日科技资讯\n"]
    current_source = None

    for news in all_news[:20]:
        if news["source"] != current_source:
            desp_lines.append(f"\n### {news['source']}\n")
            current_source = news["source"]
        desp_lines.append(f"- [{news['title']}]({news['link']}) {news['time']}\n")

    desp = "\n".join(desp_lines)

    print(f"共获取 {len(all_news)} 条资讯，推送中...")
    send_to_wechat(title, desp)

if __name__ == "__main__":
    main()
