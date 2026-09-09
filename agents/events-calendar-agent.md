# EVENTS CALENDAR AGENT

This agent is now real and runnable. Its definition — what it does, what it sweeps, the contact reverse-engineering chain, where it writes, and its standards — lives at `.claude/agents/events-calendar-agent.md`, where Claude Code can actually load it.

This file stays only as a signpost so nothing in `/agents/` silently goes stale. Read the file above for the current, authoritative version. Do not edit this description separately from that one.

## How to run it

Quit and restart Claude Code so the agent file loads, run `/agents` to confirm "events-calendar-agent" appears in the list, then say "run the events calendar agent." That costs nothing beyond the Claude Code session already in use.

Running it unattended on a schedule (no one triggering it) is a separate, not-yet-built piece — it needs a paid Anthropic API connection wired into a GitHub Actions workflow, which is real ongoing cost and needs Terry's sign-off before it's built.
