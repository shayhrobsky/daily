#!/usr/bin/env python3
"""Renders the morning brief HTML from a data JSON file.

Usage: python3 render.py data.json out.html
"""
import json
import sys
import html
from pathlib import Path
from string import Template

BRIEF_DIR = Path(__file__).parent


def esc(v):
    if isinstance(v, str):
        return html.escape(v, quote=False)
    return v


def list_items(items):
    """Render a list of plain strings as <li> rows, escaped."""
    if not items:
        return '<li>Nothing flagged &mdash; a quiet, clear list this morning.</li>'
    return "\n".join(f"<li>{esc(i)}</li>" for i in items)


def timeline_rows(events):
    """events: list of {time, title, meta, flag(optional)}"""
    if not events:
        return '<div class="tl-row"><div class="tl-time"></div><div class="tl-body"><strong>Nothing on the calendar.</strong><span>A genuinely open day &mdash; rare, use it well.</span></div></div>'
    rows = []
    for e in events:
        flag = f'<span class="tl-flag">{esc(e["flag"])}</span>' if e.get("flag") else ""
        rows.append(
            f'<div class="tl-row"><div class="tl-time">{esc(e["time"])}</div>'
            f'<div class="tl-body"><strong>{esc(e["title"])}</strong>'
            f'<span>{esc(e.get("meta",""))}</span>{flag}</div></div>'
        )
    return "\n".join(rows)


def followup_flags(chase, connect, delegate):
    def block(label, cls, items):
        if not items:
            return ""
        tags = "".join(f'<div><span class="tag {cls}">{label}</span>{esc(i)}</div>' for i in items)
        return tags
    parts = [
        block("Chase", "tag-chase", chase),
        block("Connect", "tag-connect", connect),
        block("Delegate", "tag-delegate", delegate),
    ]
    parts = [p for p in parts if p]
    if not parts:
        return '<p>Nothing to chase, connect, or delegate right now.</p>'
    return '<div style="display:flex;flex-direction:column;gap:7px;">' + "".join(parts) + "</div>"


def habit_pills(habits):
    """habits: list of {label, done(bool)}"""
    if not habits:
        return ""
    out = []
    for h in habits:
        cls = "habit-pill done" if h.get("done") else "habit-pill"
        out.append(f'<span class="{cls}">{esc(h["label"])}</span>')
    return "\n".join(out)


def friday_card(data):
    if not data.get("is_friday"):
        return ""
    return (
        '<div class="card card--priority">'
        '<div class="card-head"><span class="card-icon">🗝️</span>'
        '<span class="card-title">Friday CEO Time<small>Weekly review prompt</small></span></div>'
        f'<div class="card-body">{esc(data.get("friday_ceo_prompt",""))}</div></div>'
    )


def main():
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BRIEF_DIR / "config" / "data.json"
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else BRIEF_DIR / "out" / "brief.html"

    data = json.loads(data_path.read_text())

    tmpl = Template((BRIEF_DIR / "template.html").read_text())

    subs = dict(data)  # shallow copy; expects mostly-flat strings/numbers
    subs["waiting_on_me_items"] = list_items(data.get("waiting_on_me", []))
    subs["today_timeline_rows"] = timeline_rows(data.get("today_events", []))
    subs["marketing_ideas_items"] = list_items(data.get("marketing_ideas", []))
    subs["ai_news_items"] = list_items(data.get("ai_news", []))
    subs["competitor_moves_items"] = list_items(data.get("competitor_moves", []))
    subs["trending_automation_items"] = list_items(data.get("trending_automation", []))
    subs["trending_online_items"] = list_items(data.get("trending_online", []))
    subs["yesterday_wins_items"] = list_items(data.get("yesterday_wins", []))
    subs["followup_flags"] = followup_flags(
        data.get("chase", []), data.get("connect", []), data.get("delegate", [])
    )
    subs["habit_pills"] = habit_pills(data.get("habits", []))
    subs["friday_ceo_card"] = friday_card(data)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(tmpl.safe_substitute(subs))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
