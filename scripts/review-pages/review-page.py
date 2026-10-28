#!/usr/bin/env python3
"""Build a review page (map + table) of the clubs of one Fotobond afdeling, for the afdeling's contact (Data#68).

Usage: python3 review-page.py <afdeling>      e.g. python3 review-page.py 06
Reads clubsNL<afdeling>.level1.json from the iOS repo's working tree, which should match what is live on GitHub
main, so the page shows what the contact sees in the app. Writes one self-contained HTML file to the afdeling's
folder on the Desktop, under the same name as online (fcdegender.nl/hub/review/afd<afdeling>/afdeling<afdeling>.html).
The texts on the page are Dutch, because the reader is Dutch.

Generalized from review-page-03.py, which also compared a search draft against the file. Here the review comes
after the data went live, so the page shows only the file. To add an afdeling: a line in AFDELINGEN, and its notes
and doubts below.
"""

import html
import json
import math
import sys
from pathlib import Path

# afdeling: (name as the Fotobond writes it, folder on the Desktop for the working files)
AFDELINGEN = {
    "03": ("Drenthe-Vechtdal", "Drenthe"),
    "06": ("Gelderland Zuid", "Gelderland"),
    "15": ("Brabant West", "Brabant West"),
    "16": ("Brabant Oost", "Brabant Oost"),
}

if len(sys.argv) != 2 or sys.argv[1] not in AFDELINGEN:
    sys.exit(f"Usage: python3 review-page.py <afdeling>, one of {', '.join(AFDELINGEN)}")

AFDELING = sys.argv[1]
AFDELING_NAME, FOLDER = AFDELINGEN[AFDELING]
SOURCE = Path.home() / f"Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON/clubsNL{AFDELING}.level1.json"
OUTPUT = Path.home() / f"Desktop/{FOLDER}/afdeling{AFDELING}.html"

# Short notes per club, keyed by nickName (unique across all clubsNL files): mostly how its name or town was
# chosen, because fullName and town identify a club and are costly to change later.
NOTES = {
    "03": {
        "fcAfovera": "De website noemt nog bijeenkomsten bij leden thuis; de markering blijft op de Maasstraat.",
        "fcBorgerOdoorn": "De website noemt nog het lidmaatschap van de Fotobond.",
        "afvGoedLicht": "Vaak afgekort tot AFV Goed Licht.",
        "fgMeppel": "Bij de KvK heet de club Fotogroep Meppel.",
        "fcDWolden": "Schrijfwijze \"FotoClub\", zoals de club zelf.",
        "fcSpijkerboor": "Dicht bij de grens met Groningen.",
    },
    "06": {
        "fcCreashot": "Naam zoals in de kop van de website van de club.",
        "fkDuiven": "Fotoklub met een k, zoals de club het zelf schrijft.",
        "fcLingewaard": "Plaats Angeren: daar komt de club bijeen.",
        "nfRivierenland": "Plaats Zetten: daar komt de club bijeen.",
        "fcZelfontspanners": "Plaats Nijmegen, zoals op de website van de club.",
        "fcPositieven": "Een andere club dan De Positieven in Beuningen.",
        "fcPositievenBeuningen": "Een andere club dan De Positieven in Tiel.",
    },
    "15": {
        "AFVP": "AFV voluit geschreven, zoals bij elke club. De website noemt de club Fotoclub AFVP Etten-Leur.",
        "afvOntspanner": "AFV voluit geschreven, zoals bij elke club.",
        "afvKontrast": "AFV voluit geschreven, zoals bij elke club.",
        "TAFV": "Naam voluit, zoals op de website van de club.",
        "faRijen": "Naam zoals op de website van de club; de Fotobond schrijft FA-Rijen.",
        "fgPerspectiefW": "Fotogroep, zoals op de website van de club; de Fotobond schrijft Fotoclub.",
        "fgBelcrum": "Plaats Breda, wijk Belcrum; de Fotobond noemt 's-Hertogenbosch.",
        "fcMoerdijk": "Markering bij de expositieplek in Zevenbergen.",
        "fgTEMA": "Plaats Tilburg, zoals bij de Fotobond; markering bij de expositieplek in Moergestel.",
        "fgHuiskamer": "De website fgdehuiskamer.nl bestaat niet meer.",
        "fgWestBrabant": "De website fgwestbrabant.nl toont alleen een lege pagina.",
        "fc4Zoom": "Geen eigen website gevonden; gegevens uit een aankondiging van Galerie Arsis (2025). Markering bij die expositieplek.",
        "fcGBBreda": "Naam zoals op de pagina van Groei & Bloei Breda.",
        "fcFocusUdenhout": "Komt bij een lid thuis bijeen in Biezenmortel; markering in het midden van Biezenmortel, niet bij het huis.",
    },
    "16": {
        "fgRiethoven": "Fotokring, zoals de club zelf; de Fotobond schrijft Fotogroep.",
        "fgDeGender": "Fotogroep, zoals de club zelf; de Fotobond schrijft Fotoclub.",
        "fgFocus": "Naam zoals de club zelf; de Fotobond schrijft FG Focus.",
        "fcAFC68": "Naam voluit; de Fotobond schrijft AFC68.",
        "fcKiekus": "Plaats Wanroij, de officiële spelling; de Fotobond schrijft Wanroy.",
        "fcBGC": "Plaats Sint Agatha; de Fotobond noemt Oeffelt.",
        "fcRapenland": "Volgens de Fotobond club 1626; dat nummer staat nog niet in de app.",
        "fegGemert": "Heeft Fotobond-nummer 1632 in de app, maar staat niet op de ledenlijst van de Fotobond.",
    },
}

