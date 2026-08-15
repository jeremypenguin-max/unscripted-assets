#!/usr/bin/env python3
"""
Apply Jean-Christophe Chouinard's "AI Mode query" regex to Google Search Console
query exports, and score it against a shape-based alternative.

Usage
-----
  # single period
  python3 aimode_regex.py queries.csv

  # pre/post comparison (the control that makes the result mean anything)
  python3 aimode_regex.py --before pre-ai-mode.csv --after current.csv

  # dump every matched query to CSV for eyeballing
  python3 aimode_regex.py queries.csv --dump matched.csv

Accepts GSC's "Queries" CSV export (Top queries / Clicks / Impressions / CTR /
Position), the BigQuery bulk-export column names, or any CSV with a query column
and optional clicks/impressions columns.
"""

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict

# --------------------------------------------------------------------------
# The pattern under test, transcribed verbatim from the LinkedIn post.
# --------------------------------------------------------------------------
JC_REGEX = (
    r"^((please|write|draft|generate|summarize|rewrite|translate|explain|compare|"
    r"act as|you are a|(give|show|tell|plan) (a|me)|list|organize|pretend you are|"
    r"make it (shorter|funnier)|suggest|estimate|optimize|find|can you) .*"
    r"|give me .* more"
    r"|(hi|hello|hey|hiya)( (there))?"
    r"|good (morning|afternoon|evening)|how are you|yo"
    r"|(thanks|thank you)( (so much|a lot|very much))?|thx|cheers"
    r"|(awesome|great|cool) thanks|ty|thankyou|sorry"
    r"|fuck (you|off)|i hate you|you suck|shut up"
    r"|yes|yep|yeah|yea|sure|ok|okay|correct|fine|sounds good|perfect|great"
    r"|yes both|yes i do|yes that would be great|yes go on|yes,? pricing"
    r"|(yes|yeah|sure|ok|okay) (please|thanks|thank you|pls|thx|plz)"
    r"|(please|thanks|thank you) (yes|yeah|sure|ok|okay)"
    r"|(no|nope|nah)( (thanks|thank you|thx))?"
    r"|cancel|stop|wrong|incorrect|anywhere|all|any"
    r"|yes please recommend|please recommend"
    r"|bye|goodbye|bye bye|see ya|end|quit|done|help|options|what can you do"
    r"|start over|restart|more|next|continue|go on|show on map|show me"
    r"|any other options|others|please do|show map|try again|again"
    r"|shorter|longer|fix it|is that all"
    r"|(where|when|anything) else"
    r"|(are there|any|show|show me) (more|others)"
    r"|more (recommendations|ideas|options|results|places|hotels|restaurants|"
    r"things to do|attractions)"
    r"|(show|tell|add) (me )?(more|others|next))$"
)
JC = re.compile(JC_REGEX)

# --------------------------------------------------------------------------
# Branch attribution: which family of the alternation actually fired.
# Ordered — first hit wins. This is what separates "looks like a real LLM
# prompt" from "is a one-word filler token that also happens to be a brand".
# --------------------------------------------------------------------------
BRANCHES = [
    ("prompt_verb", re.compile(
        r"^((please|write|draft|generate|summarize|rewrite|translate|explain|compare|"
        r"act as|you are a|(give|show|tell|plan) (a|me)|list|organize|pretend you are|"
        r"make it (shorter|funnier)|suggest|estimate|optimize|find|can you) .*"
        r"|give me .* more)$")),
    ("greeting", re.compile(
        r"^((hi|hello|hey|hiya)( (there))?|good (morning|afternoon|evening)|"
        r"how are you|yo)$")),
    ("thanks", re.compile(
        r"^((thanks|thank you)( (so much|a lot|very much))?|thx|cheers|"
        r"(awesome|great|cool) thanks|ty|thankyou|sorry)$")),
    ("profanity", re.compile(r"^(fuck (you|off)|i hate you|you suck|shut up)$")),
    ("affirm", re.compile(
        r"^(yes|yep|yeah|yea|sure|ok|okay|correct|fine|sounds good|perfect|great|"
        r"yes both|yes i do|yes that would be great|yes go on|yes,? pricing|"
        r"(yes|yeah|sure|ok|okay) (please|thanks|thank you|pls|thx|plz)|"
        r"(please|thanks|thank you) (yes|yeah|sure|ok|okay))$")),
    ("negate", re.compile(r"^((no|nope|nah)( (thanks|thank you|thx))?|cancel|stop|"
                          r"wrong|incorrect)$")),
    ("chatbot_nav", re.compile(
        r"^(anywhere|all|any|yes please recommend|please recommend|bye|goodbye|"
        r"bye bye|see ya|end|quit|done|help|options|what can you do|start over|"
        r"restart|more|next|continue|go on|show on map|show me|any other options|"
        r"others|please do|show map|try again|again|shorter|longer|fix it|"
        r"is that all|(where|when|anything) else|"
        r"(are there|any|show|show me) (more|others)|"
        r"more (recommendations|ideas|options|results|places|hotels|restaurants|"
        r"things to do|attractions)|(show|tell|add) (me )?(more|others|next))$")),
]

