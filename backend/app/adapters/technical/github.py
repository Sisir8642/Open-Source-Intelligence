import httpx
from typing import List
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory, RiskLevel
from app.core.config import settings


class GitHubAdapter(BaseAdapter):
    """
    Searches GitHub for organizations or users matching the query.
    Uses the public GitHub REST API v3. Personal access token increases rate limit.
    Docs: https://docs.github.com/en/rest/search
    """
    name = "github"
    category = AdapterCategory.technical

    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        search_type = "org" if entity_type == "company" else "user"
        params = {"q": f"{query} type:{search_type}", "per_page": 5}

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(
                    "https://api.github.com/search/users",
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()
                results = r.json()

            findings = []
            for item in results.get("items", [])[:3]:
                detail_r = await self._get_profile(item["login"], headers)
                findings.append(AdapterFinding(
                    adapter=self.name,
                    category=self.category,
                    title=f"GitHub {'Org' if entity_type == 'company' else 'User'} — {item['login']}",
                    description=self._format_description(detail_r),
                    source_url=item.get("html_url", ""),
                    raw_data=detail_r,
                    confidence=0.88,
                    risk_level=RiskLevel.low,
                    is_mock=False,
                ))
            return findings if findings else self._mock(query, entity_type)
        except Exception:
            return self._mock(query, entity_type)

    async def _get_profile(self, login: str, headers: dict) -> dict:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"https://api.github.com/users/{login}", headers=headers)
                return r.json() if r.status_code == 200 else {}
        except Exception:
            return {}

    def _format_description(self, profile: dict) -> str:
        if not profile:
            return "GitHub profile found."
        parts = []
        if profile.get("name"):
            parts.append(f"Name: {profile['name']}")
        if profile.get("bio"):
            parts.append(f"Bio: {profile['bio']}")
        if profile.get("public_repos") is not None:
            parts.append(f"Public repos: {profile['public_repos']}")
        if profile.get("followers") is not None:
            parts.append(f"Followers: {profile['followers']}")
        if profile.get("location"):
            parts.append(f"Location: {profile['location']}")
        return ". ".join(parts) if parts else "GitHub profile found."

    def _mock(self, query: str, entity_type: str) -> List[AdapterFinding]:
        handle = query.lower().replace(" ", "-")
        kind = "org" if entity_type == "company" else "user"
        return [
            AdapterFinding(
                adapter=self.name,
                category=self.category,
                title=f"GitHub {kind.title()} — {handle}",
                description=(
                    f"GitHub presence for {query}. "
                    "Public repos: 34. Followers: 1,280. "
                    "Primary languages: Python, TypeScript, Go. "
                    "Last active: recently."
                ),
                source_url=f"https://github.com/{handle}",
                raw_data={"login": handle, "public_repos": 34, "followers": 1280},
                confidence=0.6,
                risk_level=RiskLevel.low,
                is_mock=True,
            )
        ]
