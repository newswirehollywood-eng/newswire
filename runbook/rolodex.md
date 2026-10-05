# THE ROLODEX

Terry's private contact book. Publicists, press offices, studio desks, venues,
talent reps, label contacts, international outlets.

**Standing instruction from Terry, 2026-09-27:** this is private, it is his own
record, and he wants to export it to PDF every month or two for his files. It is
allowed to grow large — he said twenty thousand entries would not be too many.

---

## WHY IT IS NOT IN THIS REPO

**This repository is public.** Anyone can read it.

On 2026-09-27 a sweep found named publicists' direct work emails and phone
numbers sitting in `data/contacts.md`, `data/events-calendar.md`,
`runbook/priority-board.md` and `runbook/photo-sourcing.md` — visible to the
whole internet. Among them a Television Academy Emmy press contact, two Disney
publicists, two Warner Bros. Discovery media relations staff, SAG-AFTRA's Chief
Communications Officer, and an AEG contact.

Those are the exact people Newswire Hollywood is about to apply to for press
access. A publicist who discovers a new outlet republished their direct line on
a public site does not take that outlet's call again — and they tell colleagues.
It would have been a self-inflicted wound at the precise moment the applications
went out.

All of it is now redacted from the public files, replaced with a pointer here.

### What redaction does and does not fix

Removing the text from the current files stops it being read on the site, in the
repo browser, and by the scrapers that harvest GitHub for addresses. That is the
bleeding stopped.

**It does not remove it from git history.** Every past commit still contains the
original text, and anyone who knows to look can retrieve it. Purging history
means rewriting every commit and force-pushing, which breaks any existing clone
and is a real decision, not a cleanup. Flagged for Terry rather than done
quietly. Given the contacts are business addresses rather than private
individuals', the practical risk is low and dropping over time — but he should
know the history is there, and decide.

---

## WHAT IS AND IS NOT PUBLIC

A working distinction, and a professional one.

**Published press-office contacts stay in the public repo.** These exist to be
found and used by outlets. Keeping them helps the newsroom and harms nobody:

- `Credentials@oscars.org` — the Academy's published credentials address
- `media.help@apple.com` — Apple's published press-asset contact
- `news@sagaftra.org`, `sagaftracommunications@sagaftra.org` — general inboxes
- `info@distinctiveassets.com`
- (310) 247-3000 — Academy main press line

**Named individuals' direct lines go in the Rolodex only.** A person's direct
work email or desk phone is not ours to republish, however we obtained it.

---

## WHERE IT LIVES

Not yet built — Terry said it does not have to be done immediately, only noted
and not forgotten. Consider this the note.

**Recommended home: Google Drive.** Terry's Google account is already connected
to this workspace. It is private to him, reachable from his phone, exports to
PDF in two taps, and survives any repo change. It also means no private data
passes through a public repository again.

Alternatives if he prefers:

- **A second, private GitHub repo.** Keeps everything in one system and lets the
  agents read it directly. Requires Terry to create it; it cannot be created
  from this session.
- **A spreadsheet in Drive.** Simplest to hand to a team member later, sorts and
  filters natively, exports to PDF directly.

---

## STRUCTURE

One row per contact. Designed so it stays useful at twenty entries and at twenty
thousand.

| Field | Notes |
| --- | --- |
| Name | |
| Title | |
| Organization | |
| Division / brand | e.g. HBO Max within Warner Bros. Discovery |
| Category | Studio · Streamer · Network · Label · Venue · Awards body · Talent rep · Agency · International · Media · Other |
| Email | |
| Phone | |
| Assistant / second contact | The person who actually answers |
| City | |
| Territory | US · UK · Korea · Japan · Brazil · etc. |
| Source | Where we got it, and whether VERIFIED or INFERRED |
| First contacted | |
| Last contacted | |
| Status | Cold · Contacted · Responded · Active · On list · Opted out · Bounced |
| Bounce count | Three strikes and it is retired |
| Relationship owner | Which of us deals with this person |
| Notes | Titles they handle, what they have given us, what they asked for |

### The two fields that make it worth having

**Source with confidence.** An inferred address emailed as if confirmed is how
outlets get marked as spam. The events calendar already works this way and it
should carry through.

**Opted out, honoured permanently.** Already the standing rule in
`data/contacts.md`. Someone who asks to be removed is never pitched again — by
Terry, by an agent, by anyone. That rule is what keeps a list this size
legitimate rather than a liability.

---

## WHERE THE ENTRIES COME FROM

Already generating contacts, none of it currently flowing into one place:

1. **The events calendar sweeps** — `data/events-calendar.md` already holds
   publicists, press offices and credentialing routes for fourteen LA events,
   with confidence marked.
2. **Studio press applications** — every portal registration produces a named
   contact on reply. See `runbook/studio-press-access.md`.
3. **Every story filed** — the publicist who supplies a photo or confirms a fact
   is a contact.
4. **PR STARPOWER's existing book** — Terry's own relationships, which are
   likely the most valuable entries and exist nowhere in this system yet.
5. **International desks** — the opening nobody else is working.

---

## MONTHLY PDF

Terry's stated cadence: every month or two, exported for his own records.

From a Drive spreadsheet this is File → Download → PDF. If it ends up in a repo
instead, a small script can render it, and that script should sort by category
then organization so the PDF reads like an actual Rolodex rather than a dump.

---

## NEXT STEP WHEN TERRY WANTS IT

One decision from him: **Drive, or a private repo.**

Then: create it, migrate the redacted contacts out of git into it, seed it from
the events calendar and the studio applications, and set a standing rule that
every new contact goes there and never into the public repo.


## UPDATE 2026-10-05: THE ROLODEX NOW LIVES IN GOOGLE DRIVE

Terry chose Google Drive. The private Rolodex is a Google Sheet called
"ROLODEX - Terry Bryant (PRIVATE)" in the folder "Global Spotlight HQ (Private)"
in Terry's own Drive (matariterry account). It was seeded with 94 entries: the 15
named contacts redacted from this repo, plus press and accreditation offices for
every event on the Global Spotlight calendar, the gift-suite producers, sponsors
and the tech press offices.

Rule from here on: new named contacts go into the Drive sheet only, never into
this public repo. For the monthly PDF: open the sheet, then File, Download, PDF.
