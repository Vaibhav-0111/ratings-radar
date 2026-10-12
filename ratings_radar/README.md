# Ratings Radar: MoveInSync Play Store ratings

Goal: explain why the rating is low, rank what to fix first, and answer "how are our ratings?" every week.

## Folder
- `scrape.py`           pull reviews + daily star-histogram snapshot (no key needed)
- `classify_offline.py` keyword/Hinglish labeller (no key needed)
- `classify.py`         optional LLM labeller (needs ANTHROPIC_API_KEY)
- `analyze.py`          Star Drag, owner split, version regressions, hourly spikes -> `report.md`
- `docs/`               the case study PDF
- `data/`               generated CSVs live here

## Run order
```
pip install -r requirements.txt
python scrape.py find
python scrape.py run <appId> [<appId2>]
python classify_offline.py
python analyze.py
```
Weekly: re-run the last four commands (scrape is incremental, labels are cached).

## Prompt to paste into Antigravity
> Read README.md and the PDF in docs/. Run the pipeline in README.md in order. After `classify_offline.py`,
> open data/labels.jsonl and data/reviews.csv, find rows where root_cause is "other", read the review text
> (English/Hindi/Hinglish), and relabel them using the same allowed values as in classify.py (stage, root_cause,
> owner, severity, safety_flag). Do NOT invent reviews. Then run analyze.py. Finally read report.md and the
> 100 lowest-rated reviews, and draft `recommendation.md` (max 2 pages): top 5 fixes ranked by Star Drag per
> engineering-week, each with owner, first concrete step, success metric, plus 5 real quotes and a short
> method note (tools, assumptions, limitations). Flag any claim not supported by the data.

## Honest limits
Star Drag is estimated from scraped reviews, not the official Play rating. Keyword labels are rough, so spot-check 50 rows and report the accuracy.
