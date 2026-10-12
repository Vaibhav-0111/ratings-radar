"""Step 2. Label every NEW review with journey stage, root cause, owner, severity.
Needs: export ANTHROPIC_API_KEY=...   (labels are cached in data/labels.jsonl; only new reviews are sent)
"""
import os, json, re, pandas as pd
from anthropic import Anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-5-5")
BATCH = 25
client = Anthropic()

SYSTEM = """You label Play Store reviews of MoveInSync, an employee commute app (cabs/shuttles to and from work).
Employees self-book rides by shift; the system assigns a vehicle and plans routes; they get a pickup time, track live,
board with OTP/driver checks, get dropped, and raise issues through ops -> company transport desk -> MoveInSync.
Reviews may be English, Hindi, or Hinglish. Judge what the reviewer actually complains about.

Return ONLY a JSON array, one object per input review, same order, with keys:
id: the input id
stage: one of [onboarding_login, roster_shift, booking, assignment_routing, pickup_time_eta, live_tracking,
  boarding_otp_safety, trip_driver_vehicle, drop, support_escalation, app_performance, notifications, ui_ux, praise_only, other]
root_cause: one of [app_crash_or_freeze, login_or_otp_sms_failure, booking_failed_or_unavailable, booking_window_or_policy,
  wrong_or_stale_eta_or_map, gps_tracking_inaccurate, late_or_no_show_vehicle, route_too_long_or_wrong, driver_behaviour,
  vehicle_condition, safety_concern, roster_or_shift_mismatch, support_unresponsive, notification_missing_or_late,
  confusing_ui, feature_request, slow_app, other, none]
owner: one of [app_engineering, ops_vendor, customer_config, unclear]
  (app_engineering = software defect; ops_vendor = driver/vehicle/dispatch behaviour; customer_config = company roster,
   cutoffs, policy; unclear = cannot tell)
severity: 1-4  (4 = employee could not travel or safety risk; 3 = trip badly disrupted; 2 = annoyance; 1 = minor/praise)
safety_flag: true if night-shift, women's safety, harassment, rash driving, SOS issues
company_mentioned: company/office name if stated else null
summary: max 12 words in English
Rating (score) is context only; do not assume a 1-star review is about the app."""

def parse(txt):
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    return json.loads(txt)

def main():
    rv = pd.read_csv("data/reviews.csv")
    rv = rv[rv["content"].notna() & (rv["content"].str.strip() != "")]
    done = set()
    if os.path.exists("data/labels.jsonl"):
        done = set(pd.read_json("data/labels.jsonl", lines=True)["reviewId"])
    todo = rv[~rv["reviewId"].isin(done)]
    print(f"{len(todo)} reviews to label")
    with open("data/labels.jsonl", "a") as f:
        for i in range(0, len(todo), BATCH):
            chunk = todo.iloc[i:i + BATCH]
            payload = [{"id": j, "score": int(r.score), "text": str(r.content)[:600]}
                       for j, r in enumerate(chunk.itertuples())]
            for attempt in range(3):
                try:
                    msg = client.messages.create(model=MODEL, max_tokens=4000, system=SYSTEM,
                                                 messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}])
                    out = parse(msg.content[0].text)
                    assert len(out) == len(chunk)
                    break
                except Exception as e:
                    print("retry", attempt, e); out = None
            if not out: continue
            for o, rid in zip(out, chunk["reviewId"]):
                o["reviewId"] = rid; o.pop("id", None)
                f.write(json.dumps(o, ensure_ascii=False) + "\n")
            f.flush(); print(f"labelled {min(i + BATCH, len(todo))}/{len(todo)}", end="\r")

if __name__ == "__main__":
    main()
