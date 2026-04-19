from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum


class AdapterCategory(str, Enum):
    social = "social"
    technical = "technical"
    regulatory = "regulatory"


class RiskLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    unknown = "unknown"


@dataclass
class AdapterFinding:
    """A single piece of intelligence returned by any adapter."""
    adapter: str
    category: AdapterCategory
    title: str
    description: Optional[str] = None
    source_url: Optional[str] = None
    raw_data: Optional[Any] = None
    confidence: float = 1.0          # 0.0 – 1.0
    risk_level: RiskLevel = RiskLevel.unknown
    is_mock: bool = False
    fetched_at: datetime = field(default_factory=datetime.utcnow)


class BaseAdapter(ABC):
    name: str = "base"
    category: AdapterCategory = AdapterCategory.social

    @abstractmethod
    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        """
        Fetch intelligence for the given query.

        Args:
            query: Company or individual name
            entity_type: 'company' | 'individual'

        Returns:
            List of AdapterFinding objects
        """
        ...

    async def safe_fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        try:
            return await self.fetch(query, entity_type)
        except Exception as exc:
            print(f"[{self.name}] adapter error: {exc}")
            return []
