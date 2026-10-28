#!/usr/bin/env python3
"""Build the index page of fcdegender.nl/hub/review/: one row per Fotobond afdeling (plus Belgium) with its club counts,
linked to the afdeling's review page where one exists, and a link to the all-clubs page. Readers save this one link
instead of each page, so it should be regenerated whenever a page is added or updated.

Usage: python3 index-page.py
Reads every clubsNL<afdeling>.level1.json and clubsBE.level1.json from the iOS repo's working tree, which should match
what is live on GitHub main. Which afdelingen have a page, and where it is on the Desktop, comes from AFDELINGEN in
review-page.py, so a new afdeling needs adding there only. Writes one self-contained HTML file to the Desktop, under the
same name as online (fcdegender.nl/hub/review/index.html). The texts on the page are Dutch, because the readers are Dutch.
"""

import ast
import datetime
import html
import json
import sys
from pathlib import Path

if len(sys.argv) != 1:
    sys.exit("Usage: python3 index-page.py (no arguments)")

HERE = Path(__file__).resolve().parent
SOURCE_DIR = Path.home() / "Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON"
OUTPUT = Path.home() / "Desktop/review/index.html"

# Names as the Fotobond writes them. There is no afdeling 13.
NAMES = {
    "01": "Groningen", "02": "Friesland", "03": "Drenthe-Vechtdal", "04": "Transijssel", "05": "Twente",
    "06": "Gelderland Zuid", "07": "Utrecht-'t Gooi", "08": "Noord-Holland Noord", "09": "Kennemerland",
    "10": "Amsterdam", "11": "Zuid-Holland Noord", "12": "Zuid-Holland Zuid", "14": "Zeeland", "15": "Brabant West",
    "16": "Brabant Oost", "17": "Limburg",
}

# The afdelingen with a review page: read from review-page.py rather than repeated here.
tree = ast.parse((HERE / "review-page.py").read_text(encoding="utf-8"))
pages = next(ast.literal_eval(node.value) for node in tree.body
             if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "AFDELINGEN")


def counts(path):
    # The afdeling's personal members (nickName Persoonlijk<NN>) count as one pseudo-club, as in the apps.
    clubs = json.loads(path.read_text(encoding="utf-8")).get("clubs", [])
    return sum(1 for c in clubs if c.get("optional", {}).get("nlSpecific", {}).get("fotobondNumber")), len(clubs)


e = html.escape
rows, total_fb, total = [], 0, 0
for number, name in NAMES.items():
    fb, n = counts(SOURCE_DIR / f"clubsNL{number}.level1.json")
    total_fb, total = total_fb + fb, total + n
    if number in pages:
        page = Path.home() / f"Desktop/{pages[number][1]}/afdeling{number}.html"
        updated = datetime.date.fromtimestamp(page.stat().st_mtime).strftime("%d-%m-%Y") if page.exists() else ""
        cell = f'<a href="afd{number}/afdeling{number}.html">{e(name)}</a>'
    else:
        updated, cell = "", f'{e(name)} <span class="muted">(nog geen kaart)</span>'
    rows.append(f'<tr><td class="num">{number}</td><td>{cell}</td><td class="num">{fb}</td>'
                f'<td class="num">{n}</td><td class="num">{updated}</td></tr>')
_, n_be = counts(SOURCE_DIR / "clubsBE.level1.json")
total += n_be
# Belgian clubs can't be Fotobond clubs: nvt (niet van toepassing) shows the empty count is intended.
rows.append(f'<tr><td class="num">BE</td><td>België <span class="muted">(geen afdeling)</span></td>'
            f'<td class="num"><span class="muted">nvt</span></td><td class="num">{n_be}</td><td></td></tr>')

clubs_page = OUTPUT.parent / "clubs.html"
clubs_updated = (datetime.date.fromtimestamp(clubs_page.stat().st_mtime).strftime("%d-%m-%Y")
                 if clubs_page.exists() else "")
today = datetime.date.today().strftime("%d-%m-%Y")

page = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fotoclubs per afdeling</title>
<style>
  :root {{ --text: #222; --muted: #555; --line: #ccc; --bg: #fff; }}
  body {{ margin: 0 auto; max-width: 900px; padding: 16px; background: var(--bg); color: var(--text);
         font: 17px/1.45 -apple-system, "Helvetica Neue", Arial, sans-serif; }}
  h1 {{ font-size: 26px; margin: 8px 0; }}
  h2 {{ font-size: 21px; margin: 28px 0 8px; }}
  p {{ max-width: 46em; }}
  .scroll {{ overflow-x: auto; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ text-align: left; vertical-align: top; padding: 7px 8px; border-bottom: 1px solid var(--line); }}
  th {{ font-weight: 600; }}
  td.num, th.num {{ font-variant-numeric: tabular-nums; }}
  tr.total td {{ font-weight: 600; border-bottom: none; }}
  .muted, p.help {{ color: var(--muted); }}
  p.help {{ font-size: 15px; }}
  a {{ color: #0057A0; }}
</style>
</head>
<body>
<h1>Fotoclubs in Photo Club Hub</h1>
<p>Overzicht van de fotoclubs die in de app Photo Club Hub staan, per afdeling van de Fotobond. Per afdeling is er een
kaart met de clubs en een tabel met hun gegevens. Bewaar deze pagina: de kaarten worden af en toe bijgewerkt, en nieuwe
afdelingen komen hier vanzelf bij.</p>
<p><a href="clubs.html">Alle {total} clubs in één lijst, met wat elke club bijzonder maakt</a>
<span class="muted">(bijgewerkt {clubs_updated})</span>. Handig voor een clubbestuur dat ideeën zoekt.</p>

<h2>Per afdeling</h2>
<div class="scroll"><table>
<thead><tr><th>Nr.</th><th>Afdeling</th><th class="num">Fotobond-clubs</th><th class="num">Clubs totaal</th>
<th>Kaart bijgewerkt</th></tr></thead>
<tbody>
{''.join(rows)}
<tr class="total"><td></td><td>Totaal</td><td class="num">{total_fb}</td><td class="num">{total}</td><td></td></tr>
</tbody>
</table></div>
<p class="help">"Fotobond-clubs" zijn clubs met een Fotobond-nummer; de andere clubs zijn niet aangesloten bij de
Fotobond. De persoonlijke leden van een afdeling staan erbij als één groep, net als in de app. Stand van {today}.</p>
</body>
</html>
"""

OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(page, encoding="utf-8")
print(f"{total} clubs ({total_fb} Fotobond), pages for {', '.join(sorted(pages))}, written to {OUTPUT}")
