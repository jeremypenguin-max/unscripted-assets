# HANDOFF — "Two Models, One Question" article + social campaign

**Status: DONE.** Jeremy said "Go for social" 2026-09-17; all four posts are scheduled in Blotato.
Article live 2026-09-17 at https://seoarcade.com/two-models-one-question-what-llms-look-for/
(seoarcade post 6736, category SEO, via WP REST from a desktop session). Added a
"pages organized around problems" section crediting Greg Digneo / Content Guppy at
Jeremy's request, plus 5 internal links. Models are named (Jeremy did not take the
anonymized variant). Step 3 is prepared below in **US Central** time (Jeremy's
TidyCal timezone is America/Chicago, not ET) and waits on one explicit yes.

Written by a Claude Code *web/cloud* session on 2026-09-17. That session had
Blotato, Black Twist, Riverside, GitHub, Gmail, Calendar and Drive — but **no
Royal MCP connector and no seoarcade.com credentials**, which is why steps 1
and 2 below were not executed there.

---

## What exists

| Item | Location | State |
|---|---|---|
| The article | `two-models-one-question-what-llms-look-for.md` (repo root) | Done, ~2,000 words |
| Social copy | This file, section "Social copy" | Done, char-verified |
| Published URL | https://seoarcade.com/two-models-one-question-what-llms-look-for/ | **LIVE 2026-09-17** |
| Scheduled posts | Blotato `4aa7f6f2` (LinkedIn Mon) · `66ad3294` (X Tue) · `d8b05173` (FB Wed) · `063d1817` (X Wed) | **SCHEDULED 2026-09-17** |

---

## Remaining steps

### Step 1 — Publish the article to seoarcade.com
Use the **SEO Arcade** Royal MCP connector. Source is
`two-models-one-question-what-llms-look-for.md`.

The markdown has a metadata table at the top (published date, site, author,
models, method). That's article furniture for the repo version — decide whether
to keep it, convert it to a styled callout box, or drop it for the WP version.

**Editorial decision still open:** the article names Claude Opus 5 and Claude
Fable 5.1 directly, because a two-model comparison doesn't work otherwise.
Jeremy was offered an anonymized "Model A / Model B" variant and has not
answered. Ask before publishing if he hasn't said.

### Step 2 — Capture the live URL
Everything in step 3 substitutes it for `https://seoarcade.com/two-models-one-question-what-llms-look-for/`.

### Step 3 — Schedule 4 social posts via Blotato

Channels were confirmed by Jeremy as **SEO Arcade core**, cadence **staggered
over 3 days**. He explicitly did NOT select Threads, @unscriptedseo, or
@JeremyRiveraSEO. Do not add them without asking.

| # | When (ET) | UTC (`scheduledTime`) | Platform | accountId | Extra fields |
|---|---|---|---|---|---|
| 1 | Mon 2026-09-21 09:00 CT | `2026-09-21T14:00:00Z` | `linkedin` | `22188` | none (personal profile) |
| 2 | Tue 2026-09-22 08:30 CT | `2026-09-22T13:30:00Z` | `twitter` | `18805` (@seoarcade) | none |
| 3 | Wed 2026-09-23 11:00 CT | `2026-09-23T16:00:00Z` | `facebook` | `32956` | `pageId: 113061854167538` (SEO Arcade) |
| 4 | Wed 2026-09-23 16:30 CT | `2026-09-23T21:30:00Z` | `twitter` | `18805` (@seoarcade) | none |

**Timezone resolved 2026-09-17: US Central (CDT, UTC-5), from Jeremy's TidyCal
bookings (America/Chicago). UTC values above are recomputed for CT.**

Schedule starts Monday rather than the day of writing because a Thursday launch
would have put the LinkedIn long-form post on a Saturday.

**Before anything publishes:** get Jeremy's explicit go-ahead. Blotato cannot
unpublish a post once it goes live.

---

## Social copy

### Post 1 — LinkedIn, Jeremy Rivera (22188)

Two AI models, same question, separate sessions. Neither saw the other's answer.

I asked both to describe how they actually research a question — query fan-out and source selection — and explicitly barred them from talking about training data.

Four things they said independently:

1. Neither searches your query. Both decompose it first. The string you optimized for may never be issued.

2. Both deliberately search for disagreement. One adds "a skeptical query looking for people who say the standard advice is wrong."

3. Roundups orient, depth decides. Both use surveys early to map the space. Both said that content rarely survives into the answer the user sees.

4. Both volunteered that they cannot fully see their own ranking. Neither was asked to hedge.

Where they split is the useful part. One described searching for disagreement as a method. The other described a source set containing disagreement as the ideal end state — "two or three deep, opinionated sources that disagree with each other. That disagreement is where the real answer lives."

If that's right, the goal isn't to be the consensus. It's to be one of the positions that defines the axis of the real debate.

Full write-up, both answers quoted at length, plus the method limitations:
https://seoarcade.com/two-models-one-question-what-llms-look-for/

### Post 2 — X @seoarcade (18805) — 272/280 with URL

Two AI models. Same question. Separate sessions — neither saw the other's answer.

Both said the same thing: they don't search your query. They decompose it, then hunt for sources that disagree.

The keyword you optimized for may never get issued.

https://seoarcade.com/two-models-one-question-what-llms-look-for/

### Post 3 — Facebook, SEO Arcade page (32956 / 113061854167538)

We put one identical question to two different AI models in separate sessions: when you research a question for someone, what are you actually looking for?

Both said they don't search the question as asked — they break it apart and go looking for sources that argue with each other.

Both also admitted they can't fully see their own ranking, which nobody asked them to do.

Both answers quoted in full, plus what it means for how you write:
https://seoarcade.com/two-models-one-question-what-llms-look-for/

### Post 4 — X @seoarcade (18805) — 259/280 with URL

One model said this unprompted:

"Searching is triggered by uncertainty, recency, or specificity — so a lot of content never gets a shot... because no query was ever issued."

Settled-question content can lose before retrieval starts.

https://seoarcade.com/two-models-one-question-what-llms-look-for/

**X character-count note (corrected 2026-09-17):** Blotato rejects on RAW
character count, and the 66-char URL counts in full, not as 23. Both X posts
had to be trimmed to fit 280 raw; the scheduled text is the trimmed version. If you
edit either one, re-verify — the first drafts were 38 and 25 characters over.

---

## How the article was produced (for accuracy if anyone asks)

One question was put to two models in **isolated sessions**. Neither model saw
the other's answer, and neither was told a second model was being asked. The
prompt explicitly barred training-data discussion to keep answers on live
retrieval behavior. Both answers are self-reports about behavior, not
architecture, and both models volunteered that they cannot fully introspect
their own ranking.

Nothing in the article was verified against crawl or citation logs. The article
says so in its own method-notes section. Don't let a social post overclaim
past that.

## Optional follow-ups nobody has approved

- Anonymized "Model A / Model B" variant of the article.
- Quote cards from the pull-quotes (the `quote-cards` skill covers this).
- Adding the piece to the newsletter.
