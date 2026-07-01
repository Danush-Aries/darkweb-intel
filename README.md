# DarkWeb Intel

**Tor spiders + Claude triage + threat-scoring, wrapped in a FastAPI.**

<!-- hero: 1600x600 screenshot of the DarkWeb Intel API response with scored findings -->

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-3.5_Sonnet-D97757?logo=anthropic&logoColor=white)
![Playwright](https://img.shields.io/badge/JS_render-Playwright-45ba4b)
![License](https://img.shields.io/badge/License-MIT-yellow)

A dark-web intelligence platform. Crawls Tor hidden services and Ahmia, scores findings with a weighted threat engine, triages each finding through Claude, and exposes everything through a clean REST API — with a built-in SAST scanner and lead-generation pipeline on top.

---

## Why this exists

Threat intel from the dark web is usually locked behind five-figure enterprise subscriptions or scraped by hand into a spreadsheet. This is the middle path — a self-hosted crawler + scorer + AI triager you can point at your own keyword list, run through your own Tor circuit, and use to generate leads or alert on credential leaks without paying a vendor.

---

## Try it in 60 seconds

```bash
git clone https://github.com/Danush-Aries/darkweb-intel
cd darkweb-intel
docker compose up --build

# Or without Docker
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

You need a Tor SOCKS proxy running on `:9050`. Then:

```bash
curl -X POST http://localhost:8000/scan -d '{"keywords":["yourcompany.com","ceo email"]}'
```

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
|  /scan  /findings  /leads       |
|  /sast  /payments               |
+---------------------------------+
```

Also bundled: SAST scanner (SQLi/hardcoded secrets/unsafe deserialization), a lead-generation pipeline, and Stripe/PayPal/Razorpay integrations for monetized deployments.

---

## Screenshots

<!-- screenshot: api-response.png -->
<!-- screenshot: threat-score-heatmap.png -->
<!-- screenshot: sast-report.png -->

---

## Stack

| Layer | Tech |
|---|---|
| API | FastAPI + Tortoise ORM (SQLite/Postgres) |
| Crawler | Scrapy + Playwright over Tor SOCKS5 |
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

MIT.
