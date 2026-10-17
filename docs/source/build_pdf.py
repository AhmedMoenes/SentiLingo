"""Build the SentiLingo project documentation PDF from the HTML parts in ./parts.

Usage (from the repository root):
    python docs/source/build_pdf.py

Requirements:
    * Google Chrome or Microsoft Edge (used headless to print HTML to PDF).
      Set the CHROME_PATH environment variable if it is installed in a non-standard place.
    * PyMuPDF  (pip install pymupdf) - reads the first render to fill in the table-of-contents page numbers.

Team names, dates and the schedule live in project.json; edit that file and re-run the script.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

SRC = Path(__file__).resolve().parent
DOCS = SRC.parent
OUTPUT = DOCS / "SentiLingo_Project_Documentation_Parts_1-3.pdf"

BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_browser() -> str:
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Chrome/Edge not found. Install one or set CHROME_PATH.")


def day(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def short_date(value: dt.date) -> str:
    return f"{value.day} {value:%b}"


def long_date(value: dt.date) -> str:
    return f"{value.day} {value:%b %Y}"


# --------------------------------------------------------------------------- generated content

def gantt_svg(schedule: dict) -> str:
    start, end = day(schedule["start"]), day(schedule["end"])
    n_days = (end - start).days + 1
    label_w, x0, x1 = 300, 310, 990
    unit = (x1 - x0) / n_days
    colors = {p["name"]: p["color"] for p in schedule["phases"]}

    def x(date: dt.date) -> float:
        return x0 + (date - start).days * unit

    rows = []  # (kind, payload)
    for phase in schedule["phases"]:
        tasks = [t for t in schedule["tasks"] if t["phase"] == phase["name"]]
        if tasks:
            rows.append(("phase", phase["name"], tasks))
            rows.extend(("task", t, None) for t in tasks)

    header_h, ms_row_h, row_h = 44, 26, 20
    top = header_h + ms_row_h
    height = top + len(rows) * row_h + 6
    out = [f'<svg viewBox="0 0 1000 {height}" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">']

    # sprint bands and header
    for i, sprint in enumerate(schedule["sprints"]):
        sx, ex = x(day(sprint["start"])), x(day(sprint["end"])) + unit
        fill = "#f4f6f9" if i % 2 == 0 else "#ffffff"
        out.append(f'<rect x="{sx:.1f}" y="0" width="{ex - sx:.1f}" height="{height}" fill="{fill}"/>')
        out.append(f'<rect x="{sx:.1f}" y="0" width="{ex - sx:.1f}" height="20" fill="#17324d" stroke="#ffffff" stroke-width="1"/>')
        out.append(f'<text x="{(sx + ex) / 2:.1f}" y="14.5" text-anchor="middle" font-size="12" font-weight="600" fill="#ffffff">{sprint["name"]}</text>')
        out.append(f'<text x="{sx + 3:.1f}" y="36" font-size="11" fill="#5b6675">{short_date(day(sprint["start"]))}</text>')
        out.append(f'<line x1="{sx:.1f}" y1="20" x2="{sx:.1f}" y2="{height}" stroke="#d5dbe3" stroke-width="1"/>')
    out.append(f'<text x="0" y="14.5" font-size="12" font-weight="600" fill="#17324d">Task</text>')
    out.append(f'<text x="0" y="36" font-size="11" fill="#5b6675">Sprint start →</text>')
    out.append(f'<line x1="0" y1="{header_h - 2}" x2="1000" y2="{header_h - 2}" stroke="#9aa5b1" stroke-width="1"/>')

    # milestone row and guide lines
    out.append(f'<text x="0" y="{header_h + 17}" font-size="12.5" font-weight="600" fill="#b7791f">Milestones</text>')
    for ms in schedule["milestones"]:
        mx = x(day(ms["date"])) + unit / 2
        cy = header_h + 12
        color = "#c8453b" if ms.get("official") else "#b7791f"
        out.append(f'<line x1="{mx:.1f}" y1="{cy}" x2="{mx:.1f}" y2="{height}" stroke="{color}" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>')
        out.append(f'<path d="M{mx:.1f},{cy - 7} l7,7 l-7,7 l-7,-7 z" fill="{color}"/>')
        right_edge = mx > 960
        lx, anchor = (mx - 9, "end") if right_edge else (mx + 9, "start")
        out.append(f'<text x="{lx:.1f}" y="{cy + 4.5}" text-anchor="{anchor}" font-size="10.5" font-weight="600" fill="{color}">{ms["id"]}</text>')

    # rows
    y = top
    for kind, payload, tasks in rows:
        if kind == "phase":
            color = colors[payload]
            ps = min(day(t["start"]) for t in tasks)
            pe = max(day(t["end"]) for t in tasks)
            out.append(f'<text x="0" y="{y + 14}" font-size="12.5" font-weight="700" fill="{color}">{html.escape(payload)}</text>')
            bx, bw = x(ps), x(pe) + unit - x(ps)
            out.append(f'<path d="M{bx:.1f},{y + 7} h{bw:.1f} v6 l-4,4 l-4,-4 h{-(bw - 8):.1f} l-4,4 l-4,-4 z" fill="{color}" opacity="0.85"/>')
        else:
            task = payload
            color = colors[task["phase"]]
            ts, te = day(task["start"]), day(task["end"])
            bx, bw = x(ts), x(te) + unit - x(ts)
            label = f'{task["id"]}  {task["name"]}'
            out.append(f'<text x="10" y="{y + 14}" font-size="12" fill="#1f2933">{html.escape(label)}</text>')
            out.append(f'<rect x="{bx:.1f}" y="{y + 4}" width="{bw:.1f}" height="13" rx="3" fill="{color}"/>')
        y += row_h

    out.append("</svg>")
    return "\n".join(out)


def milestone_table(schedule: dict) -> str:
    rows = []
    for ms in schedule["milestones"]:
        kind = '<span class="pill lvl-h">Official DEPI</span>' if ms.get("official") else '<span class="pill wont">Internal</span>'
        rows.append(
            "<tr>"
            f'<td class="id">{ms["id"]}</td>'
            f'<td><strong>{html.escape(ms["name"])}</strong></td>'
            f'<td class="nowrap">{long_date(day(ms["date"]))}</td>'
            f"<td>{html.escape(ms['criteria'])}</td>"
            f"<td>{kind}</td>"
            "</tr>"
        )
    return (
        '<table class="compact"><thead><tr>'
        '<th style="width:6%">ID</th><th style="width:24%">Milestone</th><th style="width:12%">Target date</th>'
        '<th style="width:45%">Exit criteria (evidence)</th><th style="width:13%">Type</th>'
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


HEADING_RE = re.compile(r'<h([12])([^>]*)\bid="([^"]+)"([^>]*)>(.*?)</h\1>', re.S)


def plain(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text))).strip()


def toc_entries(body: str) -> list[tuple[int, str, str]]:
    entries = []
    for level, before, anchor, after, inner in HEADING_RE.findall(body):
        if "no-toc" in before + after:
            continue
        entries.append((int(level), anchor, plain(inner)))
    return entries


def toc_html(entries, pages: dict[str, int] | None) -> str:
    lines = []
    for level, anchor, title in entries:
        page = pages.get(title, "") if pages else "00"
        lines.append(
            f'<div class="toc-entry toc-l{level}"><a href="#{anchor}">{html.escape(title)}</a>'
            f'<span class="dots"></span><span class="pg">{page}</span></div>'
        )
    return "\n".join(lines)


# --------------------------------------------------------------------------- assembly & rendering

def assemble(project: dict, toc: str) -> str:
    css = (SRC / "style.css").read_text(encoding="utf-8")
    body = "\n".join(p.read_text(encoding="utf-8") for p in sorted((SRC / "parts").glob("*.html")))
    schedule = project["schedule"]
    # <bdi> isolates each name, so Arabic names do not reorder the surrounding English text.
    names = [f"<bdi>{html.escape(name)}</bdi>" for name in project["members"]]
    repo = project["repo_url"]
    repo_link = "To be added" if "<" in repo else f'<a href="{repo}">{repo}</a>'

    replacements = {
        "GANTT": gantt_svg(schedule),
        "MILESTONE_TABLE": milestone_table(schedule),
        "TOC": toc,
        "PROJECT_NAME": project["project_name"],
        "FULL_TITLE": project["full_title"],
        "PROGRAM": project["program"],
        "TRACK": project["track"],
        "GROUP_CODE": project["group_code"],
        "INSTRUCTOR": project["instructor"],
        "REPO_LINK": repo_link,
        "REPO_URL": repo if "<" not in repo else "To be added",
        "VERSION": project["version"],
        "DATE": project["date"],
        "SUBMISSION_DATE": project["submission_date"],
        "TEAM_LIST": "<br>".join(names),
        "TEAM_ITEMS": "".join(f"<li>{name}</li>" for name in names),
    }
    for key, value in replacements.items():
        body = body.replace("{{" + key + "}}", value)

    leftover = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", body)))
    if leftover:
        sys.exit(f"Unresolved placeholders: {', '.join(leftover)}")

    title = f'{project["project_name"]} — Project Documentation (Parts 1–3)'
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f"<title>{html.escape(title)}</title><style>{css}</style></head><body>{body}</body></html>"
    )


def render(html_text: str, pdf_path: Path, browser: str, workdir: Path) -> None:
    page = workdir / "documentation.html"
    page.write_text(html_text, encoding="utf-8")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--generate-pdf-document-outline",
        f"--user-data-dir={workdir / 'profile'}",
        f"--print-to-pdf={pdf_path}",
        page.as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    if not pdf_path.exists():
        sys.exit("The browser did not produce a PDF.")


def outline_pages(pdf_path: Path) -> dict[str, int]:
    with pymupdf.open(pdf_path) as doc:
        return {plain(title): page for _, title, page in doc.get_toc()}


def main() -> None:
    project = json.loads((SRC / "project.json").read_text(encoding="utf-8"))
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        draft = work / "draft.pdf"

        # Pass 1: placeholder page numbers, to learn where each heading lands.
        first = assemble(project, "")
        entries = toc_entries(first)
        render(assemble(project, toc_html(entries, None)), draft, browser, work)
        pages = outline_pages(draft)

        # Pass 2 (and a safety pass if the layout shifted).
        final = work / "final.pdf"
        for _ in range(3):
            render(assemble(project, toc_html(entries, pages)), final, browser, work)
            new_pages = outline_pages(final)
            if all(new_pages.get(t) == pages.get(t) for _, _, t in entries):
                break
            pages = new_pages

        missing = [t for _, _, t in entries if t not in pages]
        if missing:
            print("Warning: no page found for:", missing)

        with pymupdf.open(final) as doc:
            doc.set_metadata({
                "title": f'{project["project_name"]} — {project["full_title"]}: Project Documentation (Parts 1–3)',
                "author": f'{project["project_name"]} team — {project["program"]}',
                "subject": "Project Planning & Management, Literature Review, Requirements Gathering",
                "keywords": "sentiment analysis, multilingual NLP, Arabic, Egyptian dialect, TF-IDF, LSTM, Transformers, MLflow, Azure ML",
                "creator": "docs/source/build_pdf.py (HTML + headless Chrome)",
                "producer": "PyMuPDF",
            })
            doc.save(OUTPUT, garbage=3, deflate=True)
            print(f"Wrote {OUTPUT} ({doc.page_count} pages)")


if __name__ == "__main__":
    main()
