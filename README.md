# 📡 Ratings Radar — MoveInSync Play Store Analysis

> **Case Study**: Explain why the MoveInSync app rating is low, rank what to fix first, and answer "how are our ratings?" every week.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Data](https://img.shields.io/badge/Reviews-24%2C317-green)]()
[![Platform](https://img.shields.io/badge/Platform-Google%20Play%20Store-brightgreen?logo=google-play)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

---

## 🔍 What This Does

| Step | Script | What it does |
|---|---|---|
| 1️⃣ Scrape | `scrape.py` | Pulls up to 30k Play Store reviews (incremental, no API key) |
| 2️⃣ Classify | `classify_offline.py` | Labels every review: root cause, stage, owner, severity (English + Hinglish) |
| 3️⃣ Analyse | `analyze.py` | Computes **Star Drag** per category → generates `report.md` |
| 4️⃣ Recommend | `recommendation.md` | Top 5 fixes ranked by impact, with real quotes & success metrics |

---

## 📊 Key Findings (Last 90 Days — 24,317 Reviews)

| # | Root Cause | Star Drag | Low Reviews | Severity | Owner |
|---|---|---|---|---|---|
| 🥇 | App crash / freeze on update | **+0.094** | 24 | 2.97/4 | App Engineering |
| 🥈 | Late / no-show vehicle | **+0.064** | 16 | 2.89/4 | Ops/Vendor |
| 🥉 | Login / OTP failure | **+0.053** | 13 | **3.86/4** | App Engineering |
| 4 | Confusing UI (extra taps) | **+0.024** | 6 | 2.00/4 | App Engineering |
| 5 | Support unresponsive | **+0.017** | 4 | 3.00/4 | Unclear |

> ⚠️ **Women's Safety** flagged as Severity 4 — requires immediate escalation independent of Star Drag ranking.

---

## 🚀 How to Run

```bash
pip install -r requirements.txt

# Step 1: Scrape latest reviews
python scrape.py find                        # discover app IDs
python scrape.py run com.moveinsync.ets      # pull reviews (incremental)

# Step 2: Classify
python classify_offline.py                   # keyword labeller, no API key needed

# Step 3: Analyse
python analyze.py                            # generates report.md + CSVs
```

**Weekly refresh**: just re-run the last 3 commands. The scraper is incremental — it only fetches new reviews.

---

## 📁 File Structure

```
ratings-radar/
├── scrape.py              # Step 1: Pull Play Store reviews
├── classify_offline.py    # Step 2: Keyword/Hinglish labeller (no API key)
├── classify.py            # Step 2 (alt): LLM labeller (needs ANTHROPIC_API_KEY)
├── analyze.py             # Step 3: Star Drag analysis → report.md
├── handcheck.py           # Spot-check labelling accuracy on 50 random rows
├── check_apps.py          # Find MoveInSync app IDs on Play Store
├── requirements.txt       # Dependencies
├── recommendation.md      # 📋 Final recommendation report (TOP 5 FIXES)
├── report.md              # Auto-generated weekly analysis report
├── data/
│   ├── reviews.csv        # 24,317 scraped reviews
│   ├── labels.jsonl       # Classified labels for every review
│   ├── snapshots.csv      # Daily star-histogram snapshots
│   ├── by_root_cause.csv  # Star Drag by root cause
│   ├── by_stage.csv       # Star Drag by journey stage
│   ├── by_owner.csv       # Star Drag by owner team
│   ├── by_version.csv     # Per-version regression analysis
│   ├── weekly.csv         # Weekly rating trend
│   ├── by_hour.csv        # Reviews by hour of day
│   └── handcheck_50.csv   # Manual label accuracy check
└── docs/
    └── Case_Study_FDE_Moveinsync.pdf
```

---

## 🧠 How Star Drag Works

**Star Drag** = how much the sample rating would rise if every 1–2 star review in a category had instead been a 4-star review.

```
Star Drag = mean(scores, with low scores in group lifted to 4) - mean(all scores)
```

This ranks fixes by **business impact** rather than raw complaint count. A rare but severe issue (e.g., OTP failure blocking login) can outrank a common but minor one.

> ⚠️ Star Drag is estimated from the scraped review sample — not the official Play Store rating.

---

## 🏗️ Architecture

```
Play Store ──► scrape.py ──► reviews.csv
                                  │
                    classify_offline.py ──► labels.jsonl
                                  │
                           analyze.py ──► report.md + CSVs
                                  │
                      recommendation.md  (Top 5 fixes)
```

---

## ⚠️ Honest Limits

- Only **English-language** reviews scraped (`lang="en"`). Hindi/Hinglish reviews may be underrepresented.
- **55%** of reviews fall into `root_cause='other'` — too generic for keyword rules. Use `classify.py` (LLM) for a second pass.
- Star Drag is a **sample-based estimate**, not the official Play rating.
- Owner reply rate (0.6%) is based on scraped data — may lag real responses.

---

## 📦 Requirements

```
google-play-scraper
pandas
anthropic  # optional — only needed for classify.py (LLM mode)
```

---

*Built for the MoveInSync FDE Case Study — October 2026*
