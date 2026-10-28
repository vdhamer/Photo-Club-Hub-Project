#!/usr/bin/env python3
"""Build one page listing the clubs of all Fotobond afdelingen with their Dutch remark, to show clubs what other clubs
do: the remarks name activity formats (photo chains, joint exhibitions, working groups) a club board can borrow.

Usage: python3 remarks-page.py
Reads every clubsNL<afdeling>.level1.json from the iOS repo's working tree, which should match what is live on GitHub
main. Writes one self-contained HTML file to the Desktop, under the same name as online
(fcdegender.nl/hub/review/clubs.html). The texts on the page are Dutch, because the readers are Dutch.
Companion of review-page.py, which makes the per-afdeling map for an afdeling's contact.
"""

import html
import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 1:
    sys.exit("Usage: python3 remarks-page.py (no arguments)")

SOURCE_DIR = Path.home() / "Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON"
OUTPUT = Path.home() / "Desktop/review/clubs.html"


# Topics a club board might look for, each found by a pattern in the lower-cased Dutch remark. A remark can have
# several topics; one that matches none gets OTHER. Plain keyword rules rather than a model, so the result is the same
# on every run and easy to adjust: when a remark lands in the wrong topic, change the pattern here.
TOPICS = {
    "Fotoketting": r"ketting|estafette|rode draad",
    "Rondgaand voorwerp": r"\bmand\b|koffer|\bdoos\b|voorwerpen|doorgeefobject",
    "Opdrachten en thema's": r"opdracht|thema|uitdaging|onderwerp",
    "Series en projecten": r"\bserie|reeks|drieluik|portfolio|project",
    "Expositie": r"exposeert|exposeren|expositie|\bexpo\b|tentoonstel|salon|galerie|fotowand|wissellijsten|\btoont\b",
    "Wedstrijd en jury": r"wedstrijd|competitie|prijs|trofee|van het jaar|van de maand|jury|beoordeel",
    "Bespreking": r"bespreking|bespreken|besproken|feedback|klankbord|manders|onbewerkt",
    "Werkgroepen": r"werkgroep|groepjes|koppels",
    "Samen op pad": r"excursie|fototocht|uitstap|uitje|fotoreis|reis\b|fotopad|fotowandeling|weekend|op pad|hemelvaart",
    "Leren": r"lezing|gastfotograaf|gastspreker|cursus|workshop|professionele fotograaf|beroepsfotogra|mentor|zeepkist",
    "Samenwerking": r"andere clubs|andere fotoclubs|samen met|samenwerk|uitwissel|bezoeken aan|saforo|\bwisselt\b",
    "Fotograferen voor anderen": r"maatschappelijk|bedrijven|kunstenaars|non-profit|goede doel|voor de gemeente|zwerfafval",
    "Geschiedenis en naam": (r"opgericht|begon|ontstaan|ontstond|\bnaam\b|genoemd|heet naar|vernoemd|sinds 19|sinds 20"
                             r"|bestaat sinds|bestaat in|jarig|ook bekend als|staat voor|is oorspronkelijk|voorheen"),
    "Karakter van de club": (r"\bklein\b|kleinschalig|huiskamerclub|bestaat uit|senioren|ouder|personeel|medewerkers"
                             r"|gepensioneerd|verbonden aan|niveau|plezier|beginnende|beginneling|eigenzinnig|overdag"
                             r"|zo min mogelijk te bewerken|deel van uitmaakt|\d+ leden|vijf leden|7-mans|zes leden"
                             r"|contributie|groei & bloei|omstreken|grote fotoclub"),
    "Natuur": r"natuur(?!theater)",
    "Film en AV": r"\bfilm|audiovisu",
    "Boeken en clubblad": r"boek|clubblad|magazine|issuu|publiceert|artotheek|bibliotheek",
    "Studio en techniek": r"studio|verlichting|lichtbron|camera obscura|techniek",
    "Praktisch": r"website|domeinnaam|verwarren|andere club dan|komt bijeen|thuisbasis|corona|tijdelijk",
}
OTHER = "Overig"


def topics(remark):
    found = [t for t, pattern in TOPICS.items() if re.search(pattern, remark.lower())]
    return found or ([OTHER] if remark else [])


def remark_nl(club):
    for r in club.get("optional", {}).get("remark", []):
        if r["language"] == "NL":
            return r["value"]
    return ""


rows = []
# Belgian clubs have no Fotobond afdeling, so their Afdeling column says BE.
# The afdeling's personal members (nickName Persoonlijk<NN>) are listed as one pseudo-club, as in the apps.
for path in sorted(SOURCE_DIR.glob("clubsNL[0-9][0-9].level1.json")) + [SOURCE_DIR / "clubsBE.level1.json"]:
    afdeling = re.search(r"clubs(?:NL(\d\d)|(BE))", path.name).group(1) or "BE"
    for club in json.loads(path.read_text(encoding="utf-8")).get("clubs", []):
        i, o = club["idPlus"], club.get("optional", {})
        rows.append({"name": i["fullName"], "town": i["town"], "afdeling": afdeling, "site": o.get("website", ""),
                     "number": o.get("nlSpecific", {}).get("fotobondNumber"), "remark": remark_nl(club)})
        rows[-1]["topics"] = topics(rows[-1]["remark"])
rows.sort(key=lambda r: (r["town"].casefold(), r["name"].casefold()))
members = sum(1 for r in rows if r["number"])
afdelingen = sorted({r["afdeling"] for r in rows} - {"BE"})
belgian = sum(1 for r in rows if r["afdeling"] == "BE")
topic_counts = {t: sum(1 for r in rows if t in r["topics"]) for t in [*TOPICS, OTHER]}

e = html.escape

