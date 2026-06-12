# DarkWeb Intel

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![Anthropic](https://img.shields.io/badge/Claude-3.5_Sonnet-orange?logo=anthropic)
![License](https://img.shields.io/badge/License-MIT-yellow)

A FastAPI-based dark web intelligence platform that crawls Tor hidden services, scores findings with a weighted threat-scoring engine, triages results through the Claude (Anthropic) API, and exposes a lead-generation pipeline and payment-system alongside core intel endpoints.

---

## What It Does

DarkWeb Intel collects and enriches threat data from the dark web and presents it through a clean REST API:

1. **Dark web scanning** — Scrapy + Playwright spiders search Ahmia and .onion search engines for keywords you define. Requests are routed through a Tor SOCKS5 proxy.
2. **Threat scoring** — A regex-based scorer assigns a 0–100 risk score to each piece of scraped content, weighting critical indicators (zero-days, credential leaks) above general noise.
3. **AI triage** — Each scored result is sent to Claude 3.5 Sonnet for a structured report: `criticality`, `threat_type`, `summary`, `action_item`, `confidence`.
4. **SAST scanner** — A built-in static-analysis scanner checks code snippets for SQL injection, hard-coded secrets, unsafe deserialization, weak crypto, and more — no external tools required.
5. **Lead generation** — A multi-source lead pipeline (LinkedIn keyword search, email extraction from URLs, niche prospecting) with automatic scoring and deduplication.
6. **Monetization / payments** — Product, order, subscription, affiliate, and referral management backed by Stripe, PayPal, and Razorpay.

---

## Features

- REST API built with **FastAPI** and **Tortoise ORM** (SQLite by default, swap to Postgres for production)
- Async throughout — `asyncio`, `aiohttp`, `AsyncAnthropic`
- Scrapy + Playwright spider for JavaScript-rendered .onion pages
- Tor health-check utility (`tor_health_check.py`)
- Weighted regex threat scorer with density normalisation
- Claude AI triage with graceful fallback when API key is absent
- Portable SAST scanner — 15 built-in rules across 7 languages, no external binary needed
- Lead scoring formula (seniority + company size + email quality + LinkedIn presence)
- Full payment-gateway integration (Stripe, PayPal, Razorpay) with webhook endpoints
- Affiliate / referral commission tracking
- Docker Compose setup with Tor sidecar (`dperson/torproxy`)

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI 0.115 |
| ORM | Tortoise ORM 0.21 + aiosqlite |
| AI | Anthropic Claude 3.5 Sonnet (`anthropic` SDK 0.40) |
| Scraping | Scrapy 2.11 + scrapy-playwright |
| Anonymisation | Tor + SOCKS5 (`stem`, `requests[socks]`) |
| Payments | Stripe, PayPal REST SDK, Razorpay |
| Validation | Pydantic v2 + email-validator |
| Containerisation | Docker + Docker Compose |

---

## Installation

### Prerequisites

- Python 3.11+
- (Optional) Docker and Docker Compose for the Tor proxy sidecar

### 1. Clone and set up

```bash
git clone https://github.com/<your-org>/darkweb-intel.git
cd darkweb-intel/backend

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set ANTHROPIC_API_KEY and payment gateway keys
```

Minimum required variable for AI triage:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Start the API

```bash
# From the backend/ directory
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

### 4. (Optional) Start with Docker Compose including Tor proxy

```bash
# From docker/
docker compose up --build
```

---

## Usage Examples

### Check API is running

```bash
curl http://localhost:8000/
# {"message":"DarkWeb Intel API is running"}
```

### Add a keyword to monitor

```bash
curl -X POST "http://localhost:8000/keywords?keyword=ransomware"
```

### Trigger a dark web scan

```bash
curl -X POST http://localhost:8000/scan
# {"status":"Scan triggered"}
```

The scan runs in the background. Results appear under `/reports`.

### Retrieve intelligence reports

```bash
curl http://localhost:8000/reports
```

### Scan code for vulnerabilities (SAST)

```bash
curl -X POST http://localhost:8000/scanner/scan \
  -H "Content-Type: application/json" \
  -d '{
    "code": "password = \"hunter2\"\neval(user_input)",
    "filename": "app.py"
  }'
```

Example response:

```json
{
  "findings": [
    {
      "ruleId": "SAST-010",
      "message": "Hard-coded password or secret",
      "severity": "critical",
      "file": "app.py",
      "line": 1,
      "column": 1,
      "snippet": "password = \"hunter2\""
    },
    {
      "ruleId": "SAST-030",
      "message": "Use of eval() — remote code execution risk",
      "severity": "high",
      "file": "app.py",
      "line": 2,
      "column": 1,
      "snippet": "eval(user_input)"
    }
  ],
  "status": "success"
}
```

### Generate leads

```bash
curl -X POST http://localhost:8000/leads/generate \
  -H "Content-Type: application/json" \
  -d '{
    "linkedin_keywords": ["cybersecurity", "CISO"],
    "niche_markets": ["fintech"],
    "location": "San Francisco, CA",
    "limit_per_source": 20
  }'
