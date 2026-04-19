# OSINT Intelligence Platform

A full-stack Open-Source Intelligence (OSINT) web application that aggregates data from 9+ public sources for any company or individual, presents structured findings in a clean dashboard, and exports professional reports.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│  Next.js 14 Frontend  (Tailwind CSS + Context API)           │
│  Search → Results Dashboard → History → Export               │
└─────────────────────┬────────────────────────────────────────┘
                      │ HTTP (REST)
┌─────────────────────▼────────────────────────────────────────┐
│  FastAPI Backend                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Adapter Manager (asyncio.gather — runs in parallel)    │ │
│  │  ┌──────────┐  ┌───────────┐  ┌─────────────────────┐  │ │
│  │  │  Social  │  │ Technical │  │     Regulatory      │  │ │
│  │  │ Google   │  │ WHOIS     │  │  NewsAPI            │  │ │
│  │  │ LinkedIn │  │ GitHub    │  │  OpenCorporates     │  │ │
│  │  │ Twitter  │  │ DNS       │  │  Company Registry   │  │ │
│  │  │ HIBP     │  │           │  │                     │  │ │
│  │  └──────────┘  └───────────┘  └─────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│  Analysis Engine: Entity Resolution + Risk Scoring           │
│  Report Service: PDF (fpdf2) + Markdown                      │
└─────────────────────┬────────────────────────────────────────┘
                      │ SQLAlchemy async
┌─────────────────────▼────────────────────────────────────────┐
│  PostgreSQL  (searches · findings · reports)                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer     | Technology                                |
|-----------|-------------------------------------------|
| Frontend  | Next.js 14, Tailwind CSS, Context API     |
| Backend   | FastAPI, Python 3.12, asyncpg             |
| Database  | PostgreSQL 16, SQLAlchemy 2 (async)       |
| Reports   | fpdf2 (PDF), Markdown                     |
| Deploy    | Docker + docker-compose                   |

---

## Quick Start (Docker)

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd osint-app

# 2. Copy and configure environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys (see below)

# 3. Start everything
docker-compose up --build

# App:     http://localhost:3000
# API:     http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Manual Setup (Development)

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 16 running locally

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and API keys

# Run the server (tables auto-created on startup)
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## API Keys

The app works **without any API keys** — all adapters have mock fallbacks. Add real keys progressively to get live data:

| API | Purpose | Get Key | Free Tier |
|-----|---------|---------|-----------|
| `GOOGLE_API_KEY` + `GOOGLE_CSE_ID` | Web search results | [console.cloud.google.com](https://console.cloud.google.com) + [programmablesearchengine.google.com](https://programmablesearchengine.google.com) | 100 queries/day |
| `GITHUB_TOKEN` | GitHub org/user search | [github.com/settings/tokens](https://github.com/settings/tokens) | 60 req/hr unauth, 5000 with token |
| `NEWS_API_KEY` | Recent news mentions | [newsapi.org/register](https://newsapi.org/register) | 100 req/day |
| `HIBP_API_KEY` | Data breach lookup | [haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key) | Paid (~$4/mo) |
| `OPENCORPORATES_API_KEY` | Company registry data | [opencorporates.com/api_accounts](https://opencorporates.com/api_accounts) | Free tier available |

**No key needed**: WHOIS (whoisjson.com free tier), DNS (Cloudflare DNS-over-HTTPS)

**Mock data**: LinkedIn, Twitter/X (no public API)

---

## Adapter Architecture

Each data source is an independent adapter that inherits from `BaseAdapter`:

```python
class BaseAdapter(ABC):
    name: str
    category: AdapterCategory   # social | technical | regulatory

    @abstractmethod
    async def fetch(self, query: str, entity_type: str) -> List[AdapterFinding]:
        ...

    async def safe_fetch(self, ...):
        # Error isolation — one failure never blocks others
        ...
```

### Adding a new adapter

```python
# backend/app/adapters/social/my_new_source.py
from app.adapters.base import BaseAdapter, AdapterFinding, AdapterCategory

class MyNewAdapter(BaseAdapter):
    name = "my_source"
    category = AdapterCategory.social

    async def fetch(self, query, entity_type):
        # your implementation
        return [AdapterFinding(...)]
```

Then register it in `backend/app/adapters/orchestrator.py`:
```python
from app.adapters.social.my_new_source import MyNewAdapter
ALL_ADAPTERS = [..., MyNewAdapter()]
```

---

## Database Schema

```
searches
  id, query, entity_type, status, risk_level, risk_score,
  confidence_score, summary, created_at, completed_at

findings
  id, search_id (FK), adapter, category, title, description,
  source_url, raw_data (JSON), confidence, risk_level, is_mock, fetched_at

reports
  id, search_id (FK), format, file_path, content, created_at
```

---

## Risk Scoring

```
Risk Score = Σ (finding_risk × adapter_weight × confidence) / Σ (adapter_weight × confidence)

Risk Level:
  score ≥ 0.60  →  🔴 High
  score ≥ 0.25  →  🟡 Medium
  score < 0.25  →  🟢 Low
```

Adapter weights reflect source credibility: HIBP (1.0) > WHOIS (0.95) > OpenCorporates (0.92) > GitHub (0.88) > NewsAPI (0.85) > Google (0.80) > LinkedIn (0.60) > Twitter (0.55)

---

## API Reference

```
POST   /api/v1/searches/              Run a new OSINT search
GET    /api/v1/searches/              List search history
GET    /api/v1/searches/{id}          Get search with findings
POST   /api/v1/searches/{id}/report   Generate PDF or Markdown report
DELETE /api/v1/searches/{id}          Delete a search
GET    /api/v1/reports/{id}/download  Download a generated report
GET    /health                        Health check
```

Interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Project Structure

```
osint-app/
├── backend/
│   ├── app/
│   │   ├── adapters/
│   │   │   ├── base.py                  # Abstract adapter base class
│   │   │   ├── orchestrator.py          # Parallel adapter runner
│   │   │   ├── social/                  # google_search, linkedin, twitter, hibp
│   │   │   ├── technical/               # whois, github, dns_lookup
│   │   │   └── regulatory/              # newsapi, opencorporates
│   │   ├── api/v1/endpoints/            # FastAPI route handlers
│   │   ├── core/config.py               # Pydantic settings
│   │   ├── db/models/                   # SQLAlchemy models
│   │   ├── db/schemas/                  # Pydantic response schemas
│   │   └── services/                    # analysis, report, search_service
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/                         # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── ui/                      # Shared UI (RiskBadge, Spinner, etc.)
│   │   │   ├── search/                  # SearchForm
│   │   │   ├── results/                 # SearchHeader, FindingsPanel, FindingCard
│   │   │   ├── export/                  # ExportPanel
│   │   │   └── layout/                  # Navbar
│   │   ├── context/OSINTContext.tsx      # Global state (Context API + useReducer)
│   │   ├── lib/api.ts                   # Axios API client
│   │   └── types/index.ts               # TypeScript interfaces
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## Disclaimer

All data is sourced from public APIs and open databases. Mock/simulated data is clearly marked with a "simulated" badge in the UI and in reports. This tool is intended for legitimate open-source intelligence research only.
