# RUNBOOK

How the system operates. Every agent handoff is written here with explicit file paths. Nothing is assumed.

## Handoff chain — originated stories

Story Scout writes to data/story-queue.md
Assignment Desk reads data/story-queue.md, writes to data/assignments.md
Writer reads data/assignments.md, writes drafts to data/drafts/
Copy Desk reads data/drafts/, marks approved or returns
Headline and SEO reads approved drafts, adds metadata
Photo and Assets attaches images with license source recorded
Publishing pushes live after named human sign-off
Distribution syndicates to affiliate channels
Analytics reports back to data/performance.md

## Handoff chain — syndicated in

Intake writes to data/syndicated-queue.md with source and attribution
Copy Desk verifies attribution
Publishing runs it tagged SYNDICATED

## Handoff chain — paid out

Client intake writes to data/paid-queue.md
Formatting to house template
Publishing runs it labeled SPONSORED, distributes to affiliate channels

## Error log

Every failure gets logged in runbook/errors.md. What broke, why, what fixed it.
