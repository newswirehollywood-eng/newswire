# HOUSE STYLE

To be defined by Terry. Until then, agents default to AP style with entertainment trade conventions.

## Sourcing standard

To be set. Placeholder: two independent sources before publishing an unconfirmed claim, or one on-record source.

## Corrections

Corrections are posted, not deleted. Required for news aggregator eligibility.

## Embargo

Embargoes are hard stops. Breaking one costs credentialing access.

## Bylines — desk convention, confirmed 2026-09-10

We publish under desk bylines, not individual names, until real staff are attached to a desk in `data/masthead.json`. This is standard practice at Variety, Deadline, TMZ, and AP.

**Hard rule, no exceptions:** never invent a person. No fabricated reporter names, no made-up staff, no placeholder humans — in a byline, in structured data, anywhere. If there's no real person attached to a desk, the byline is the desk, full stop. A credentialed newsroom caught with a fake masthead is finished.

**Standing desks:**

| Desk | Covers |
|---|---|
| Newswire Hollywood Staff | general / publication-level |
| Breaking News Desk | rapid response, developing stories |
| Film Desk | film |
| Television Desk | TV |
| Music Desk | music |
| Style Desk | fashion, red carpet looks, best-dressed |
| Deals Desk | business, dealmaking, executive moves |
| AI & Technology Desk | AI and big tech in entertainment |
| Awards Desk | seasonal, January–March, guild through Oscars |
| Red Carpet Desk | carpets, premieres, arrivals, party coverage |
| Global Desk | international, affiliate and syndicated |
| Photo Desk | image credits and captions |
| Calendar Desk | the Hollywood events calendar (already in use on site, not in the original list but a natural fit for Division Five) |

**Byline format on published items:**
- Desk only: `By the Film Desk, Newswire Hollywood`
- Real named person: `By [Name], [Title], Newswire Hollywood`
- Mixed: `By [Name] and the Awards Desk, Newswire Hollywood`

Structured data (`author` in JSON-LD) should match the visible byline — same desk name, `@type: Organization` for a desk-only byline, never a fabricated `Person`.
