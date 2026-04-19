import httpx
from typing import List
from datetime import datetime, timedelta
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
from app.core.config import settings


class NewsAPIAdapter(BaseAdapter):
    name = "newsapi"
    category = AdapterCategory.regulatory

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        if not settings.NEWS_API_KEY:
            return self._mock(query)

        from_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        params = {
            "q": f'"{query}"',
            "from": from_date,
            "sortBy": "relevancy",
            "pageSize": 5,
            "apiKey": settings.NEWS_API_KEY,
            "language": "en",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://newsapi.org/v2/everything", params=params)
            r.raise_for_status()
            data = r.json()

        findings = []
        for article in data.get("articles", [])[:5]:
            title = article.get("title", "")
            negative_terms = ["fraud", "breach", "hack", "lawsuit", "fine", "scam", "bankrupt"]
            risk = RiskLevel.high if any(t in title.lower() for t in negative_terms) else RiskLevel.low

            findings.append(AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"News: {title[:120]}",
                description=article.get("description", ""),
                source_url=article.get("url", ""),
                raw_data={
                    "source": article.get("source", {}).get("name"),
                    "published_at": article.get("publishedAt"),
                },
                confidence=0.85,
                risk_level=risk,
                is_mock=False,
            ))
        return findings if findings else self._mock(query)

    def _mock(self, query: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"News: {query} Announces Series B Funding Round",
                description=f"{query} has secured $12M in Series B funding to expand its AI-powered platform globally.",
                source_url="https://techcrunch.com",
                raw_data={"source": "TechCrunch", "published_at": "2024-10-05"},
                confidence=0.6,
                risk_level=RiskLevel.low,
                is_mock=True,
            ),
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"News: {query} Expands to European Markets",
                description=f"{query} is opening offices in London and Berlin as part of its international expansion strategy.",
                source_url="https://businesswire.com",
                raw_data={"source": "Business Wire", "published_at": "2024-09-20"},
                confidence=0.6,
                risk_level=RiskLevel.low,
                is_mock=True,
            ),
        ]