```

### Create a product and order (Stripe)

```bash
# Create product
curl -X POST http://localhost:8000/api/v1/monetization/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DarkWeb Intel Pro",
    "description": "Monthly threat intelligence subscription",
    "product_type": 3,
    "price": 99.00,
    "billing_interval": "month"
  }'

# Create order
curl -X POST http://localhost:8000/api/v1/monetization/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "customer_email": "analyst@example.com",
    "payment_gateway": "stripe"
  }'
```

### Check Tor connectivity

```bash
python backend/tor_health_check.py
```

---

## Project Structure

```
darkweb-intel/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints.py          # Core intel + lead endpoints
│   │   │   └── scanner.py            # SAST scan endpoint
│   │   ├── core/
│   │   │   └── config.py             # Pydantic settings
│   │   ├── models/
│   │   │   ├── models.py             # Keyword, IntelReport
│   │   │   └── lead_models.py        # Lead, LeadInteraction
│   │   ├── monetization/
│   │   │   ├── api.py                # Payment / subscription endpoints
│   │   │   ├── models.py             # Product, Order, Subscription…
│   │   │   └── services.py           # Stripe / PayPal / Razorpay wrappers
│   │   ├── services/
│   │   │   ├── ai_triage.py          # Claude AI triage
│   │   │   ├── lead_generation_service.py
│   │   │   ├── scanner_service.py    # Built-in regex SAST engine
│   │   │   ├── threat_scorer.py      # Weighted regex threat scorer
│   │   │   └── telegram_bot.py       # Alert notifications
│   │   ├── spiders/
│   │   │   └── darkweb_spider.py     # Scrapy + Playwright .onion spider
│   │   └── main.py                   # FastAPI app + Tortoise registration
│   ├── scraper/
│   │   ├── middlewares.py            # Tor proxy middleware
│   │   └── settings.py               # Scrapy project settings
│   ├── tests/
│   ├── tor_health_check.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker/
│   └── docker-compose.yml
└── frontend/                         # Next.js dashboard (optional)
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes (for AI triage) | Anthropic API key |
| `DATABASE_URL` | No (default: SQLite) | Tortoise ORM database URL |
| `TOR_PROXY_URL` | No (default: `socks5://127.0.0.1:9050`) | Tor SOCKS5 proxy |
| `TELEGRAM_BOT_TOKEN` | No | Telegram alert bot token |
| `TELEGRAM_CHAT_ID` | No | Telegram destination chat ID |
| `STRIPE_SECRET_KEY` | For Stripe payments | Stripe secret key |
| `PAYPAL_CLIENT_ID` | For PayPal payments | PayPal client ID |
| `RAZORPAY_KEY_ID` | For Razorpay payments | Razorpay key ID |

See `backend/.env.example` for the full list.

---

## Security Notes

- This tool is intended for **authorised security research and threat intelligence** only.
- All .onion requests are routed through Tor — never over a clearnet connection.
- Do not store real credentials, PII, or payment keys in version control.
- The SAST scanner is a best-effort heuristic tool; supplement with dedicated tools (Semgrep, Bandit) for production security pipelines.
- No authentication is implemented on the API endpoints — add an API-key or OAuth middleware before exposing to the internet.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