# Clubs whose afdeling is in doubt, keyed by nickName, with the question. They are in the app either way: the
# afdeling only decides which file holds them.
DOUBTS = {}

STATUS = {  # key: (label, color); green and orange from the Okabe-Ito palette, safe for color blindness
    "fotobond": ("Lid van de Fotobond", "#009E73"),
    "other": ("Geen lid van de Fotobond", "#E69F00"),
    "doubt": ("Twijfel: welke afdeling?", "#999999"),
}


def remark_nl(club):
    for r in club.get("optional", {}).get("remark", []):
        if r["language"] == "NL":
            return r["value"]
    return ""


def row(club):
    i, o = club["idPlus"], club.get("optional", {})
    number = o.get("nlSpecific", {}).get("fotobondNumber")
    doubt = DOUBTS.get(AFDELING, {}).get(i["nickName"], "")
    note = " ".join(n for n in (NOTES.get(AFDELING, {}).get(i["nickName"], ""), doubt) if n)
    return {
        "name": i["fullName"], "town": i["town"],
        "lat": club["coordinates"]["latitude"], "lon": club["coordinates"]["longitude"],
        "site": o.get("website", ""), "number": number, "remark": remark_nl(club), "note": note,
        "status": "doubt" if doubt else "fotobond" if number else "other",
    }


# The afdeling's personal members (nickName Persoonlijk<NN>) are listed as one pseudo-club, as in the apps.
clubs = json.loads(SOURCE.read_text(encoding="utf-8"))["clubs"]
rows = sorted((row(c) for c in clubs), key=lambda r: (r["town"].casefold(), r["name"].casefold()))
members = sum(1 for r in rows if r["number"])

# Clubs meeting at the same venue, or both pinned to their town centre, have pins a few meters apart, which look like
# one pin at any zoom. Such a group is drawn as a small ring of pins around its spot, a fixed number of screen pixels
# apart; each pin keeps its true coordinates, so the spread is only on this page, not in the data.
NEAR_M, SPREAD_PX = 50, 11


def meters(a, b):
    dy = (a["lat"] - b["lat"]) * 111_320
    dx = (a["lon"] - b["lon"]) * 111_320 * math.cos(math.radians(a["lat"]))
    return math.hypot(dx, dy)


groups = []
for r in rows:
    group = next((g for g in groups if any(meters(r, other) < NEAR_M for other in g)), None)
    if group is None:
        groups.append([r])
    else:
        group.append(r)
for group in groups:
    for k, r in enumerate(group):
        angle = 2 * math.pi * k / len(group)
        spread = SPREAD_PX if len(group) > 1 else 0
        r["dx"], r["dy"] = round(spread * math.cos(angle)), round(spread * math.sin(angle))

e = html.escape


def site_link(url):
    if not url:
        return "&nbsp;"
    label = url.split("//")[-1].removeprefix("www.").split("/")[0]  # the domain only, so the column stays narrow
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>'


table_rows = []
for r in rows:
    # Without a website there was nothing to write a description from, which is the more useful thing to say.
    remark = e(r["remark"]) if r["remark"] else "<i>Geen beschrijving.</i>" if r["site"] else "<i>Geen website.</i>"
    table_rows.append(f"""<tr>
<td class="name">{e(r['name'])}</td>
<td>{e(r['town'])}</td>
<td>{site_link(r['site'])}</td>
<td class="num">{f"{r['number']:04d}" if r['number'] else ""}</td>
<td>{remark}</td>
<td class="note">{e(r['note'])}</td>
</tr>""")

legend = "".join(f'<span class="legend"><span class="dot" style="background:{c}"></span>{e(l)}</span>'
                 for key, (l, c) in STATUS.items() if key != "doubt" or DOUBTS.get(AFDELING))

page = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fotoclubs afdeling {AFDELING}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root {{ --text: #222; --muted: #555; --line: #ccc; --bg: #fff; }}
  body {{ margin: 0 auto; max-width: 1200px; padding: 16px; background: var(--bg); color: var(--text);
         font: 17px/1.45 -apple-system, "Helvetica Neue", Arial, sans-serif; }}
  h1 {{ font-size: 26px; margin: 8px 0; }}
  h2 {{ font-size: 21px; margin: 32px 0 8px; }}
  p {{ max-width: 46em; }}
  #map {{ height: 520px; border: 1px solid var(--line); border-radius: 6px; margin: 12px 0; }}
  .legend {{ display: inline-block; margin: 0 18px 6px 0; }}
  .dot {{ display: inline-block; width: 13px; height: 13px; border-radius: 50%; margin-right: 6px;
          vertical-align: -1px; border: 1px solid #0006; }}
  .scroll {{ overflow-x: auto; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ text-align: left; vertical-align: top; padding: 7px 8px; border-bottom: 1px solid var(--line); }}
  th {{ font-weight: 600; }}
  td.name {{ font-weight: 600; }}
  td.num {{ font-variant-numeric: tabular-nums; }}
  td.note {{ color: var(--muted); font-size: 15px; }}
  a {{ color: #0057A0; }}
  td a {{ overflow-wrap: anywhere; }}
  .pin {{ border-radius: 50%; border: 1px solid #000; opacity: 0.9; box-sizing: border-box; }}
  .pin div {{ width: 100%; height: 100%; border-radius: 50%; }}
  .leaflet-popup-content {{ font-size: 15px; }}
  p.help {{ color: var(--muted); font-size: 15px; margin-top: 0; }}
</style>
</head>
<body>
<p class="help"><a href="../index.html">&larr; Overzicht per afdeling</a> &nbsp;·&nbsp; <a href="../clubs.html">Alle clubs, met onderwerpen</a></p>
<h1>Fotoclubs in afdeling {AFDELING}, {e(AFDELING_NAME)}</h1>
<p>De {len(rows)} clubs zoals ze nu in Photo Club Hub staan, waarvan {members} lid van de Fotobond. Ga met de muis over een markering (of tik erop) voor de naam en de korte beschrijving van de club. Een klik op een markering laat ook de website zien.</p>
<div>{legend}</div>
<div id="map"></div>
<p class="help"><b>De kaart bedienen:</b> sleep met de muis om de kaart te verschuiven, en zoom in en uit met het scrollwiel of met de knoppen + en - linksboven. Met een trackpad gaat het met twee vingers. Of klik eerst op de kaart: dan verschuiven de pijltjestoetsen de kaart, en zoomen de toetsen + en - in en uit.</p>

<h2>De clubs</h2>
<p>Naam en plaats zijn het belangrijkst om te controleren: samen bepalen ze welke club het is. Markering, beschrijving en website kunnen altijd nog veranderen.</p>
<div class="scroll"><table>
<tr><th>Club</th><th>Plaats</th><th>Website</th><th>Fotobond-nr.</th><th>Beschrijving</th><th>Opmerking</th></tr>
{''.join(table_rows)}
</table></div>

<script>
const clubs = {json.dumps(rows, ensure_ascii=False)};
const colors = {json.dumps({k: v[1] for k, v in STATUS.items()})};
const map = L.map('map');
L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
  maxZoom: 18, attribution: '&copy; OpenStreetMap-bijdragers'
}}).addTo(map);
const esc = s => s.replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
const bounds = [];
for (const c of clubs) {{
  const icon = L.divIcon({{
    className: 'pin', html: '<div style="background:' + colors[c.status] + '"></div>', iconSize: [18, 18],
    iconAnchor: [9 - c.dx, 9 - c.dy], tooltipAnchor: [c.dx, c.dy - 9], popupAnchor: [c.dx, c.dy - 9]
  }});
  const m = L.marker([c.lat, c.lon], {{icon, keyboard: false}}).addTo(map);
  const desc = c.remark ? esc(c.remark) : c.site ? '<i>Geen beschrijving.</i>' : '<i>Geen website.</i>';
  m.bindTooltip('<b>' + esc(c.name) + '</b>, ' + esc(c.town) + '<br>' + desc, {{maxWidth: 280, direction: 'top'}});
  const site = c.site ? '<br><a href="' + esc(c.site) + '" target="_blank" rel="noopener">' + esc(c.site.replace(/^https?:\\/\\/(www\\.)?/, '').replace(/\\/$/, '')) + '</a>' : '';
  m.bindPopup('<b>' + esc(c.name) + '</b><br>' + esc(c.town) + site + '<br><br>' + desc);
  bounds.push([c.lat, c.lon]);
}}
map.fitBounds(bounds, {{padding: [30, 30]}});
</script>
</body>
</html>
"""

OUTPUT.write_text(page, encoding="utf-8")
print(f"{len(rows)} clubs ({members} Fotobond) written to {OUTPUT}")
