"""Step 3. Turn labelled reviews into the weekly 'Ratings Radar' report (report.md) + CSVs.
Usage: python analyze.py [days_window=90] [lift_target=4]
Star Drag = how much the mean star rating of the window would rise if every 1-2 star review in that
group had instead been `lift_target` stars. It is a SAMPLE-based estimate, not the official Play rating.
"""
import sys, pandas as pd
WIN = int(sys.argv[1]) if len(sys.argv) > 1 else 90
TARGET = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0

rv = pd.read_csv("data/reviews.csv", parse_dates=["at"])
lb = pd.read_json("data/labels.jsonl", lines=True)
df = rv.merge(lb, on="reviewId")
df = df[df["at"] >= df["at"].max() - pd.Timedelta(days=WIN)].copy()
df["low"] = df["score"] <= 2
df["week"] = df["at"].dt.to_period("W").dt.start_time
df["hour"] = df["at"].dt.hour
base = df["score"].mean()

def drag(col):
    rows = []
    for k, g in df.groupby(col):
        lifted = df["score"].where(~((df[col] == k) & df["low"]), TARGET)
        rows.append({col: k, "low_reviews": int((g["low"]).sum()), "share_of_low_%": round(100 * g["low"].sum() / df["low"].sum(), 1),
                     "star_drag": round(lifted.mean() - base, 3), "avg_severity": round(g["severity"].mean(), 2)})
    return pd.DataFrame(rows).sort_values("star_drag", ascending=False)

out = {}
out["by_stage"] = drag("stage"); out["by_root_cause"] = drag("root_cause"); out["by_owner"] = drag("owner")

wk = df.groupby("week").agg(reviews=("score", "size"), avg=("score", "mean"), pct_1star=("score", lambda s: 100 * (s == 1).mean())).round(2)
ver = df.groupby("appVersion").agg(reviews=("score", "size"), avg=("score", "mean"), pct_low=("low", lambda s: 100 * s.mean())).round(2)
ver = ver[ver["reviews"] >= 30].sort_values("pct_low", ascending=False)
ver["regression_flag"] = ver["pct_low"] > 100 * df["low"].mean() + 10
hr = df[df["low"]].groupby("hour").size().rename("low_reviews")
hr_all = df.groupby("hour").size().rename("all_reviews")
hours = pd.concat([hr_all, hr], axis=1).fillna(0).astype(int)
safety = df[df["safety_flag"] == True][["at", "score", "content", "summary"]].sort_values("at", ascending=False).head(15)
comp = df["company_mentioned"].dropna().value_counts().head(10)
replied = df["replyContent"].notna().mean() * 100 if "replyContent" in df else float("nan")

for k, v in out.items(): v.to_csv(f"data/{k}.csv", index=False)
ver.to_csv("data/by_version.csv"); wk.to_csv("data/weekly.csv"); hours.to_csv("data/by_hour.csv")

with open("report.md", "w") as f:
    f.write(f"# Ratings Radar (last {WIN} days, {len(df)} labelled reviews)\n\n")
    f.write(f"Sample avg: **{base:.2f}** | 1-2 star share: **{100*df['low'].mean():.1f}%** | replied: {replied:.1f}%\n\n")
    f.write(f"_Star Drag assumes 1-2 star reviews in a group would become {TARGET:g} stars. Estimate, not fact._\n\n")
    for title, t in [("Who owns the 1-2 star pain", out["by_owner"]), ("Star Drag by journey stage", out["by_stage"]),
                     ("Star Drag by root cause", out["by_root_cause"]), ("Weekly trend", wk.tail(12)),
                     ("Versions (>=30 reviews), worst first", ver.head(10)), ("Reviews by hour", hours),
                     ("Top companies/offices mentioned", comp.to_frame())]:
        f.write(f"## {title}\n```\n{t.to_string()}\n```\n\n")
    f.write("## Safety-flagged reviews\n")
    for r in safety.itertuples(): f.write(f"- {r.at:%Y-%m-%d} ({r.score}*) {r.summary}\n")
print(open("report.md").read())