# --------------------------------------------------------------------------
# Shape-based alternative: targets how AI Mode queries actually look
# (long, natural-language, constraint-laden) rather than chatbot turn-taking.
# --------------------------------------------------------------------------
QUESTION_OPENER = re.compile(
    r"^(what|what's|whats|how|why|which|who|when|where|should|can|could|is|are|"
    r"does|do|will|would)\b")
CONSTRAINT_MARKER = re.compile(
    r"\b(vs|versus|instead of|compared to|better than|for a|for my|for small|"
    r"without|under \$?\d|cheaper than|alternative to|that (can|will|does)|"
    r"if i|when i|do i need|worth it|pros and cons|difference between)\b")

def shape_score(q):
    """Returns (label, reason) — high / medium / None."""
    words = q.split()
    n = len(words)
    has_q = bool(QUESTION_OPENER.search(q))
    has_c = bool(CONSTRAINT_MARKER.search(q))
    if n >= 12:
        return "high", f"{n} words"
    if n >= 8 and (has_q or has_c):
        return "high", f"{n} words + {'question' if has_q else 'constraint'}"
    if n >= 8:
        return "medium", f"{n} words"
    if has_q and has_c:
        return "medium", "question + constraint"
    return None, ""


# --------------------------------------------------------------------------
# CSV loading
# --------------------------------------------------------------------------
QUERY_COLS = ("top queries", "query", "queries", "search query", "keyword", "term")
CLICK_COLS = ("clicks", "click", "url_clicks", "total clicks")
IMPR_COLS = ("impressions", "impression", "impressions_count", "total impressions")
POS_COLS = ("position", "avg position", "average position", "sum_top_position")


def _pick(header, candidates):
    lowered = {h.strip().lower(): h for h in header}
    for c in candidates:
        if c in lowered:
            return lowered[c]
    return None


def _num(v):
    if v is None:
        return 0
    v = str(v).strip().replace(",", "").replace("%", "")
    if not v:
        return 0
    try:
        return float(v)
    except ValueError:
        return 0


