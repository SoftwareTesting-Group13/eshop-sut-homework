#!/usr/bin/env python3
"""Render the HW03 Markdown reports to HTML (PDF is produced by html_to_pdf.js)."""
import os
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = [
    ("reports/main-report.md", "reports/main-report.html", "HW03 — Main report"),
    ("reports/ai-audit.md", "reports/ai-audit.html", "HW03 — AI Audit Report"),
    ("reports/ai-critique.md", "reports/ai-critique.html", "HW03 — AI Critique"),
]

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
       font-size: 10.5pt; line-height: 1.45; color: #1f2937; max-width: 100%; }
h1 { font-size: 20pt; border-bottom: 2px solid #1f4e78; padding-bottom: 4px; margin-top: 22px; }
h2 { font-size: 15pt; color: #1f4e78; margin-top: 20px; }
h3 { font-size: 12.5pt; color: #374151; margin-top: 16px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 8.8pt; }
th, td { border: 1px solid #cbd5e1; padding: 4px 6px; vertical-align: top; }
th { background: #1f4e78; color: #fff; text-align: left; }
tr:nth-child(even) td { background: #f8fafc; }
code { background: #f1f5f9; padding: 1px 4px; border-radius: 3px; font-size: 9pt; }
pre { background: #0f172a; color: #e2e8f0; padding: 10px; border-radius: 6px; overflow-x: auto; font-size: 8.5pt; }
pre code { background: transparent; color: inherit; padding: 0; }
blockquote { border-left: 4px solid #94a3b8; margin: 10px 0; padding: 4px 12px; color: #475569; background: #f8fafc; }
a { color: #1d4ed8; text-decoration: none; }
hr { border: 0; border-top: 1px solid #cbd5e1; margin: 18px 0; }
img { max-width: 100%; }
"""

for src, dst, title in FILES:
    path = os.path.join(ROOT, src)
    text = open(path, encoding="utf-8").read()
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "toc", "sane_lists"])
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}</style></head><body>{body}</body></html>"""
    out = os.path.join(ROOT, dst)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", dst)
