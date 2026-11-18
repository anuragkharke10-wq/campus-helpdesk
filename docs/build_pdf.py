"""Build docs/Assignment8_Report.pdf from REPORT.md, PROMPT_LOG.md and SOURCES.md.

Usage (from the repo root):
    uv run --with markdown python docs/build_pdf.py
Needs Google Chrome installed; it is used in headless mode to print the HTML to PDF.
"""
import subprocess
from pathlib import Path

import markdown

DOCS = Path(__file__).resolve().parent
PARTS = ["REPORT.md", "PROMPT_LOG.md", "SOURCES.md"]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 10pt; line-height: 1.45; color: #111; }
h1 { font-size: 18pt; margin: 0 0 6pt; } h2 { font-size: 14pt; border-bottom: 1px solid #999; padding-bottom: 2pt; margin-top: 18pt; }
h3 { font-size: 11.5pt; margin-top: 12pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 8.6pt; page-break-inside: auto; }
th, td { border: 1px solid #bbb; padding: 3pt 4pt; vertical-align: top; text-align: left; word-break: normal; overflow-wrap: break-word; }
th { background: #eee; } tr { page-break-inside: avoid; }
code { font-family: Menlo, Consolas, monospace; font-size: 8.4pt; background: #f3f3f3; padding: 0 2pt; }
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 6pt; white-space: pre-wrap; word-break: break-all; font-size: 8pt; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3px solid #c80; margin: 6pt 0; padding: 2pt 8pt; background: #fff8ec; }
img { max-width: 100%; border: 1px solid #ccc; margin: 6pt 0; }
.part-break { page-break-before: always; }
"""


def main() -> None:
    html_parts = []
    for i, name in enumerate(PARTS):
        body = markdown.markdown((DOCS / name).read_text(encoding="utf-8"), extensions=["tables", "fenced_code"])
        html_parts.append(f'<section class="{"part-break" if i else ""}">{body}</section>')
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>Assignment 8 Report</title><style>{CSS}</style></head><body>{''.join(html_parts)}</body></html>"
    out_html = DOCS / "Assignment8_Report.html"
    out_pdf = DOCS / "Assignment8_Report.pdf"
    out_html.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", out_html.as_uri()], check=True, capture_output=True)
    print(f"wrote {out_pdf}")


if __name__ == "__main__":
    main()
