"""Step 1. Pull Play Store reviews + a daily rating snapshot.
Usage:
  python scrape.py find                 # list candidate MoveInSync apps and their appIds
  python scrape.py run com.app.id ...   # scrape one or more apps (incremental: safe to re-run weekly)
"""
import sys, time, os, datetime as dt
import pandas as pd
from google_play_scraper import reviews, search, app, Sort

DATA = "data"; os.makedirs(DATA, exist_ok=True)
RV = f"{DATA}/reviews.csv"; SNAP = f"{DATA}/snapshots.csv"

def find():
    for q in ["MoveInSync", "MoveInSync employee", "MoveInSync driver", "MIS Moveinsync shuttle"]:
        for r in search(q, lang="en", country="in", n_hits=10):
            app_id   = str(r.get("appId") or "")
            title    = str(r.get("title") or "")[:35]
            dev      = str(r.get("developer") or "")[:25]
            score    = r.get("score") or "N/A"
            print(f'{app_id:55} | {title:35} | {dev:25} | {score}')

def scrape(app_id, max_reviews=30000):
    rows, token = [], None
    while len(rows) < max_reviews:
        batch, token = reviews(app_id, lang="en", country="in", sort=Sort.NEWEST,
                               count=200, continuation_token=token)
        rows += batch
        print(f"{app_id}: {len(rows)} reviews", end="\r")
        if not token or not batch: break
        time.sleep(1)
    df = pd.DataFrame(rows); df["app_id"] = app_id
    return df

def snapshot(app_id):
    a = app(app_id, lang="en", country="in")
    h = a["histogram"]  # [1star, 2star, 3star, 4star, 5star]
    return {"date": dt.date.today().isoformat(), "app_id": app_id, "title": a["title"],
            "score": a["score"], "ratings": a["ratings"], "reviews": a["reviews"],
            "s1": h[0], "s2": h[1], "s3": h[2], "s4": h[3], "s5": h[4]}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "find": find(); sys.exit()
    new = pd.concat([scrape(a) for a in sys.argv[2:]], ignore_index=True)
    if os.path.exists(RV):
        new = pd.concat([pd.read_csv(RV), new], ignore_index=True)
    new.drop_duplicates("reviewId").to_csv(RV, index=False)
    snaps = pd.DataFrame([snapshot(a) for a in sys.argv[2:]])
    if os.path.exists(SNAP): snaps = pd.concat([pd.read_csv(SNAP), snaps])
    snaps.drop_duplicates(["date", "app_id"], keep="last").to_csv(SNAP, index=False)
    print(f"\nSaved {len(new.drop_duplicates('reviewId'))} reviews total")
