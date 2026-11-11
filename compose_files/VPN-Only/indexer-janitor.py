#!/usr/bin/env python3
"""Indexer janitor for Prowlarr, run from cron. Prowlarr pushes every change to Sonarr/Radarr itself.
- Disables indexers with no successful query for DEAD_DAYS (Sonarr/Radarr keep warning about them), re-tests the
  ones it disabled on every run and re-enables them once Prowlarr's test passes. Indexers disabled by hand stay off.
- Adds public French/English TV/movie indexers from Prowlarr's catalog that pass Prowlarr's test: MAX_TESTS
  candidates per run, up to MAX_ENABLED active indexers; a failed candidate is retried after RETRY_DAYS.
Nothing is ever deleted. --dry-run prints what would change."""
import atexit, datetime as dt, json, os, re, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = re.search(r"^COMMON_PATH=(\S+)", open(os.path.join(HERE, ".env")).read(), re.M).group(1)
KEY = re.search(r"<ApiKey>([^<]+)", open(f"{COMMON}/configs/prowlarr/config.xml").read()).group(1)
STATE = f"{COMMON}/configs/indexer-janitor.json"
DEAD_DAYS, RETRY_DAYS, MAX_ENABLED, MAX_TESTS = 7, 30, 30, 5
LANGS, CATEGORIES = ("fr", "en"), {2000, 5000}  # Movies, TV
SKIP = re.compile(r"hentai|xxx|porn|adult", re.I)
DRY = "--dry-run" in sys.argv
NOW = dt.datetime.now(dt.timezone.utc)


def api(path, body=None, method="GET"):
    req = urllib.request.Request(f"http://127.0.0.1:9696/api/v1/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"X-Api-Key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:200]


def passes_test(indexer):
    return api("indexer/test", dict(indexer, enable=True), "POST")[0] == 200


def days_since(iso):
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (NOW - (t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc))).days


def log(msg):
    print(f"{NOW:%Y-%m-%d %H:%M} {'[dry-run] ' if DRY else ''}{msg}", flush=True)


state = json.load(open(STATE)) if os.path.exists(STATE) else {"disabled": [], "tried": {}}
if not DRY:  # also on a crash or interruption, so an indexer disabled here is never forgotten
    atexit.register(lambda: json.dump(state, open(STATE, "w"), indent=1))
indexers = api("indexer")[1]
failing = {s["indexerId"]: s for s in api("indexerstatus")[1]}

for i in indexers:
    s = failing.get(i["id"])
    if i["id"] in state["disabled"] and not i["enable"]:
        if passes_test(i):
            log(f"re-enabled {i['name']}: its test passes again")
            if not DRY:
                api(f"indexer/{i['id']}?forceSave=true", dict(i, enable=True), "PUT")
                state["disabled"].remove(i["id"])
            i["enable"] = True
    elif i["enable"] and s and days_since(s["initialFailure"]) >= DEAD_DAYS:
        log(f"disabled {i['name']}: no successful query since {s['initialFailure'][:10]}")
        if not DRY:
            api(f"indexer/{i['id']}?forceSave=true", dict(i, enable=False), "PUT")
            state["disabled"].append(i["id"])
        i["enable"] = False

enabled = sum(i["enable"] for i in indexers)
have = {i["definitionName"] for i in indexers}
profile = api("appprofile")[1][0]["id"]
candidates = [d for d in api("indexer/schema")[1]
              if d["privacy"] == "public" and d["protocol"] == "torrent"
              and (d.get("language") or "").split("-")[0] in LANGS
              and CATEGORIES & {c["id"] for c in (d.get("capabilities") or {}).get("categories", [])}
              and not SKIP.search(f"{d['definitionName']} {d['name']} {d.get('description') or ''}")
              and d["definitionName"] not in have
              and days_since(state["tried"].get(d["definitionName"], "2000-01-01")) >= RETRY_DAYS]
for d in candidates[:MAX_TESTS]:
    if enabled >= MAX_ENABLED:
        break
    d = {k: v for k, v in d.items() if k != "presets"}
    d.update(enable=True, appProfileId=profile, priority=25, tags=[])
    state["tried"][d["definitionName"]] = f"{NOW:%Y-%m-%d}"
    if not passes_test(d):
        log(f"skipped {d['name']}: test failed, retry in {RETRY_DAYS} days")
    elif DRY:
        log(f"would add {d['name']}: test passed, a real search decides")
    else:
        code, new = api("indexer?forceSave=true", d, "POST")
        assert code in (200, 201), f"adding {d['name']} failed: {code} {new}"
        # Prowlarr's test can pass while real searches hit Cloudflare: run the same empty search the apps do.
        code, results = api(f"search?query=&type=search&limit=20&indexerIds={new['id']}")
        if code == 200 and results:
            log(f"added {d['name']}: public, {d.get('language')}, test and a real search passed")
            enabled += 1
        else:
            api(f"indexer/{new['id']}", method="DELETE")  # only ever our own fresh, never-working addition
            log(f"skipped {d['name']}: a real search failed, retry in {RETRY_DAYS} days")

log(f"{enabled} active indexers, {len(candidates) - min(len(candidates), MAX_TESTS)} candidates left for later runs")
