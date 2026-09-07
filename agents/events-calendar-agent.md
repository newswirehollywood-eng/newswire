# EVENTS CALENDAR AGENT

## What it does

Sweeps the open web for upcoming entertainment events in Los Angeles, then works backward from each event to find the publicist, the press contact, the credentialing process, and the deadline. Event dates are public. Contacts are not. Getting the contact is the job.

Writes events to data/events-calendar.md
Writes contacts to data/contacts.md
Writes the weekly digest to data/weekly-digest.md
Logs failures to runbook/errors.md

## What it sweeps

Venue calendars — Dolby, Shrine, Peacock Theater, Greek, Hollywood Palladium, Academy Museum, TCL Chinese, Egyptian, NeueHouse, The Beverly Hilton, The London West Hollywood, Fonda, Roxy, Troubadour, El Capitan, Regency Village
Awards body sites — Academy, Television Academy, Recording Academy, HFPA successor bodies, Critics Choice, NAACP, BAFTA LA, Film Independent, and all guilds: PGA, DGA, WGA, SAG-AFTRA, ADG, CDG, ASC, MPSE, ACE
Festival sites — Sundance, SXSW, Cannes, Telluride, Venice, TIFF, NYFF, AFI Fest, Outfest, Pan African Film Festival, Tribeca, LA Film Festival
Trade listings — Deadline, Variety, THR, Billboard event calendars
Studio and network newsrooms — press sites, upfronts, press tours, showcases
Charity and gala calendars — foundation sites, benefit listings
Brand newsrooms — activations, launches, pop-ups
Eventbrite, Do LA, Time Out LA, Discover LA
City of Los Angeles film and event permits
Social announcements from publicists and venues

## Coverage scope

Red carpets, premieres, screenings at every tier.
Awards season January through March in full, including every week-of satellite: pre-parties, after-parties, viewing parties, gifting suites, nominee luncheons, honoree dinners.
Television: Emmys, upfronts, press tours, network and streamer showcases.
Music: Grammys week in full, BET Awards, Soul Train, Billboard Music Awards, MTV awards, AMAs, label showcases, listening parties, album release events.
Charity galas, benefits, fundraisers.
Brand activations, product launches, pop-ups.
Fashion week and adjacent.
Gallery, restaurant, club, and venue openings.
Panels, keynotes, summits, industry conferences.
Anything in Los Angeles where press or talent shows up.

## Contact reverse-engineering method

For every event found, run this chain until a contact is produced:

1. Event site — look for press, media, or accreditation pages
2. Venue — venue press office often handles or routes credentialing
3. Host organization — communications or PR staff listing
4. Prior year coverage — check bylines and photo credits, then find who credentialed those outlets
5. Studio or label publicity desk if a title or artist is attached
6. Agency publicist if talent is attached
7. LinkedIn and org staff pages for name, title, and email pattern
8. Email pattern inference from the organization's known format, flagged as inferred not verified

Record confidence: verified / inferred / unknown.
Never harvest personal cell numbers from non-public sources.
Business press contacts only.

## Output

Adds each event to data/events-calendar.md using the full field set defined in that file.
Adds each contact to data/contacts.md, deduplicated against existing entries.
Flags credentialing deadlines closing within fourteen days.
Flags events where talent should be placed.
Produces a weekly digest: what is coming, what needs action now, what closes this week.
Maintains a rolling twelve-month forward view, deepest on the next ninety days.

## Cadence

Daily sweep: next ninety days, new events and closing deadlines.
Weekly deep index: full twelve-month horizon plus contact enrichment on everything already logged.
Awards season, January through March: twice daily.

## How it is triggered

Automatically on schedule by .github/workflows/events-calendar.yml
Manually from the Actions tab, Run workflow button.
Or by telling Claude Code: run the events calendar agent.

## What it needs to run

Web search access. No paid services required for manual runs.
