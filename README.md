# Shay's Morning Brief

A warm, visual daily dashboard for Shay Hrobsky — one page, built from her brand guide
(colors: Cedar Green / Oat Milk / Clay Gold / Deep Ink Blue; fonts: Playfair Display + Montserrat).

## How it works

- `brief/template.html` — the page design. Plain HTML/CSS with `$placeholder` tokens
  (Python `string.Template`), no build step.
- `brief/render.py` — fills the template from a data file and writes the final HTML.
  `python3 render.py config/data.json out/YYYY-MM-DD.html`
- `brief/config/data.json` — the day's content. Regenerated fresh each morning by the
  scheduled Claude session described in `brief/PROMPT.md`.
- `brief/PROMPT.md` — the instructions the daily automation follows: what to gather,
  from where, and how to render + deliver the brief.

## Status

- **Live data today:** Google Calendar (today's timeline, tomorrow/week-ahead), weather,
  AI/marketing news, astrology (public transit data).
- **Sample/placeholder today, wire up when ready:** Revenue (Square — connected, first
  live pull needs the daily session to have Square tools loaded), social & email
  performance (Kit — connected, not yet pulled), content calendar (Viraly has no
  connector — kept as manual/organic entry), colleague & competitor watch (needs a
  confirmed name list), family calendar / meal plan / kids' schedule (Family Schedule
  calendar exists in Google Calendar and is checked, but is currently empty).

## Automation

A daily Routine (`create_trigger`, fresh session per firing) runs at 6am America/Chicago,
gathers the day's data per `brief/PROMPT.md`, renders the page, and delivers it to Shay.
