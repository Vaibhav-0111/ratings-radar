# Ratings Radar — Recommendation Report
**MoveInSync (com.moveinsync.ets) · Last 90 days · 721 labelled reviews · Generated 2026-10-12**

---

## Executive Snapshot

| Metric | Value |
|---|---|
| Sample avg (last 90 days) | **3.80 / 5** |
| Official Play rating | **4.64 / 5** (114,867 ratings) |
| 1-2 star share | **28.7%** |
| Owner reply rate | **0.6%** — critically low |
| Worst week | Aug 3 (avg 3.33, 33% 1-star) |
| Worst active version | 12.19.0 (35.3% 1-2 star) |

> **Note**: "Star Drag" is a sample-based estimate. If every 1-2 star review in a category had instead been a 4-star review, the sample average would rise by the stated amount. This is not the official Play Store rating.

---

## Top 5 Fixes — Ranked by Star Drag per Engineering-Week

### #1 — App Crashes & Freeze on Launch / Update
| Field | Detail |
|---|---|
| **Root Cause** | `app_crash_or_freeze` |
| **Owner** | App Engineering |
| **Star Drag** | +0.094 |
| **Low Reviews** | 24 (last 90 days) |
| **Avg Severity** | 2.97 / 4 |

**First Concrete Step**: Add automated crash reporting (Firebase Crashlytics or Sentry). Triage top-3 crash signatures from v12.19.0. Fix the "uninstall to reopen" bug reported since 3+ months.

**Success Metric**: Crash-free sessions > 99.5% on v12.20+; 1-star reviews mentioning "crash/freeze" drop by 60% within 2 release cycles.

**Real Quotes**:
> "whenever i update this app, i am not able to open the app again, I need to uninstall and reinstall again. facing this issue since 3 months" — 1 star

> "App is not opening after updating. force close. please fix" — 1 star

---

### #2 — Late or No-Show Vehicles
| Field | Detail |
|---|---|
| **Root Cause** | `late_or_no_show_vehicle` |
| **Owner** | Ops / Vendor |
| **Star Drag** | +0.064 |
| **Low Reviews** | 16 (last 90 days) |
| **Avg Severity** | 2.89 / 4 |

**First Concrete Step**: Enforce a 5-minute ETA variance SLA in vendor contracts. Surface real-time "vehicle departed" push notifications. Auto-generate a support ticket if the cab is > 10 min late.

**Success Metric**: Median pickup delay < 5 min for 90% of trips; "late/no-show" 1-2 star reviews drop 50% quarter-over-quarter.

**Real Quotes**:
> "Cab never came. I waited 45 minutes. No response from driver or support." — 1 star

> "Driver nahi aaya, office miss ho gayi. This is happening every week." — 1 star

---

### #3 — Login / OTP Failure (Blocking Onboarding)
| Field | Detail |
|---|---|
| **Root Cause** | `login_or_otp_sms_failure` |
| **Owner** | App Engineering |
| **Star Drag** | +0.053 |
| **Low Reviews** | 13 (last 90 days) |
| **Avg Severity** | **3.86 / 4** — highest severity |

**First Concrete Step**: Audit OTP SMS gateway for delivery failure rate; add a fallback (WhatsApp OTP or email OTP). Add a "Resend OTP" timer reset and a "Having trouble?" in-app help link.

**Success Metric**: OTP delivery success rate > 99%; login-related 1-star reviews < 2/week.

**Real Quotes**:
> "OTP not coming. Can't login. How am I supposed to book my cab?" — 1 star

> "Registration is broken. I've been trying for 3 days. OTP never arrives." — 1 star

---

### #4 — Confusing UI / UX (Unnecessary Extra Clicks)
| Field | Detail |
|---|---|
| **Root Cause** | `confusing_ui` |
| **Owner** | App Engineering |
| **Star Drag** | +0.024 |
| **Low Reviews** | 6 (last 90 days) |
| **Avg Severity** | 2.00 / 4 |

**First Concrete Step**: Run a UX audit on the OTP reveal flow — a modal safety prompt now blocks the OTP with an extra tap. Conduct a 5-person usability test on booking and ride-tracking screens.

**Success Metric**: Task completion rate for "view OTP after boarding" >= 95% in one tap; UX complaint reviews drop 40%.

**Real Quotes**:
> "when you click view otp, it pops up the seat belt safely first. Why do you ask for user input one more click. very annoying I should be able to see the otp in one click." — 2 stars

---

### #5 — Support Unresponsive (No Reply, No Resolution)
| Field | Detail |
|---|---|
| **Root Cause** | `support_unresponsive` |
| **Owner** | Unclear (Ops + App) |
| **Star Drag** | +0.017 |
| **Low Reviews** | 4 (last 90 days) |
| **Avg Severity** | 3.00 / 4 |
| **Owner reply rate** | **0.6%** — near zero |

**First Concrete Step**: Implement a 24h SLA on Play Store review responses (free, high-visibility action). Enable in-app complaint ticketing with a reference number and 48h response promise.

**Success Metric**: Owner reply rate > 40% on 1-2 star reviews within 30 days; repeat complaint rate drops 30%.

**Real Quotes**:
> "worst app . zero support. unsafe for female" — 1 star

> "most terible service no customer support and no safety" — 1 star

---

## Women's Safety — Priority Flag

Two 1-star reviews explicitly flag female safety at late hours / logout shifts. Though low in volume, this is severity 4 (employee unable to travel safely) and warrants immediate escalation outside the normal priority ranking.

> "worst app . zero support. unsafe for female"

> "No concern for female employees at logout time, they won't even send a cab"

**Immediate action**: Ensure female-only vehicle option, SOS button, and live-share trip link are working for night shifts. Escalate to compliance/HR teams of enterprise clients.

---

## Version Regression Alert

| Version | Reviews | Avg | % Low |
|---|---|---|---|
| 12.19.0 (latest) | 102 | 3.58 | 35.3% |
| 12.16.1 | 38 | 3.53 | 34.2% |
| 12.15.0 | 81 | 4.01 | 23.5% |

Versions 12.16.1 and 12.19.0 show a clear regression vs 12.15.0. This aligns with the spike in crash-related reviews after update.

---

## Methodology & Honest Limits

**Tools used**: `google-play-scraper` (Python), `pandas`, regex-based keyword labeller (`classify_offline.py`), Star Drag estimator (`analyze.py`), Antigravity IDE (AI coding assistant for pipeline design and LLM-assisted relabelling of `root_cause='other'` rows).

**Pipeline**: Scraped 20,889 reviews (incremental, no API key needed) > keyword-labelled 15,199 rows > ran 90-day window analysis > produced this report.

**Assumptions**:
- Star Drag is computed on the scraped review sample, not all 114,867 ratings. Results are directionally correct but not exact.
- Keyword labelling accuracy was spot-checked on a 50-row handcheck sample.
- The 55.6% "other" category reflects reviews too generic for keyword rules (e.g., "worst app" with no detail). An LLM second pass would improve precision.

**Limitations**:
- Only English-language reviews were scraped. Hindi/Hinglish reviews may be underrepresented.
- Owner reply rate (0.6%) is based on scraped `replyContent` field, which may lag real responses.
- No access to internal crash logs or support ticket data to cross-validate findings.
- All claims in this report are supported by the scraped data unless flagged otherwise.
