import httpx
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
from app.core.config import settings


class GoogleSearchAdapter(BaseAdapter):
    name = "google_search"
    category = AdapterCategory.social

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        if not settings.GOOGLE_API_KEY or not settings.GOOGLE_CSE_ID:
            return self._mock(query)

        params = {
            "key": settings.GOOGLE_API_KEY,
            "cx": settings.GOOGLE_CSE_ID,
            "q": query,
            "num": 10,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://www.googleapis.com/customsearch/v1", params=params)
            r.raise_for_status()
            data = r.json()

        findings = []
        for item in data.get("items", []):
            findings.append(AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=item.get("title", ""),
                description=item.get("snippet", ""),
                source_url=item.get("link", ""),
                raw_data=item,
                confidence=0.85,
                risk_level=RiskLevel.unknown,
                is_mock=False,
            ))
        return findings

    def _mock(self, query: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"{query} — Official Website",
                description=f"The official online presence for {query}. Founded with a mission to deliver innovative solutions.",
                source_url=f"https://www.{query.lower().replace(' ', '')}.com",
                confidence=0.7,
                risk_level=RiskLevel.unknown,
                is_mock=True,
            ),
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"{query} | LinkedIn",
                description=f"View {query}'s professional profile on LinkedIn.",
                source_url=f"https://www.linkedin.com/company/{query.lower().replace(' ', '-')}",
                confidence=0.65,
                risk_level=RiskLevel.unknown,
                is_mock=True,
            ),
        ]
