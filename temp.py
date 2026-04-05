from datetime import datetime
import asyncio

import feedparser
from telegram import Bot
import nest_asyncio

nest_asyncio.apply()

# =========================
# 직접 입력
# =========================
RSS_URL = "http://www.boannews.com/media/news_rss.xml"

TELEGRAM_BOT_TOKEN = "6632520987:AAELlUGyyefA7VgUzkNbMKwMioSypXB4FeY"
TELEGRAM_CHAT_ID = 6419577835  # 본인 chat_id로 변경
# 최신 몇 개 기사까지 보낼지
MAX_ITEMS = 10


def get_rss_news():
    feed = feedparser.parse(RSS_URL)

    news_items = []
    for entry in feed.entries[:MAX_ITEMS]:
        title = entry.get("title", "제목 없음").strip()
        link = entry.get("link", "").strip()

        if not link:
            continue

        news_items.append({
            "title": title,
            "link": link
        })

    return news_items


def build_message(news_items):
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "🛡 보안뉴스",
        f"⏰ {today_str}",
        ""
    ]

    for idx, item in enumerate(news_items, start=1):
        lines.append(f"{idx}. {item['title']}")
        lines.append(item["link"])
        lines.append("")

    return "\n".join(lines).strip()


async def send_telegram_message(text: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text,
        disable_web_page_preview=True
    )


async def send_rss_news():
    rss_items = get_rss_news()

    if not rss_items:
        print("가져온 기사가 없습니다.")
        return

    message = build_message(rss_items)
    await send_telegram_message(message)
    print(f"전송 완료: {len(rss_items)}건")


if __name__ == "__main__":
    try:
        asyncio.run(send_rss_news())
    except KeyboardInterrupt:
        pass
