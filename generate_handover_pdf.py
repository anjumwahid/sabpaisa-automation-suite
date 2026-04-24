"""
Convert HANDOVER_GUIDE.md into a printable PDF.

Uses:
  - `markdown` library (Python package) to convert md → HTML
  - Playwright (already installed) to render HTML and save as PDF

Run:
    python generate_handover_pdf.py

Output: HANDOVER_GUIDE.pdf (in project root)
"""

import os
import sys

try:
    import markdown
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "markdown"], check=True)
    import markdown

from playwright.sync_api import sync_playwright


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH  = os.path.join(PROJECT_DIR, "HANDOVER_GUIDE.md")
PDF_PATH = os.path.join(PROJECT_DIR, "HANDOVER_GUIDE.pdf")

# Basic print-friendly CSS (A4 pages, readable font, table borders, etc.)
CSS = """
@page { size: A4; margin: 20mm 18mm; }
body {
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 11pt; line-height: 1.5; color: #1a1a1a;
    max-width: 100%; margin: 0; padding: 0;
}
h1 { font-size: 22pt; color: #1565C0; border-bottom: 3px solid #1565C0; padding-bottom: 6px; margin-top: 0; page-break-before: auto; }
h2 { font-size: 16pt; color: #1565C0; border-bottom: 1px solid #d4d4d4; padding-bottom: 4px; margin-top: 26px; page-break-after: avoid; }
h3 { font-size: 13pt; color: #333; margin-top: 20px; page-break-after: avoid; }
h4 { font-size: 12pt; color: #444; }
p, ul, ol { margin: 0.6em 0; }
code {
    background: #f4f4f4; padding: 2px 6px; border-radius: 3px;
    font-family: Consolas, "Courier New", monospace; font-size: 10pt;
    color: #c7254e;
}
pre {
    background: #f8f8f8; border: 1px solid #e1e1e1; border-radius: 4px;
    padding: 10px 14px; overflow-x: auto; page-break-inside: avoid;
}
pre code { background: transparent; color: #2d2d2d; padding: 0; }
table {
    border-collapse: collapse; width: 100%; margin: 12px 0;
    page-break-inside: avoid;
}
th, td { border: 1px solid #cbd5e1; padding: 6px 10px; text-align: left; vertical-align: top; }
th { background: #eef4fc; font-weight: 600; color: #1565C0; }
tr:nth-child(even) td { background: #fafbfc; }
a { color: #1565C0; text-decoration: none; }
hr { border: 0; border-top: 1px solid #d4d4d4; margin: 20px 0; }
blockquote { border-left: 3px solid #1565C0; padding-left: 12px; color: #555; margin: 12px 0; }
li { margin: 3px 0; }
ul ul, ol ol, ul ol, ol ul { margin: 3px 0 3px 18px; }

/* Callout emoji for colored PASS/FAIL */
.emoji { font-size: 110%; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SabPaisa Automation — Handover Guide</title>
    <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def main():
    if not os.path.exists(MD_PATH):
        print(f"ERROR: {MD_PATH} not found")
        sys.exit(1)

    print(f"Reading {MD_PATH} ...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    print("Converting markdown to HTML ...")
    html_body = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "toc", "nl2br", "sane_lists"],
    )
    full_html = HTML_TEMPLATE.format(css=CSS, body=html_body)

    # Save intermediate HTML for debugging (optional — can delete if unused)
    html_tmp = os.path.join(PROJECT_DIR, "_handover_tmp.html")
    with open(html_tmp, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("Launching headless browser to render PDF ...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(full_html, wait_until="domcontentloaded")
        page.pdf(
            path=PDF_PATH,
            format="A4",
            margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"},
            print_background=True,
        )
        browser.close()

    # Clean tmp HTML
    try:
        os.remove(html_tmp)
    except Exception:
        pass

    size_kb = os.path.getsize(PDF_PATH) / 1024
    print(f"\nDONE.  {PDF_PATH}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
