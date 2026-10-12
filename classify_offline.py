"""Step 2 (NO API KEY NEEDED). Keyword-based labeller incl. common Hinglish words.
Writes the same data/labels.jsonl format as classify.py, so analyze.py works unchanged.
It is rough: rows it cannot place get root_cause='other' -> have Antigravity (or you) relabel those.
"""
import re, json, os, pandas as pd

# (root_cause, stage, owner, severity, regex)  -- FIRST match wins, so order = priority
# Negative-context guard: these words indicate a complaint context.
# Used to avoid firing keyword rules on praise reviews that mention e.g. "tracking" positively.
NEG_CONTEXT = re.compile(
    r"not |n't |nahi|nhi|\bbad\b|worst|poor|waste|disappoint|pathetic|useless|horrible|"
    r"problem|issue|error|fail|wrong|can.?t|cannot|unable|never|doesn.?t|don.?t|didn.?t|"
    r"please fix|please improve|need to|should (fix|change|improve)|awful|terrible"
)

RULES = [
 ("safety_concern", "boarding_otp_safety", "ops_vendor", 4, r"unsafe|harass|molest|drunk|\brash\b|reckless|\bsos\b|women safety|female safety|lady|girl.*(night|alone)|safety issue"),
 ("login_or_otp_sms_failure", "onboarding_login", "app_engineering", 4, r"log ?in|sign ?in|otp (not|nahi|never)|not getting otp|password|register|registration|verification fail|can.?t (log|sign)"),
 ("app_crash_or_freeze", "app_performance", "app_engineering", 3, r"crash|force close|keeps closing|not opening|won.?t open|open nahi|black screen|freez|\bhang\b|stuck on|not working|nahi chal|bug|\berror\b"),
 ("slow_app", "app_performance", "app_engineering", 2, r"\bslow\b|\blag\b|loading|takes too long"),
 ("booking_window_or_policy", "booking", "customer_config", 3, r"cut ?off|window closed|deadline|too late to book|booking closed|not allowed to book|booking limit"),
 ("booking_failed_or_unavailable", "booking", "app_engineering", 4, r"book(ing)? (fail|error|not|nahi|issue|problem)|can.?t book|cannot book|unable to book|no (cab|seat|vehicle)s? available|slot|booking nahi|cancel(led|s)? (my )?(booking|trip|ride)"),
 ("wrong_or_stale_eta_or_map", "pickup_time_eta", "app_engineering", 3, r"\beta\b|wrong (time|pickup)|pickup time.*(wrong|late)|time (wrong|change|incorrect)|map (wrong|not working)"),
 # GPS rule: only fire when negative context is present (checked in label() below)
 ("gps_tracking_inaccurate", "live_tracking", "app_engineering", 3, r"gps|live location|location (wrong|not|inaccurate|issue)|cab location (wrong|not)|where is (my )?cab|tracking (not|wrong|inaccurate|issue)"),
 ("late_or_no_show_vehicle", "pickup_time_eta", "ops_vendor", 3, r"\blate\b|delay|no ?show|not (come|came|arrive)|didn.?t (come|arrive)|nahi aa|nhi aa|der se|\bwait\b|intezar|never came"),
 # Driver rule: only fire on negative context (checked in label() below)
 ("driver_behaviour", "trip_driver_vehicle", "ops_vendor", 3, r"rude|misbehav|call(s)? (not )?(pick|receive)|phone nahi|bad attitude|driver (rude|misbehav|bad|did not|didn.?t|never)|chauffeur"),
 ("vehicle_condition", "trip_driver_vehicle", "ops_vendor", 2, r"dirty|smell|old (car|vehicle)|breakdown|broke down|uncomfortable"),
 # Route rule: exclude comparative sentences like "X was better than this"
 ("route_too_long_or_wrong", "assignment_routing", "ops_vendor", 2, r"wrong route|detour|zig ?zag|long way|taking too long|route (bad|wrong|issue|problem)"),
 # Support rule: exclude "no complaints"
 ("support_unresponsive", "support_escalation", "unclear", 3, r"support (not|bad|no|unresponsive)|customer care|helpline|help ?desk|no response|not responding|no reply|grievance|\bticket\b"),
 ("roster_or_shift_mismatch", "roster_shift", "customer_config", 3, r"roster|wrong shift|schedule (wrong|issue|problem)|timing not"),
 ("notification_missing_or_late", "notifications", "app_engineering", 2, r"notification (not|missing|late|fail)|alert (not|missing)|\bsms\b (not|fail)|no (notification|alert)"),
 # UI rule: exclude positive phrases like "user friendly", "nice ui"
 ("confusing_ui", "ui_ux", "app_engineering", 2, r"confusing|complicated|difficult to use|not user.?friendly|bad (ui|interface|design)|worst (ui|interface)"),
 ("feature_request", "other", "app_engineering", 1, r"please add|should (add|have)|need option|add (a )?feature|wish|suggest"),
]
SAFETY_FLAG = re.compile(r"night|midnight|unsafe|harass|molest|drunk|\brash\b|reckless|\bsos\b|women|female|lady|safety")
COMPANY = re.compile(r"\b(infosys|tcs|wipro|cognizant|accenture|capgemini|hcl|tech mahindra|ibm|amazon|google|microsoft|deloitte|genpact|ey|kpmg|hsbc|jpmorgan|goldman|dell|oracle|sap|adobe|cisco)\b")
POS = re.compile(r"good|great|nice|excellent|best|awesome|helpful|love|smooth|easy|perfect|thanks|useful")

def label(text, score):
    t = str(text).lower()
    has_neg = bool(NEG_CONTEXT.search(t))
    # High-star reviews with no negative context → praise before any keyword rule fires
    if score >= 4 and not has_neg:
        return "none", "praise_only", "unclear", 1
    for rc, stage, owner, sev, rx in RULES:
        if re.search(rx, t):
            return rc, stage, owner, sev
    if score >= 4 or POS.search(t):
        return "none", "praise_only", "unclear", 1
    return "other", "other", "unclear", 2

rv = pd.read_csv("data/reviews.csv")
rv = rv[rv["content"].notna() & (rv["content"].astype(str).str.strip() != "")]
done = set()
if os.path.exists("data/labels.jsonl"):
    done = set(pd.read_json("data/labels.jsonl", lines=True)["reviewId"])
todo = rv[~rv["reviewId"].isin(done)]
with open("data/labels.jsonl", "a", encoding="utf-8") as f:
    for r in todo.itertuples():
        rc, stage, owner, sev = label(r.content, r.score)
        # a 4-5 star review with a complaint keyword is usually mild; cap severity
        if r.score >= 4 and rc != "none": sev = min(sev, 2)
        t = str(r.content).lower(); m = COMPANY.search(t)
        f.write(json.dumps({"reviewId": r.reviewId, "stage": stage, "root_cause": rc, "owner": owner,
                            "severity": sev, "safety_flag": bool(SAFETY_FLAG.search(t)),
                            "company_mentioned": m.group(1) if m else None,
                            "summary": str(r.content)[:60]}, ensure_ascii=False) + "\n")
print(f"labelled {len(todo)} new reviews. Rows with root_cause='other' need a second pass.")
