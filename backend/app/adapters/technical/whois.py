import httpx
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
from app.core.config import settings


class WhoisAdapter(BaseAdapter):
    """
    Fetches WHOIS registration data for a domain derived from the query.
    Uses whoisjson.com free tier (no key) or paid key for higher limits.
    Docs: https://whoisjson.com
    """
    name = "whois"
    category = AdapterCategory.technical

    def _derive_domain(self, query: str) -> str:
        return f"{query.lower().replace(' ', '').replace(',', '').replace('.', '')}.com"

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        domain = self._derive_domain(query)

        try:
            headers = {}
            if settings.WHOIS_API_KEY:
                headers["Authorization"] = f"Token {settings.WHOIS_API_KEY}"

            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(
                    f"https://get.whoisjson.com/?domain={domain}",
                    headers=headers,
                )
                r.raise_for_status()
                data = r.json()

            whois = data.get("WhoisRecord", data)
            registrant = whois.get("registrant", {})
            dates = whois.get("registryData", whois)
            creation = dates.get("createdDate", whois.get("createdDate", "N/A"))
            expiry = dates.get("expiresDate", whois.get("expiresDate", "N/A"))
            registrar = whois.get("registrarName", whois.get("domainName", "N/A"))
            privacy = "yes" if "privacy" in str(registrant).lower() or registrant == {} else "no"

            return [AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"WHOIS — {domain}",
                description=(
                    f"Domain: {domain}. Registrar: {registrar}. "
                    f"Created: {creation}. Expires: {expiry}. "
                    f"Privacy protection: {privacy}."
                ),
                source_url=f"https://who.is/whois/{domain}",
                raw_data=data,
                confidence=0.9,
                risk_level=RiskLevel.low,
                is_mock=False,
            )]
        except Exception:
            return self._mock(query, domain)

    def _mock(self, query: str, domain: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"WHOIS — {domain}",
                description=(
                    f"Domain: {domain}. Registrar: GoDaddy LLC. "
                    "Created: 2019-04-12. Expires: 2026-04-12. "
                    "Privacy protection: yes (WhoisGuard enabled)."
                ),
                source_url=f"https://who.is/whois/{domain}",
                raw_data={"domain": domain, "registrar": "GoDaddy LLC"},
                confidence=0.6,
                risk_level=RiskLevel.low,
                is_mock=True,
            )
        ]
