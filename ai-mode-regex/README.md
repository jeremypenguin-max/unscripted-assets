# AI Mode query regex — apply & validate

Tooling to actually run Jean-Christophe Chouinard's "detect AI Mode queries in
GSC" regex against real Search Console data, instead of taking it on faith.

## What it does

1. Applies the regex **verbatim** as posted.
2. Attributes every match to a **branch family** — the thing the post doesn't
   show. `prompt_verb` ("please write a…", "can you explain…") is the part that
   plausibly indicates an LLM-style query. `affirm` / `chatbot_nav` / `thanks` /
   `greeting` are conversational turn-taking tokens (`yes`, `ok`, `more`,
   `next`, `help`, `all`, `any`) that match single common words.
3. Flags **accidental matches** — branches sitting at average position ≥ 20 with
   CTR < 0.5%. That is the signature of barely ranking for a generic word, not
   of AI Mode traffic.
4. Scores a **shape-based alternative** (long, natural-language, constraint-laden
   queries) and reports overlap.
5. Runs a **pre/post control**, which is the only thing that makes any of it
   mean something.

## Getting the data

Search Console → Performance → Search results → Queries tab → Export → CSV.
Do it twice:

- **before** — a date range that predates AI Mode in your market
- **after** — the most recent equivalent-length range

Use equal-length windows or the percentages aren't comparable. GSC keeps 16
months, so the pre-period window is tight.

Column names are auto-detected; the standard GSC export
(`Top queries, Clicks, Impressions, CTR, Position`) works as-is, as does the
BigQuery bulk export.

## Usage

```bash
# single period — descriptive only
python3 aimode_regex.py queries.csv

# with the control
python3 aimode_regex.py --before pre-ai-mode.csv --after current.csv

# export matches for manual review
python3 aimode_regex.py current.csv --dump matched.csv
```

No dependencies beyond the Python 3 standard library.

## Reading the output

- **prompt-like share of matches** — if this is a small fraction, the regex is
  mostly matching filler tokens, and the headline match rate is not an AI Mode
  measurement.
- **ACCIDENTAL-MATCH FLAG** — impressions attributable to deep-tail rankings on
  generic words. Subtract these before drawing any conclusion.
- **pre/post delta** — if the matched share barely moves between the two
  periods, the pattern is matching queries that existed before AI Mode existed.

## Known limits of the method itself

- **GSC anonymization.** Queries issued by too few users are omitted from the
  Performance report entirely. Genuine AI Mode prompts are near-unique and
  mostly fall below that threshold — so the queries the method most wants to
  find are the ones GSC will never show. What survives is high-frequency short
  strings, which is where false positives live.
- **Corpus mismatch.** The pattern's travel-specific branches (`show on map`,
  `more hotels`, `more attractions`, `yes,? pricing`) indicate it was derived
  from a conversational travel-booking assistant log. Those are multi-turn
  continuation utterances. Queries entering GSC from AI Mode are first-turn.
- **Case and punctuation.** GSC lowercases queries and strips punctuation, so
  the pattern works there as written. Add `(?i)` and handle trailing `?` before
  using it on BigQuery exports or raw LLM logs.
- **RE2.** GSC uses RE2, so this pattern is linear-time and safe to paste into a
  Custom (regex) filter. The `^…$` anchoring is correct for GSC's partial-match
  default.
