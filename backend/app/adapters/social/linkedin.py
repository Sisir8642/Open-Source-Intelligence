import asyncio
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
#mock data
MOCK_COMPANY_PROFILES = {
    "default": {
        "followers": "12,400",
        "employees": "51–200",
        "industry": "Technology & Software",
        "hq": "San Francisco, CA",
        "founded": "2018",
        "specialties": ["AI/ML", "SaaS", "Cloud Infrastructure"],
    }
}

MOCK_INDIVIDUAL_PROFILES = {
    "default": {
        "headline": "Senior Software Engineer | Open Source Contributor",
        "connections": "500+",
        "location": "New York, NY",
        "skills": ["Python", "TypeScript", "Kubernetes", "System Design"],
    }
}


class LinkedInAdapter(BaseAdapter):
    """Mock LinkedIn adapter — returns synthetic profile data."""
    name = "linkedin"
    category = AdapterCategory.social

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        await asyncio.sleep(0.1) 

        if entity_type == "company":
            p = MOCK_COMPANY_PROFILES["default"]
            return [
                AdapterFinding(
                    adapter=self.name,
                    category=self.category,
                    title=f"LinkedIn Company Page — {query}",
                    description=(
                        f"{query} on LinkedIn. Industry: {p['industry']}. "
                        f"Employees: {p['employees']}. HQ: {p['hq']}. "
                        f"Founded: {p['founded']}. Followers: {p['followers']}. "
                        f"Specialties: {', '.join(p['specialties'])}."
                    ),
                    source_url=f"https://www.linkedin.com/company/{query.lower().replace(' ', '-')}",
                    raw_data=p,
                    confidence=0.6,
                    risk_level=RiskLevel.unknown,
                    is_mock=True,
                )
            ]
        else:
            p = MOCK_INDIVIDUAL_PROFILES["default"]
            return [
                AdapterFinding(
                    adapter=self.name,
                    category=self.category,
                    title=f"LinkedIn Profile — {query}",
                    description=(
                        f"{query} — {p['headline']}. "
                        f"Location: {p['location']}. "
                        f"Connections: {p['connections']}. "
                        f"Skills: {', '.join(p['skills'])}."
                    ),
                    source_url=f"https://www.linkedin.com/in/{query.lower().replace(' ', '-')}",
                    raw_data=p,
                    confidence=0.55,
                    risk_level=RiskLevel.unknown,
                    is_mock=True,
                )
            ]
