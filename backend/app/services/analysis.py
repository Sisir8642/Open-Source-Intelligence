"""
Entity Resolution & Risk Scoring Engine

Responsibilities:
1. Entity Resolution  — link findings to the correct entity, filter likely false positives
2. Confidence Scoring — normalise per-adapter scores into a combined entity confidence
3. Risk Scoring       — aggregate finding-level risks into a single entity risk score + level
"""
from typing import List, Tuple
from app.adapters.base import AdapterFinding, RiskLevel

ADAPTER_WEIGHT: dict[str, float] = {
    "hibp":            1.0,  
    "whois":           0.95,
    "dns":             0.95,
    "opencorporates":  0.92,
    "github":          0.88,
    "newsapi":         0.85,
    "google_search":   0.80,
    "linkedin":        0.60,   # Mock
    "twitter":         0.55,  
}

RISK_SCORE: dict[RiskLevel, float] = {
    RiskLevel.high:    1.0,
    RiskLevel.medium:  0.5,
    RiskLevel.low:     0.1,
    RiskLevel.unknown: 0.0,
}

HIGH_RISK_KEYWORDS = [
    "breach", "hack", "fraud", "lawsuit", "fine", "penalty",
    "scam", "bankrupt", "dissolved", "sanction", "leak",
]
MEDIUM_RISK_KEYWORDS = [
    "missing spf", "inactive", "no dns", "privacy protected",
    "expired", "unverified",
]


def resolve_entities(findings: List[AdapterFinding], query: str) -> List[AdapterFinding]:
    """
    Filter out findings that are unlikely to relate to the queried entity.
    Strategy: require at least one token from the query to appear in the title or description.
    """
    query_tokens = set(query.lower().split())
    if len(query_tokens) <= 1:
        return findings

    resolved = []
    for finding in findings:
        text = f"{finding.title} {finding.description or ''}".lower()
        if any(tok in text for tok in query_tokens if len(tok) > 3):
            resolved.append(finding)
        else:
            finding.confidence *= 0.4
            resolved.append(finding)
    return resolved


def elevate_risk_from_content(finding: AdapterFinding) -> AdapterFinding:
    """
    Inspect finding title + description for risk-indicative keywords
    and elevate risk_level if found.
    """
    text = f"{finding.title} {finding.description or ''}".lower()

    if any(kw in text for kw in HIGH_RISK_KEYWORDS):
        finding.risk_level = RiskLevel.high
    elif finding.risk_level == RiskLevel.unknown and any(kw in text for kw in MEDIUM_RISK_KEYWORDS):
        finding.risk_level = RiskLevel.medium

    return finding


def compute_risk_score(findings: List[AdapterFinding]) -> Tuple[float, RiskLevel]:
  
    if not findings:
        return 0.0, RiskLevel.unknown

    weighted_sum = 0.0
    weight_total = 0.0

    for f in findings:
        w = ADAPTER_WEIGHT.get(f.adapter, 0.7)
        score = RISK_SCORE[f.risk_level]
        weighted_sum += score * w * f.confidence
        weight_total += w * f.confidence

    if weight_total == 0:
        return 0.0, RiskLevel.unknown

    aggregate = weighted_sum / weight_total

    if aggregate >= 0.6:
        level = RiskLevel.high
    elif aggregate >= 0.25:
        level = RiskLevel.medium
    else:
        level = RiskLevel.low

    return round(aggregate, 3), level


def compute_confidence_score(findings: List[AdapterFinding]) -> float:

    if not findings:
        return 0.0
    total = sum(f.confidence * ADAPTER_WEIGHT.get(f.adapter, 0.7) for f in findings)
    weight = sum(ADAPTER_WEIGHT.get(f.adapter, 0.7) for f in findings)
    return round(total / weight, 3) if weight else 0.0


def generate_summary(query: str, findings: List[AdapterFinding], risk_level: RiskLevel) -> str:

    category_counts: dict[str, int] = {}
    for f in findings:
        category_counts[f.category] = category_counts.get(f.category, 0) + 1

    sources_str = ", ".join(
        f"{count} {cat}" for cat, count in category_counts.items()
    )

    risk_phrases = {
        RiskLevel.high:    " Significant risk indicators detected.",
        RiskLevel.medium:  " Moderate risk indicators present.",
        RiskLevel.low:     "Low risk profile. No major concerns identified.",
        RiskLevel.unknown: "Insufficient data to determine risk.",
    }

    return (
        f"Intelligence report for '{query}'. "
        f"Found {len(findings)} data points across {sources_str} sources. "
        f"{risk_phrases[risk_level]}"
    )


def analyse(query: str, findings: List[AdapterFinding]) -> dict:

    findings = resolve_entities(findings, query)
    findings = [elevate_risk_from_content(f) for f in findings]
    risk_score, risk_level = compute_risk_score(findings)
    confidence_score = compute_confidence_score(findings)
    summary = generate_summary(query, findings, risk_level)

    return {
        "findings": findings,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "confidence_score": confidence_score,
        "summary": summary,
    }
