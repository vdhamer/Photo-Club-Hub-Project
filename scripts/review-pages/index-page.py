#!/usr/bin/env python3
# Created by Claude Code (guided by Peter van den Hamer) on 27/10/2026.

"""Build the index page of fcdegender.nl/hub/review/: one row per Fotobond afdeling (plus Belgium)
with its club counts, linked to its review page, and a link to the all-clubs page.
Readers save this one link instead of each page, so it should be regenerated whenever a page is added or updated.

Usage: python3 index-page.py

Reads every clubsNL<afdeling>.level1.json and clubsBE.level1.json from the iOS repo's working tree, which should match
what is live on GitHub main. The afdelingen, their names and the Belgian page's name come from AFDELINGEN and BELGIUM
in review-page.py, so they are written down in one place.
Writes one self-contained HTML file into ~/Desktop/review, which mirrors fcdegender.nl/hub/review, as index.html.
The texts on the page are Dutch, because the readers are Dutch.
"""

import ast # abstract syntax trees
import datetime
import html
import json
import sys
from pathlib import Path

from former import former_entry

if len(sys.argv) != 1:
    sys.exit("Usage: python3 index-page.py (no arguments)")

HERE = Path(__file__).resolve().parent
SOURCE_DIR = Path.home() / "Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON"
SITE = Path.home() / "Desktop/review"  # mirrors fcdegender.nl/hub/review, so it can be uploaded as one tree
OUTPUT = SITE / "index.html"

# Read from review-page.py rather than repeated here.
tree = ast.parse((HERE / "review-page.py").read_text(encoding="utf-8"))


def constant(name):
    return next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == name)


AFDELINGEN, BELGIUM = constant("AFDELINGEN"), constant("BELGIUM")


def counts(path):
    # The afdeling's personal members (nickName Persoonlijk<NN>) count as one pseudo-club, as in the apps.
    # Clubs that may have stopped don't count: the page describes the clubs shown in the apps, which hide them.
    clubs = [c for c in json.loads(path.read_text(encoding="utf-8")).get("clubs", []) if former_entry(c) is None]
    return sum(1 for c in clubs if c.get("optional", {}).get("nlSpecific", {}).get("fotobondNumber")), len(clubs)


e = html.escape


def updated(page):
    return datetime.date.fromtimestamp(page.stat().st_mtime).strftime("%d-%m-%Y") if page.exists() else ""


def share(fb, n):
    """A Fotobond count with its share of the clubs, e.g. 6 (38%), to show the ratio at a glance."""
    return f"{fb} ({round(100 * fb / n)}%)" if n else f"{fb}"


# The afdelingen that had a full search and a review round with their contact. Fotobond clubs come from the roster, so
# they are complete everywhere; other clubs are only as complete as the search was, so these afdelingen have more.
# Add an afdeling here when its round is done.
REVIEWED = ["03", "06", "15", "16"]

# Same colors as the map pins on the afdeling pages (Okabe-Ito, safe for color blindness).
FOTOBOND_COLOR, OTHER_COLOR = "#009E73", "#E69F00"


def chart(bars):
    """An inline SVG with one stacked bar per afdeling: Fotobond clubs at the bottom, the other clubs on top, so the
    bar's height is the afdeling's total and the green part shows the Fotobond share. Hovering a bar shows its
    numbers; the table below the chart holds them all."""
    width, height, left, top, bottom = 800, 250, 34, 10, 26
    plot_w, plot_h = width - left, height - top - bottom
    step = 20
    y_max = -(-max(n for _, _, _, n in bars) // step) * step  # rounded up to a gridline
    y = lambda count: top + plot_h * (1 - count / y_max)
    slot = plot_w / len(bars)
    bar_w = slot * 0.6
    gap, radius = 2, 4  # a 2px gap between the two parts; rounded top on the topmost part

    def part(x, y_bottom, y_top, color, rounded):
        if y_bottom - y_top <= 0:
            return ""
        r = min(radius, y_bottom - y_top) if rounded else 0
        return (f'<path fill="{color}" d="M{x:.1f},{y_bottom:.1f} V{y_top + r:.1f} Q{x:.1f},{y_top:.1f} '
                f'{x + r:.1f},{y_top:.1f} H{x + bar_w - r:.1f} Q{x + bar_w:.1f},{y_top:.1f} {x + bar_w:.1f},'
                f'{y_top + r:.1f} V{y_bottom:.1f} Z"/>')

    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Clubs per afdeling, met het deel dat lid is '
           f'van de Fotobond; de getallen staan ook in de tabel"'
           ' style="width: 100%; height: auto; margin: 4px 0 16px;">']
    for count in range(0, y_max + 1, step):
        out.append(f'<line x1="{left}" x2="{width}" y1="{y(count):.1f}" y2="{y(count):.1f}" stroke="#e3e3e3"/>'
                   f'<text x="{left - 6}" y="{y(count) + 4:.1f}" text-anchor="end">{count}</text>')
    for k, (number, name, fb, n) in enumerate(bars):
        x = left + k * slot + (slot - bar_w) / 2
        base, green_top = y(0), y(fb)
        tip = f"{number} {name}: {n} clubs, waarvan {share(fb, n)} bij de Fotobond"
        out.append(f'<g><title>{e(tip)}</title>'
                   # the whole column is the hover target, so a short bar is as easy to hover as a tall one
                   f'<rect x="{left + k * slot:.1f}" y="{top}" width="{slot:.1f}" height="{plot_h}"'
                   f' fill="transparent"/>'
                   + part(x, base, green_top, FOTOBOND_COLOR, fb == n)
                   + part(x, green_top - (gap if fb else 0), y(n), OTHER_COLOR, True)
                   + f'<text x="{x + bar_w / 2:.1f}" y="{height - 8}" text-anchor="middle">{number}</text></g>')
    out.append("</svg>")
    return "".join(out)


