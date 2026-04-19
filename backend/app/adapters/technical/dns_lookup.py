import httpx
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel


class DNSAdapter(BaseAdapter):
    name = "dns"
    category = AdapterCategory.technical
    DOH_URL = "https://cloudflare-dns.com/dns-query"

    def _derive_domain(self, query: str) -> str:
        return f"{query.lower().replace(' ', '').replace(',', '')}.com"

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        domain = self._derive_domain(query)
        record_types = ["A", "MX", "TXT", "NS"]
        all_records: dict = {}

        async with httpx.AsyncClient(timeout=15) as client:
            for rtype in record_types:
                try:
                    r = await client.get(
                        self.DOH_URL,
                        params={"name": domain, "type": rtype},
                        headers={"Accept": "application/dns-json"},
                    )
                    data = r.json()
                    answers = data.get("Answer", [])
                    if answers:
                        all_records[rtype] = [a.get("data", "") for a in answers]
                except Exception:
                    pass

        if not all_records:
            return self._mock(query, domain)

        description_parts = [f"DNS records for {domain}:"]
        risk = RiskLevel.low

        if "A" in all_records:
            description_parts.append(f"A: {', '.join(all_records['A'][:3])}")
        if "MX" in all_records:
            description_parts.append(f"MX: {', '.join(all_records['MX'][:3])}")
        if "NS" in all_records:
            description_parts.append(f"NS: {', '.join(all_records['NS'][:2])}")
        if "TXT" in all_records:
            txt_joined = " | ".join(all_records["TXT"][:2])
            description_parts.append(f"TXT: {txt_joined[:200]}")
            if "spf" not in txt_joined.lower():
                risk = RiskLevel.medium 

        return [AdapterFinding(
            adapter=self.name,
            category=self.category,
            title=f"DNS records — {domain}",
            description=". ".join(description_parts),
            source_url=f"https://mxtoolbox.com/SuperTool.aspx?action=dns:{domain}",
            raw_data=all_records,
            confidence=0.95,
            risk_level=risk,
            is_mock=False,
        )]

    def _mock(self, query: str, domain: str) -> List[AdapterFinding]:
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"DNS records — {domain}",
                description=(
                    f"DNS records for {domain}. "
                    "A: 104.21.45.32, 172.67.183.12. "
                    "MX: mail.google.com (priority 10). "
                    "NS: ns1.cloudflare.com, ns2.cloudflare.com. "
                    "TXT: v=spf1 include:_spf.google.com ~all."
                ),
                source_url=f"https://mxtoolbox.com/SuperTool.aspx?action=dns:{domain}",
                raw_data={},
                confidence=0.6,
                risk_level=RiskLevel.low,
                is_mock=True,
            )
        ]
