"""Write a quota-axi cache-format (schemaVersion 3) snapshot for QUOTA_AXI_SNAPSHOT.
argv: out devin_weekly devin_daily devin_credits_usd claude_5h claude_7d"""
import json, sys, datetime as dt
out, dw, dd, cr, c5, c7 = sys.argv[1], *map(float, sys.argv[2:])
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
def win(i, label, kind, secs, pct, reset_in):
    r = now + dt.timedelta(seconds=reset_in)
    return {"id": i, "label": label, "kind": kind, "percentRemaining": pct, "percentUsed": 100 - pct,
            "windowSeconds": secs, "startsAt": (r - dt.timedelta(seconds=secs)).isoformat().replace("+00:00", "Z"),
            "resetsAt": r.isoformat().replace("+00:00", "Z")}
iso = now.isoformat().replace("+00:00", "Z")
snap = {"schemaVersion": 3, "providers": [
  {"provider": "devin", "label": "Devin", "source": "api", "plan": "Pro",
   "windows": [win("weekly", "week", "weekly", 604800, dw, 3*86400), win("daily", "day", "session", 86400, dd, 10*3600)],
   "credits": {"remaining": cr, "unit": "usd"},
   "state": {"status": "fresh", "stale": False, "refreshedAt": iso, "sourcesTried": ["api"]}},
  {"provider": "claude", "label": "Claude", "source": "oauth",
   "windows": [win("five_hour", "session", "session", 18000, c5, 3*3600), win("seven_day", "week", "weekly", 604800, c7, 4*86400)],
   "state": {"status": "fresh", "stale": False, "refreshedAt": iso, "sourcesTried": ["oauth"]}},
]}
json.dump(snap, open(out, "w"), indent=1)
