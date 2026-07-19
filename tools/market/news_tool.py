from langchain_core.tools import tool
import feedparser
from urllib.parse import quote
from core.logger import logger
from core.constants import MAX_NEWS_ITEMS

@tool
def get_company_news(company_name: str) -> list:
    """
    Retrieve latest news headlines for a company using Google News RSS.

    Returns a list of structured dictionaries containing headline title, publication date, and source link.
    """
    try:
        query = quote(company_name)
        rss_url = f"https://news.google.com/rss/search?q={query}+stock+finance&hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(rss_url)

        if not feed.entries:
            # Fallback search query
            rss_url_fallback = f"https://news.google.com/rss/search?q={query}"
            feed = feedparser.parse(rss_url_fallback)

        news = []
        seen_titles = set()

        for entry in feed.entries:
            title = entry.title.strip()
            # Simple deduplication
            if title.lower() in seen_titles:
                continue
            seen_titles.add(title.lower())

            news.append({
                "title": title,
                "published": getattr(entry, "published", "Recently"),
                "link": getattr(entry, "link", ""),
            })

            if len(news) >= MAX_NEWS_ITEMS:
                break

        return news
    except Exception as e:
        logger.error(f"Error fetching news for {company_name}: {e}")
        return [{"title": f"Could not fetch news: {str(e)}", "published": "N/A", "link": ""}]