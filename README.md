# DarkWeb Intel

**Tor spiders + Claude triage + threat-scoring, wrapped in a FastAPI.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-3.5_Sonnet-D97757?logo=anthropic&logoColor=white)
![Playwright](https://img.shields.io/badge/JS_render-Playwright-45ba4b)
![License](https://img.shields.io/badge/License-MIT-yellow)

A dark-web intelligence platform. A Scrapy + Playwright spider targets Ahmia and Tor search engines, a regex-weighted engine scores findings, Claude triages each finding, and a FastAPI backend exposes it all — with a SAST scanner service and lead-generation endpoints on top.

> **Status:** work in progress. The spider and scorer are implemented, but the `POST /scan` endpoint currently runs a *simulated* scan (it scores placeholder content per keyword; the Scrapy hand-off is a stub).

---

## Why this exists

Threat intel from the dark web is usually locked behind five-figure enterprise subscriptions or scraped by hand into a spreadsheet. This is the middle path — a self-hosted crawler + scorer + AI triager you can point at your own keyword list, run through your own Tor circuit, and use to generate leads or alert on credential leaks without paying a vendor.

---

## Try it in 60 seconds

```bash
git clone https://github.com/Danush-Aries/darkweb-intel
cd darkweb-intel
cp backend/.env.example backend/.env   # add your ANTHROPIC_API_KEY
docker compose -f docker/docker-compose.yml up --build   # API + Tor proxy

# Or without Docker (needs a Tor SOCKS proxy on :9050)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then register a keyword and trigger a scan:

```bash
curl -X POST 'http://localhost:8000/keywords?keyword=yourcompany.com'
curl -X POST http://localhost:8000/scan
curl http://localhost:8000/reports
```

Interactive API docs are at `http://localhost:8000/docs`.

---

## How it works

```
keyword list
     |
     v
+-- Scrapy + Playwright spiders --+
|  Ahmia + .onion search          |
|  Tor SOCKS5 (127.0.0.1:9050)    |
+--------------|------------------+
               v
+-- Threat scorer ----------------+
|  regex-weighted 0-100 score     |
|  boosts: zero-day, cred-leak    |
+--------------|------------------+
               v
+-- Claude 3.5 Sonnet triage -----+
|  structured JSON:               |
|  criticality / threat_type /    |
|  summary / action / confidence  |
+--------------|------------------+
               v
+-- FastAPI + Tortoise ORM -------+
|  /keywords /scan /reports       |
|  /leads  /api/v1/monetization   |
+---------------------------------+
```

Also bundled: a SAST scanner service (`backend/app/services/scanner_service.py`), a lead-generation pipeline (`/leads`), and Stripe/PayPal/Razorpay monetization endpoints. The repo additionally contains a Next.js dashboard (`frontend/`) and a few experimental side projects (`revenueforge-ai/`, `llm-fragility-lab/`, `corruption-platform/`).

---

## Stack

| Layer | Tech |
|---|---|
| API | FastAPI + Tortoise ORM (SQLite/Postgres) |
| Crawler | Scrapy + Playwright over Tor SOCKS5 |
| Frontend | Next.js (`frontend/`) |
| Triage | AsyncAnthropic (Claude 3.5 Sonnet) |
| Async | asyncio + aiohttp |
| Payments | Stripe / PayPal / Razorpay |
| SAST | pure-Python static analyzer |

---

## More from Danush

Part of a broader stack of AI + security tooling:

- [jarvis](https://github.com/Danush-Aries/jarvis) — portable multi-provider AI assistant (voice/web/CLI)
- [breachintel](https://github.com/Danush-Aries/breachintel) — OSINT breach intelligence aggregator
- [cve-advisor](https://github.com/Danush-Aries/cve-advisor) — AI-powered CVE triage and patch recommendation
- [llm-fragility-lab](https://github.com/Danush-Aries/llm-fragility-lab) — adversarial testing lab for LLM robustness
- [network-intrusion-analyzer](https://github.com/Danush-Aries/network-intrusion-analyzer) — Suricata + Claude AI intrusion triage
- [autonomous-coding-agent](https://github.com/Danush-Aries/autonomous-coding-agent) — two-agent autonomous coding system

Built by [Dhanush](https://github.com/Danush-Aries) — AI engineering + cybersecurity.

## License

MIT — see [LICENSE](LICENSE).
