import httpx
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
from app.core.config import settings


class OpenCorporatesAdapter(BaseAdapter):

    name = "opencorporates"
    category = AdapterCategory.regulatory

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        if entity_type != "company":
            return self._individual_mock(query)

        params = {"q": query, "format": "json", "per_page": 3}
        if settings.OPENCORPORATES_API_KEY:
            params["api_token"] = settings.OPENCORPORATES_API_KEY

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(
                    "https://api.opencorporates.com/v0.4/companies/search",
                    params=params,
                )
                r.raise_for_status()
                data = r.json()

            findings = []
            companies = data.get("results", {}).get("companies", [])
            for item in companies[:3]:
                co = item.get("company", {})
                inactive = co.get("current_status", "").lower() in ["dissolved", "inactive"]
                risk = RiskLevel.medium if inactive else RiskLevel.low

                findings.append(AdapterFinding(
                    adapter=self.name,
                    category=self.category,
                    title=f"Company Registry — {co.get('name', query)}",
                    description=(
                        f"Jurisdiction: {co.get('jurisdiction_code', 'N/A').upper()}. "
                        f"Company number: {co.get('company_number', 'N/A')}. "
                        f"Status: {co.get('current_status', 'N/A')}. "
                        f"Incorporated: {co.get('incorporation_date', 'N/A')}. "
                        f"Company type: {co.get('company_type', 'N/A')}."
                    ),
                    source_url=co.get("opencorporates_url", ""),
                    raw_data=co,
                    confidence=0.92,
                    risk_level=risk,
                    is_mock=False,
                ))
            return findings if findings else self._mock(query)
        except Exception:
            return self._mock(query)

    def _mock(self, query: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"Company Registry — {query} Inc.",
                description=(
                    f"Jurisdiction: US/DE (Delaware). "
                    "Company number: 7284910. "
                    "Status: Active. "
                    "Incorporated: 2018-07-22. "
                    "Company type: Corporation."
                ),
                source_url=f"https://opencorporates.com/companies?q={query.replace(' ', '+')}",
                raw_data={"status": "Active", "jurisdiction": "us_de"},
                confidence=0.65,
                risk_level=RiskLevel.low,
                is_mock=True,
            )
        ]

    def _individual_mock(self, query: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"Corporate affiliations — {query}",
                description=(
                    f"{query} is listed as a director or officer in 2 registered companies. "
                    "No dissolved or flagged entities found."
                ),
                source_url=f"https://opencorporates.com/officers?q={query.replace(' ', '+')}",
                raw_data={"directorships": 2},
                confidence=0.55,
                risk_level=RiskLevel.low,
                is_mock=True,
            )
        ]
