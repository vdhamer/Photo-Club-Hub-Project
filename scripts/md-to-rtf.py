#!/usr/bin/env python3
"""Convert a mail to an afdeling contact from Markdown to RTF, for pasting into an e-mail.

Usage: python3 md-to-rtf.py "<mail>.md"
Writes "<mail>.rtf" next to it. Handles only what the mail uses: an "Onderwerp:" line (left out of the body
and printed instead), paragraphs, "##" headings, numbered questions with indented lines and "-" sub-bullets,
"-" bullet lists, **bold** and [text](url) links. Open the RTF in TextEdit, select all, copy, paste into Mail.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit('Usage: python3 md-to-rtf.py "<mail>.md"')

src = Path(sys.argv[1])
lines = src.read_text(encoding="utf-8").split("\n")


def inline(text):
    text = html.escape(text.strip(), quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)


out, para = [], []
in_ol = in_ul = in_sub = in_li = False


def flush_para():
    global para
    if para:
        out.append("<p>" + "<br>".join(inline(p) for p in para) + "</p>")
        para = []


def close_sub():
    global in_sub
    if in_sub:
        out.append("</ul>")
        in_sub = False


def close_li():
    global in_li
    close_sub()
    if in_li:
        out.append("</li>")
        in_li = False


def close_lists():
    global in_ol, in_ul
    close_li()
    if in_ol:
        out.append("</ol>")
        in_ol = False
    if in_ul:
        out.append("</ul>")
        in_ul = False


subject = ""
for line in lines:
    if line.startswith("Onderwerp:"):
        subject = line.removeprefix("Onderwerp:").strip()
        continue
    if not line.strip():
        flush_para()
        continue
    numbered = re.match(r"^(\d+)\. (.*)", line)
    sub = re.match(r"^\s+- (.*)", line)
    bullet = re.match(r"^- (.*)", line)
    if line.startswith("## "):
        flush_para()
        close_lists()
        out.append(f"<h3>{inline(line[3:])}</h3>")
    elif numbered:
        flush_para()
        if in_ul:
            close_lists()
        close_li()
        if not in_ol:
            out.append("<ol>")
            in_ol = True
        out.append(f'<li value="{numbered.group(1)}">{inline(numbered.group(2))}')
        in_li = True
    elif sub and in_li:
        if not in_sub:
            out.append("<ul>")
            in_sub = True
        out.append(f"<li>{inline(sub.group(1))}</li>")
    elif line.startswith(" ") and in_li:
        close_sub()
        out.append(f"<br>{inline(line)}")
    elif bullet:
        flush_para()
        if in_ol:
            close_lists()
        if not in_ul:
            out.append("<ul>")
            in_ul = True
        out.append(f"<li>{inline(bullet.group(1))}</li>")
    else:
        if in_ol or in_ul:
            close_lists()
        para.append(line)
flush_para()
close_lists()

page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ font-family: Helvetica, Arial, sans-serif; font-size: 13pt; color: #222; }}
h3 {{ font-size: 14pt; margin: 14pt 0 6pt; }}
li {{ margin-bottom: 8pt; }}
ul ul li, ol ul li {{ margin-bottom: 3pt; }}
</style></head><body>
{chr(10).join(out)}
</body></html>"""

html_path = src.with_suffix(".html.tmp")
rtf_path = src.with_suffix(".rtf")
html_path.write_text(page, encoding="utf-8")
subprocess.run(["textutil", "-convert", "rtf", "-inputencoding", "UTF-8", str(html_path), "-output", str(rtf_path)],
               check=True)
html_path.unlink()
print(f"Written: {rtf_path}")
print(f"Onderwerp: {subject}")
