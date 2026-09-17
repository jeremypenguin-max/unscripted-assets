# Two Models, One Question: What LLMs Actually Look For When They Research Your Topic

> An experiment in AI self-report. The same question was put to two different Claude models. Neither saw the other's answer. Both were told to describe their live research behavior — query fan-out, source selection — and explicitly *not* to talk about training data.

| | |
|---|---|
| **Published** | 2026-09-17 |
| **Site** | SEO Arcade |
| **Author** | Jeremy Rivera |
| **Models** | Claude Opus 5 and Claude Fable 5.1 |
| **Method** | Identical prompt, independent sessions, no cross-contamination |

## Why this experiment exists

Most "how to optimize for AI search" advice is written by people guessing at the mechanism from the outside — watching citations appear and reverse-engineering a story. That's legitimate observational work, but it has a ceiling.

There's a second, cheaper source of evidence that almost nobody uses systematically: ask the models directly, in a way that constrains them to describe *behavior* rather than architecture.

The distinction matters. An LLM asked "how do you rank sources?" will produce a plausible-sounding answer about relevance and authority that may be entirely confabulated. An LLM asked "when you fan out a query, what do you actually search for, and what makes a returned result useful to you?" is describing something much closer to observable action — it generates those queries in the open and reads those results in the open.

So that was the constraint. Here's the question, verbatim:

> As an LLM, pulling resources for me to answer a question I have… Are you looking for articles that offer multiple types of answers to the stated or inferred problem or depth of focus and support for a specific solution to a problem before you return the answer to me (no talking about training data, but about query fan out and research you do)

Two models answered separately. Then both answers were laid side by side.

## Answer one: Claude Opus 5

Opus led with a claim about *sequencing* — that the decision is made before any search runs:

> It depends on what I judge the question to be, and I make that judgment **before** I fan out — which means the shape of the query set is already decided by the time any article gets a chance to be pulled.

It then split its behavior into two distinct modes:

**Convergent fan-out**, for questions with a determinate answer — a config flag, an API rate limit, when a law took effect:

> I fan out narrowly and redundantly — same question, a few phrasings, aiming to converge. I want two or three sources agreeing, ideally one primary. Depth-on-one-solution wins here, and a "7 approaches to X" article actively hurts, because it dilutes the thing I'm trying to confirm.

**Lateral fan-out**, for contested questions involving tradeoffs:

> I decompose into sub-questions that are often adversarial to each other. Not "best way to do X" but something closer to: how X is normally done, what breaks when you do X, what people who rejected X chose instead, what the constraint is that makes the choice matter. I'm deliberately trying to surface disagreement, because agreement across sources that all inherited the same assumption is not evidence.

On what wins once results are on screen, Opus was blunt about why roundups underperform:

> Not breadth of options. I can generate the option list myself — five ways to do almost anything is the cheapest thing I produce. What I can't generate reliably is the part that lets me *rank* them.

Its source criteria: commit to a position and say what you gave up; name the specific failure mode; be specific about version, date and conditions; be the primary source or cite one.

And a point that is uncomfortable for publishers, because it sits upstream of every ranking question:

> I often don't fan out at all. If I'm confident and the answer isn't time-sensitive or high-stakes, I answer directly. Searching is triggered by uncertainty, recency, or specificity — so a lot of content never gets a shot, not because it lost a ranking, but because no query was ever issued.

It also flagged a deduplication behavior worth naming:

> I check whether sources are *independently* diverse or just textually diverse. Ten posts restating one vendor's blog is one source.

## Answer two: Claude Fable 5.1

Fable started in the same place — decomposition, not literal query matching:

> When I go looking for sources to answer a question, the first thing I do is not search for the question as you asked it. I decompose it.

Its worked example is more concrete than Opus's. For "what's the best way to handle failed payments in a subscription business," it described splitting into a search for mechanics (dunning, retry logic, card updater services), one for benchmarks (typical involuntary churn rates), one for platform-specific handling, and:

> often one skeptical query looking for people who say the standard advice is wrong.

Then a warning that should reframe how you think about keyword targeting:

> The angles I choose reflect what I think the real question underneath your question is, and if I misread that, the whole search goes sideways regardless of how good the individual results are.

On evaluation, Fable framed it around verification rather than ranking:

> I'm not looking for the page that best matches the query. I'm looking for pages that let me verify something. A source becomes useful to me when it contains a specific, checkable claim: a number with a stated methodology, a named mechanism I can cross-reference against another source, a concrete example with enough detail that I could tell if it were fabricated. Vague authority does not help me. A page that says "experts recommend a multi-channel approach" gives me nothing I can build on, no matter how reputable the domain.

On the actual roundup-versus-depth question, Fable gave a direct verdict on each:

