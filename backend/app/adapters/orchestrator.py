import asyncio
from typing import List
from app.adapters.base import AdapterFinding

from app.adapters.social.google_search import GoogleSearchAdapter
from app.adapters.social.linkedin import LinkedInAdapter
from app.adapters.social.twitter import TwitterAdapter
from app.adapters.social.hibp import HaveIBeenPwnedAdapter

from app.adapters.technical.whois import WhoisAdapter
from app.adapters.technical.github import GitHubAdapter
from app.adapters.technical.dns_lookup import DNSAdapter

from app.adapters.regulatory.newsapi import NewsAPIAdapter
from app.adapters.regulatory.opencorporates import OpenCorporatesAdapter


ALL_ADAPTERS = [
    GoogleSearchAdapter(),
    LinkedInAdapter(),
    TwitterAdapter(),
    HaveIBeenPwnedAdapter(),
    WhoisAdapter(),
    GitHubAdapter(),
    DNSAdapter(),
    NewsAPIAdapter(),
    OpenCorporatesAdapter(),
]


async def run_all_adapters(query: str, entity_type: str) -> List[AdapterFinding]:
    """
    Runs all adapters concurrently using asyncio.gather.
    Each adapter's safe_fetch() ensures one failure doesn't block others.
    Returns a flat, deduplicated list of findings.
    """
    tasks = [adapter.safe_fetch(query, entity_type) for adapter in ALL_ADAPTERS]
    results = await asyncio.gather(*tasks)

    all_findings: List[AdapterFinding] = []
    for adapter_findings in results:
        all_findings.extend(adapter_findings)

    return all_findings