rows, bars, total_fb, total = [], [], 0, 0
for number, name in AFDELINGEN.items():
    fb, n = counts(SOURCE_DIR / f"clubsNL{number}.level1.json")
    total_fb, total = total_fb + fb, total + n
    bars.append((number, name, fb, n))
    page = SITE / f"afd{number}/afdeling{number}.html"
    link = f"afd{number}/afdeling{number}.html"  # both the name and the total link to the page
    rows.append(f'<tr><td class="num">{number}</td><td><a href="{link}">{e(name)}</a></td>'
                f'<td class="num">{share(fb, n)}</td><td class="num"><a href="{link}">{n}</a></td>'
                f'<td class="num">{updated(page)}</td></tr>')
total_nl = total  # Belgian clubs can't be Fotobond clubs, so the total's share is of the Dutch clubs only
_, n_be = counts(SOURCE_DIR / "clubsBE.level1.json")
total += n_be
be_page = SITE / f"{BELGIUM}/{BELGIUM}.html"
# Belgian clubs can't be Fotobond clubs: nvt (niet van toepassing) shows the empty count is intended.
rows.append(f'<tr><td class="num">BE</td><td><a href="{BELGIUM}/{BELGIUM}.html">België</a> '
            f'<span class="muted">(geen afdeling)</span></td><td class="num"><span class="muted">nvt</span></td>'
            f'<td class="num"><a href="{BELGIUM}/{BELGIUM}.html">{n_be}</a></td>'
            f'<td class="num">{updated(be_page)}</td></tr>')

clubs_updated = updated(OUTPUT.parent / "clubs.html")
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
  .muted, .help {{ color: var(--muted); }}
  .help {{ font-size: 15px; }}
  ul.help {{ padding-left: 1.2em; max-width: 46em; }}
  ul.help li {{ margin-bottom: 4px; }}
  a {{ color: #0057A0; }}
  svg text {{ font-size: 13px; fill: var(--muted); font-variant-numeric: tabular-nums; }}
  .legend {{ display: inline-block; margin: 0 18px 0 0; font-size: 15px; }}
  .dot {{ display: inline-block; width: 13px; height: 13px; border-radius: 3px; margin-right: 6px;
          vertical-align: -1px; }}
</style>
</head>
<body>
<h1>Fotoclubs in Photo Club Hub</h1>
<p>Overzicht van de fotoclubs die in de apps van Photo Club Hub staan, per afdeling van de Fotobond, en de Belgische
clubs. Per afdeling is er een kaart met de clubs en een tabel met hun gegevens. Bewaar deze pagina: de kaarten worden af
en toe bijgewerkt.</p>
<p><a href="clubs.html">Alle {total} clubs in één lijst, met wat elke club bijzonder maakt</a>
<span class="muted">(bijgewerkt {clubs_updated})</span>. Handig voor een clubbestuur dat ideeën zoekt.</p>

<h2>Per afdeling</h2>
<div><span class="legend"><span class="dot" style="background: {FOTOBOND_COLOR}"></span>Fotobond-clubs</span><span
class="legend"><span class="dot" style="background: {OTHER_COLOR}"></span>Andere clubs</span></div>
{chart(bars)}
<div class="scroll"><table>
<thead><tr><th>Nr.</th><th>Afdeling</th><th class="num">Fotobond-clubs</th><th class="num">Clubs totaal</th>
<th>Kaart bijgewerkt</th></tr></thead>
<tbody>
{''.join(rows)}
<tr class="total"><td></td><td>Totaal</td><td class="num">{share(total_fb, total_nl)}</td><td class="num">{total}</td><td></td></tr>
</tbody>
</table></div>
<ul class="help">
<li>"Fotobond-clubs" zijn clubs met een Fotobond-nummer; de andere clubs zijn niet aangesloten bij de Fotobond.</li>
<li>Het percentage is het deel Fotobond-clubs van de clubs in die afdeling. Bij het totaal is het hun deel van de
Nederlandse clubs, omdat Belgische clubs geen lid kunnen zijn.</li>
<li>De oranje delen zijn zo volledig als ons zoeken tot nu toe; afdelingen die al een controleronde hadden
({", ".join(REVIEWED[:-1])} en {REVIEWED[-1]}) zijn vollediger. Daardoor kan het werkelijke deel Fotobond-clubs lager
zijn dan het percentage.</li>
<li>De persoonlijke leden van een afdeling staan erbij als één groep, net als in de apps.</li>
</ul>
<p class="help">Stand van {today}.</p>
</body>
</html>
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(page, encoding="utf-8")
print(f"{total} clubs ({total_fb} Fotobond), pages for {', '.join(AFDELINGEN)} and BE, written to {OUTPUT}")
