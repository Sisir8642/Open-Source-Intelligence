import httpx
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
from app.core.config import settings


class HaveIBeenPwnedAdapter(BaseAdapter):
    name = "hibp"
    category = AdapterCategory.social

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        domain = f"{query.lower().replace(' ', '')}.com"

        if not settings.HIBP_API_KEY:
            return self._mock(query, domain)

        headers = {
            "hibp-api-key": settings.HIBP_API_KEY,
            "user-agent": "OSINT-Intelligence-Platform",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"https://haveibeenpwned.com/api/v3/breaches?domain={domain}",
                headers=headers,
            )
            if r.status_code == 404:
                return [AdapterFinding(
                    adapter=self.name,
                    category=self.category,
                    title=f"No known breaches — {domain}",
                    description=f"HaveIBeenPwned found no publicly known data breaches for {domain}.",
                    source_url=f"https://haveibeenpwned.com/DomainSearch/{domain}",
                    confidence=0.95,
                    risk_level=RiskLevel.low,
                    is_mock=False,
                )]
            r.raise_for_status()
            breaches = r.json()

        findings = []
        for b in breaches:
            findings.append(AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"Data breach: {b.get('Name', 'Unknown')}",
                description=(
                    f"Breach date: {b.get('BreachDate', 'N/A')}. "
                    f"Compromised accounts: {b.get('PwnCount', 0):,}. "
                    f"Exposed data: {', '.join(b.get('DataClasses', []))}."
                ),
                source_url=f"https://haveibeenpwned.com/PwnedWebsites#{b.get('Name', '')}",
                raw_data=b,
                confidence=0.98,
                risk_level=RiskLevel.high,
                is_mock=False,
            ))
        return findings

    def _mock(self, query: str, domain: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"Data breach detected — {domain}",
                description=(
                    f"1 known breach found for {domain}. "
                    "Breach date: 2022-03-15. Compromised accounts: 45,000. "
                    "Exposed data: Email addresses, Passwords, Phone numbers."
                ),
                source_url=f"https://haveibeenpwned.com/DomainSearch/{domain}",
                raw_data={"breach_count": 1, "pwn_count": 45000},
                confidence=0.7,
                risk_level=RiskLevel.high,
                is_mock=True,
            )
        ]