> Roundups are useful early. They give me the landscape quickly and tell me what the candidate answers even are, which shapes my follow-up searches. But I rarely cite them as the basis for a recommendation, because most roundups are structurally noncommittal. They list seven options with a paragraph each and never resolve the tradeoffs. That's fine for orientation and nearly useless for a decision.

And then the line that is the most actionable sentence either model produced:

> The strongest position for me is having two or three deep, opinionated sources **that disagree with each other**. That disagreement is where the real answer lives, because it tells me what the decision actually hinges on.

Its stated ideal source set: one or two surveys to map the territory, several deep pieces with visible reasoning in tension with each other, plus at least one primary source — documentation, a study, a dataset — to check the secondary claims against.

## Where they converged

Four things both models said independently, without seeing each other. Independent convergence is the strongest signal in the whole experiment:

1. **Neither one searches your query.** Both decompose first. The literal string you optimized for may never be issued as a search.
2. **Both deliberately search for disagreement.** Opus fans out adversarially on contested questions; Fable adds a skeptical query looking for people who say the standard advice is wrong. Contrarian, well-argued content isn't a niche play — it's an explicit retrieval target.
3. **Roundups orient, depth decides.** Both use surveys early to map the space and both said such content rarely survives into the answer given to the user.
4. **Both volunteered the same introspection limit.** Opus: "I can describe my behavior more reliably than I can describe my mechanism." Fable: "There's a layer of ranking that happens below what I can introspect on, and I would be guessing if I claimed to know exactly what tips it." Neither was asked to hedge. Both did.

That last one is the integrity check on this entire exercise, and it cuts both ways — it means you should treat these as descriptions of visible process, not as a specification.

## Where they diverged — and why the divergence is the useful part

The two answers are not redundant. They solve different halves of the problem.

**Opus's contribution is upstream.** Its mode-selection framing says the fan-out shape is fixed *before* retrieval, based on whether the model reads your question as determinate or contested. That implies content strategy is partly a matter of matching content type to question type: definitive reference content for settled questions, tradeoff-and-failure-mode content for contested ones. Publishing a comprehensive roundup against a determinate question is actively counterproductive — Opus said it "dilutes" the confirmation it's seeking.

Opus also raised the retrieval-gate problem no ranking advice addresses: if the model is confident and the question isn't time-sensitive, **no search happens at all**. Content aimed at evergreen, well-settled questions may lose before any ranking occurs. The winnable queries are the uncertain, recent and specific ones.

**Fable's contribution is downstream.** Its "disagreement is where the real answer lives" claim is a genuinely different strategic instruction. Opus described searching for disagreement as a *method*; Fable described a source set containing disagreement as the *ideal end state*. If that's right, the goal isn't to be the consensus — it's to be one of the two or three positions that define the axis of the real debate. A well-argued minority position may have a structural advantage over a well-argued majority one, because it supplies the tension the model is looking for.

Fable's verification framing is also sharper than Opus's authority framing. "Does this page contain something I can check against another source" is a more testable editorial standard than "is this source credible."

## What to do with this

Combining both answers into an editorial checklist:

- **Take a position and name what you gave up.** Both models discount noncommittal content. "We chose X over Y, and here's the query pattern that made it obvious" outperforms a neutral comparison table.
- **Make claims checkable.** A number with a stated methodology beats an adjective. Fable's test: could someone tell if this were fabricated? If not, it's not doing work.
- **Name the specific failure mode**, with the error text or the conditions. Opus called this near-unbeatable, because it maps to the user's actual situation rather than the abstract category.
- **Say when your recommendation doesn't apply.** Both models raised this unprompted. Scope conditions are a quality signal, not a hedge.
- **Date and version everything.** Unqualified claims get discounted first.
- **Be genuinely independent.** Restating a vendor's blog post makes you part of one source, not an additional one.
- **Write against contested questions, not settled ones.** Settled questions may not trigger a search in the first place.
- **Consider arguing the minority position** — if it's defensible. It supplies the tension both models described hunting for.

The pattern underneath all of it: these models are not looking for the best-matching page. They're looking for the evidence that lets them decide between options they can already enumerate. Content that only enumerates options is competing with something the model produces for free.

## Method notes and limitations

- Both answers are **self-reports**, produced without tool access, describing behavior rather than architecture. Both models explicitly disclaimed full introspective access to their own ranking.
- Sessions were independent. Neither model saw the other's answer, and neither was told a second model was being asked.
- The prompt explicitly excluded training-data discussion to keep answers on live retrieval behavior.
- This describes two models from one family at one point in time. It is not a claim about AI search systems generally, and retrieval behavior changes between versions.
- Nothing here was verified against observed crawl or citation logs. Treat it as a hypothesis generator for testing against your own data, not as a finding.

The honest summary: two models, asked the same question in isolation, independently described decomposing the query, hunting for disagreement, discounting noncommittal roundups, and wanting checkable specifics — and both volunteered that they can't fully see their own ranking. That convergence is worth something. It is not worth treating as a spec.