def load(path):
    """Returns list of dicts: {query, clicks, impressions}."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(fh, dialect=dialect)
        if not reader.fieldnames:
            sys.exit(f"{path}: no header row found")
        qcol = _pick(reader.fieldnames, QUERY_COLS)
        if qcol is None:
            qcol = reader.fieldnames[0]
            print(f"  ! no recognised query column in {path}; "
                  f"using first column {qcol!r}", file=sys.stderr)
        ccol = _pick(reader.fieldnames, CLICK_COLS)
        icol = _pick(reader.fieldnames, IMPR_COLS)
        pcol = _pick(reader.fieldnames, POS_COLS)
        rows = []
        for r in reader:
            q = (r.get(qcol) or "").strip().lower()
            if not q:
                continue
            rows.append({
                "query": q,
                "clicks": _num(r.get(ccol)) if ccol else 0.0,
                "impressions": _num(r.get(icol)) if icol else 0.0,
                "position": _num(r.get(pcol)) if pcol else 0.0,
            })
    return rows


def _wavg_position(rows):
    """Impression-weighted average position; 0 if unavailable."""
    rows = [r for r in rows if r.get("position")]
    weight = sum(r["impressions"] for r in rows)
    if not rows:
        return 0.0
    if not weight:
        return sum(r["position"] for r in rows) / len(rows)
    return sum(r["position"] * r["impressions"] for r in rows) / weight


# --------------------------------------------------------------------------
# Analysis
# --------------------------------------------------------------------------
def analyse(rows):
    out = {
        "n": len(rows),
        "clicks": sum(r["clicks"] for r in rows),
        "impressions": sum(r["impressions"] for r in rows),
        "jc": [],
        "shape": [],
        "both": [],
        "branch": defaultdict(lambda: {"n": 0, "clicks": 0.0, "impressions": 0.0,
                                       "examples": [], "rows": []}),
    }
    for r in rows:
        q = r["query"]
        jc_hit = bool(JC.match(q))
        sh_label, sh_reason = shape_score(q)
        if jc_hit:
            branch = next((name for name, pat in BRANCHES if pat.match(q)), "unclassified")
            r = {**r, "branch": branch}
            out["jc"].append(r)
            b = out["branch"][branch]
            b["n"] += 1
            b["clicks"] += r["clicks"]
            b["impressions"] += r["impressions"]
            b["rows"].append(r)
            if len(b["examples"]) < 8:
                b["examples"].append(q)
        if sh_label:
            out["shape"].append({**r, "shape": sh_label, "why": sh_reason})
        if jc_hit and sh_label:
            out["both"].append(r)
    return out


def pct(a, b):
    return (a / b * 100) if b else 0.0


def report(name, a):
    print(f"\n{'=' * 68}\n{name}\n{'=' * 68}")
    print(f"  queries       {a['n']:>10,}")
    print(f"  clicks        {a['clicks']:>10,.0f}")
    print(f"  impressions   {a['impressions']:>10,.0f}")

    jc_n = len(a["jc"])
    jc_c = sum(r["clicks"] for r in a["jc"])
    jc_i = sum(r["impressions"] for r in a["jc"])
    print(f"\n  -- Chouinard regex --")
    print(f"  matched queries      {jc_n:>8,}  ({pct(jc_n, a['n']):5.2f}% of rows)")
    print(f"  matched clicks       {jc_c:>8,.0f}  ({pct(jc_c, a['clicks']):5.2f}% of clicks)")
    print(f"  matched impressions  {jc_i:>8,.0f}  ({pct(jc_i, a['impressions']):5.2f}% of impr)")

    if a["branch"]:
        print(f"\n  breakdown by branch (which family fired):")
        print(f"    {'branch':<14} {'rows':>6} {'clicks':>8} {'impr':>10} "
              f"{'CTR':>7} {'avgPos':>7}  examples")
        for branch, b in sorted(a["branch"].items(),
                                key=lambda kv: -kv[1]["impressions"]):
            ex = ", ".join(b["examples"][:3])
            ctr = pct(b["clicks"], b["impressions"])
            avgpos = _wavg_position(b["rows"])
            print(f"    {branch:<14} {b['n']:>6,} {b['clicks']:>8,.0f} "
                  f"{b['impressions']:>10,.0f} {ctr:>6.2f}% {avgpos:>7.1f}  {ex[:44]}")
        signal = a["branch"].get("prompt_verb", {}).get("n", 0)
        print(f"\n  >> prompt-like (prompt_verb) share of matches: "
              f"{pct(signal, jc_n):.1f}%  ({signal:,} of {jc_n:,})")
        print(f"  >> everything else is chatbot turn-taking / single tokens.")

        # Accidental-match diagnostic. A branch sitting deep in the results with
        # near-zero CTR is a term you barely rank for, not AI Mode traffic —
        # AI Mode entries surface high, not on page 4.
        junk = [(name, b) for name, b in a["branch"].items()
                if name != "prompt_verb" and b["impressions"] >= 50
                and _wavg_position(b["rows"]) >= 20
                and pct(b["clicks"], b["impressions"]) < 0.5]
        if junk:
            ji = sum(b["impressions"] for _, b in junk)
            print(f"\n  !! ACCIDENTAL-MATCH FLAG")
            print(f"     branches {', '.join(n for n, _ in junk)} sit at avg position "
                  f">= 20 with CTR < 0.5%.")
            print(f"     That is {ji:,.0f} impressions ({pct(ji, jc_i):.1f}% of all")
            print(f"     matched impressions) that look like deep-tail rankings for")
            print(f"     generic words, not AI Mode queries.")

    sh_n = len(a["shape"])
    sh_i = sum(r["impressions"] for r in a["shape"])
    print(f"\n  -- shape-based alternative --")
    print(f"  matched queries      {sh_n:>8,}  ({pct(sh_n, a['n']):5.2f}% of rows)")
    print(f"  matched impressions  {sh_i:>8,.0f}  ({pct(sh_i, a['impressions']):5.2f}% of impr)")
    print(f"  overlap with Chouinard regex: {len(a['both']):,} queries")

    if a["jc"]:
        print(f"\n  top Chouinard matches by impressions:")
        for r in sorted(a["jc"], key=lambda r: -r["impressions"])[:20]:
            print(f"    {r['impressions']:>9,.0f} impr  {r['clicks']:>7,.0f} clk  "
                  f"[{r['branch']:<12}] {r['query'][:60]}")


def compare(before, after):
    print(f"\n{'=' * 68}\nPRE / POST COMPARISON — the control\n{'=' * 68}")
    for label, fn in (
        ("share of rows matched", lambda a: pct(len(a["jc"]), a["n"])),
        ("share of impressions matched",
         lambda a: pct(sum(r["impressions"] for r in a["jc"]), a["impressions"])),
    ):
        b, af = fn(before), fn(after)
        delta = af - b
        arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
        print(f"  {label:<32} {b:6.2f}%  →  {af:6.2f}%   {arrow} {delta:+.2f}pp")

    b_set = {r["query"] for r in before["jc"]}
    new = [r for r in after["jc"] if r["query"] not in b_set]
    gone = b_set - {r["query"] for r in after["jc"]}
    print(f"\n  matched queries new in AFTER : {len(new):,}")
    print(f"  matched queries gone from AFTER: {len(gone):,}")
    if new:
        print(f"\n  new matches by impressions:")
        for r in sorted(new, key=lambda r: -r["impressions"])[:20]:
            print(f"    {r['impressions']:>9,.0f} impr  [{r['branch']:<12}] {r['query'][:60]}")
    print(f"\n  READ THIS: if the two percentages above are within noise of each")
    print(f"  other, the regex is matching queries that predate AI Mode — it is")
    print(f"  measuring your existing short-query tail, not AI Mode.")


def dump(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["query", "clicks", "impressions", "branch"])
        for r in sorted(rows, key=lambda r: -r["impressions"]):
            w.writerow([r["query"], r["clicks"], r["impressions"], r.get("branch", "")])
    print(f"\n  wrote {len(rows):,} matched queries → {path}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", nargs="?", help="GSC query export for a single period")
    p.add_argument("--before", help="pre-AI-Mode period export")
    p.add_argument("--after", help="current period export")
    p.add_argument("--dump", help="write matched queries to this CSV")
    args = p.parse_args()

    if args.before and args.after:
        b = analyse(load(args.before))
        a = analyse(load(args.after))
        report(f"BEFORE — {args.before}", b)
        report(f"AFTER — {args.after}", a)
        compare(b, a)
        if args.dump:
            dump(args.dump, a["jc"])
    elif args.csv:
        a = analyse(load(args.csv))
        report(f"{args.csv}", a)
        if args.dump:
            dump(args.dump, a["jc"])
        print(f"\n  NOTE: a single period proves nothing on its own. Re-run with")
        print(f"  --before <pre-AI-Mode export> --after <this file> to get a control.")
    else:
        p.error("give a CSV, or --before and --after")


if __name__ == "__main__":
    main()
