# unscripted-assets

Asset host for Jeremy Rivera's Unscripted podcast network and SEO Arcade.
Mostly published media — clips, quote cards, impact cards, GIFs — referenced by
public URL from WordPress posts, social scheduling tools, and show notes.

Because files here are hot-linked from live pages and scheduled posts,
**renaming or deleting an existing asset can break a published page or a
queued post.** Add new files rather than repointing old ones. Slugs are
lowercase-hyphenated and usually lead with the guest name
(`dan-kurtz-ssl-recrawl-trick.mp4`).

## Open handoffs

Files matching `HANDOFF-*.md` at the repo root are **work in progress that a
previous session could not finish**, usually because it lacked a connector or
a credential. Each one states its own status.

**If a `HANDOFF-*.md` says `Status: OPEN`, read it before starting related
work** — it carries decisions already made with Jeremy (approved channels,
schedules, editorial calls) that are expensive to re-litigate and easy to
contradict by accident.

Mark one `Status: DONE` when it is finished, or delete it.

## Publishing

The three WordPress sites — unscriptedsmallbusiness.com, seoarcade.com,
unscriptedseo.com — are reached through the Royal MCP connectors (Unscripted
SMB, SEO Arcade, Unscripted SEO). **These are not available in Claude Code web
sessions**, only on the desktop install. A cloud session can write and commit
an article but cannot publish it; that is the usual reason a handoff exists.

Social scheduling runs through Blotato (`blotato_list_accounts` first — the
account IDs and required per-platform fields come from there). Blotato cannot
unpublish a post once it is live, so **confirm copy, destination and timing
with Jeremy before scheduling anything outward-facing.**