table_rows = []
for r in rows:
    name = (f'<a href="{e(r["site"])}" target="_blank" rel="noopener">{e(r["name"])}</a>' if r["site"]
            else e(r["name"]))
    # Without a website there was nothing to write a description from, which is the more useful thing to say.
    remark = e(r["remark"]) if r["remark"] else "<i>Geen beschrijving.</i>" if r["site"] else "<i>Geen website.</i>"
    table_rows.append(f"""<tr>
<td class="name">{name}</td>
<td>{e(r['town'])}</td>
<td class="num">{r['afdeling']}</td>
<td class="num">{f"{r['number']:04d}" if r['number'] else ""}</td>
<td>{remark}</td>
<td class="topics">{"".join(f'<span class="tag">{e(t)}</span>' for t in r["topics"])}</td>
</tr>""")
# One button per topic that has clubs, in the order of TOPICS; clicking one again clears it.
buttons = "".join(f'<button type="button" class="topic" data-topic="{e(t)}">{e(t)} <span>{n}</span></button>'
                  for t, n in topic_counts.items() if n)

page = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fotoclubs en hun activiteiten</title>
<style>
  :root {{ --text: #222; --muted: #555; --line: #ccc; --bg: #fff; }}
  body {{ margin: 0 auto; max-width: 1200px; padding: 16px; background: var(--bg); color: var(--text);
         font: 17px/1.45 -apple-system, "Helvetica Neue", Arial, sans-serif; }}
  h1 {{ font-size: 26px; margin: 8px 0; }}
  p {{ max-width: 46em; }}
  #filter {{ font: inherit; padding: 6px 10px; width: min(100%, 26em); box-sizing: border-box;
            border: 1px solid var(--line); border-radius: 6px; }}
  #count {{ color: var(--muted); margin-left: 10px; }}
  .scroll {{ overflow-x: auto; margin-top: 12px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ text-align: left; vertical-align: top; padding: 7px 8px; border-bottom: 1px solid var(--line); }}
  th {{ font-weight: 600; }}
  td.name {{ font-weight: 600; }}
  td.num {{ font-variant-numeric: tabular-nums; }}
  a {{ color: #0057A0; }}
  p.help {{ color: var(--muted); font-size: 15px; }}
  #topics {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0 8px; }}
  button.topic {{ font: inherit; font-size: 15px; padding: 3px 10px; border: 1px solid var(--line); border-radius: 14px;
                 background: var(--bg); color: var(--text); cursor: pointer; }}
  button.topic span {{ color: var(--muted); }}
  button.topic[aria-pressed="true"] {{ background: #0057A0; border-color: #0057A0; color: #fff; }}
  button.topic[aria-pressed="true"] span {{ color: #fff; }}
  td.topics {{ font-size: 14px; }}
  .tag {{ display: inline-block; margin: 0 4px 4px 0; padding: 1px 7px; border-radius: 10px; background: #eef2f6;
          white-space: nowrap; }}
</style>
</head>
<body>
<p class="help"><a href="index.html">&larr; Overzicht per afdeling</a></p>
<h1>Fotoclubs en hun activiteiten</h1>
<p>De {len(rows)} clubs zoals ze nu in Photo Club Hub staan, uit de afdelingen {", ".join(afdelingen)}{f" en {belgian} uit België (afdeling BE)" if belgian else ""}, waarvan
{members} lid van de Fotobond. Bij veel clubs staat een korte beschrijving van iets wat de club anders doet: een
fotoketting, een gezamenlijke expositie, werkgroepen. Zo kan een clubbestuur zien wat elders werkt.</p>
<p><input id="filter" type="search" placeholder="Zoek, bijvoorbeeld fotoketting of expositie" autofocus>
<span id="count"></span></p>
<p class="help">Of kies een onderwerp. De onderwerpen zijn automatisch toegekend op grond van de beschrijving, dus
soms wat grof.</p>
<div id="topics">{buttons}</div>
<p class="help">Gesorteerd op plaats. De naam van een club is een link naar haar website.</p>
<div class="scroll"><table>
<thead><tr><th>Club</th><th>Plaats</th><th>Afdeling</th><th>Fotobond-nr.</th><th>Beschrijving</th><th>Onderwerpen</th></tr></thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table></div>

<script>
// Matches every word typed, in any column, ignoring case and accents (so "expositie" also finds "Expositie", and
// "een" finds "één").
const fold = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
const rows = [...document.querySelectorAll('tbody tr')];
const texts = rows.map(r => fold(r.textContent));
const count = document.getElementById('count');
const tags = rows.map(r => [...r.querySelectorAll('.tag')].map(t => t.textContent));
let topic = null;  // the selected topic, if any; it combines with the typed words
function update() {{
  const words = fold(document.getElementById('filter').value).split(/\\s+/).filter(Boolean);
  let shown = 0;
  rows.forEach((r, k) => {{
    const hit = words.every(w => texts[k].includes(w)) && (!topic || tags[k].includes(topic));
    r.hidden = !hit;
    shown += hit;
  }});
  count.textContent = words.length || topic ? shown + ' van ' + rows.length + ' clubs' : '';
}}
document.getElementById('filter').addEventListener('input', update);
document.querySelectorAll('button.topic').forEach(b => b.addEventListener('click', () => {{
  topic = topic === b.dataset.topic ? null : b.dataset.topic;
  document.querySelectorAll('button.topic').forEach(x => x.setAttribute('aria-pressed', x.dataset.topic === topic));
  update();
}}));
</script>
</body>
</html>
"""

OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(page, encoding="utf-8")
print(f"{len(rows)} clubs ({members} Fotobond) from afdelingen {', '.join(afdelingen)} written to {OUTPUT}")
