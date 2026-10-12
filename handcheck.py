"""Hand-check 50 random labelled reviews and print the result for manual verification."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import pandas as pd, json, random

random.seed(42)

rv = pd.read_csv("data/reviews.csv", encoding="utf-8").set_index("reviewId")
labels = pd.read_json("data/labels.jsonl", lines=True, encoding="utf-8").set_index("reviewId")

# Sample 50 random labelled reviews
sample_ids = random.sample(list(labels.index), 50)

rows = []
for rid in sample_ids:
    rev  = rv.loc[rid]
    lab  = labels.loc[rid]
    rows.append({
        "reviewId": rid,
        "score": rev["score"],
        "text": str(rev["content"])[:200],
        "stage": lab["stage"],
        "root_cause": lab["root_cause"],
        "owner": lab["owner"],
        "severity": lab["severity"],
        "safety_flag": lab["safety_flag"],
    })

df = pd.DataFrame(rows)
df.to_csv("data/handcheck_50.csv", index=False, encoding="utf-8")
print(f"Saved 50 samples to data/handcheck_50.csv")
print()
for i, r in df.iterrows():
    print(f"[{i+1:2d}] ⭐{r['score']} | stage={r['stage']:<25} | rc={r['root_cause']:<35} | sev={r['severity']} | owner={r['owner']}")
    print(f"       TEXT: {r['text'][:120]}")
    print()
