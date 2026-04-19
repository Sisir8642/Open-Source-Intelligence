import asyncio
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel

class TwitterAdapter(BaseAdapter):
    name = "twitter"
    category = AdapterCategory.social

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        await asyncio.sleep(0.1)
        handle = query.lower().replace(" ", "")

        findings = [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"@{handle} on X (Twitter)",
                description=(
                    f"Official X account for {query}. "
                    f"Followers: ~8,200. Following: 420. Tweets: 1,340. "
                    f"Recent activity: product launches, community updates."
                ),
                source_url=f"https://x.com/{handle}",
                raw_data={
                    "handle": f"@{handle}",
                    "followers": 8200,
                    "tweets": 1340,
                    "verified": False,
                },
                confidence=0.55,
                risk_level=RiskLevel.unknown,
                is_mock=True,
            ),
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"Recent mentions of {query} on X",
                description=(
                    f"Recent public mentions of {query} include discussions about "
                    "their latest product release and customer support interactions. "
                    "Sentiment appears mostly positive (72% positive, 18% neutral, 10% negative)."
                ),
                source_url=f"https://x.com/search?q={query.replace(' ', '+')}",
                raw_data={
                    "total_mentions_7d": 312,
                    "sentiment": {"positive": 0.72, "neutral": 0.18, "negative": 0.10},
                },
                confidence=0.5,
                risk_level=RiskLevel.unknown,
                is_mock=True,
            ),
        ]
        return findings
