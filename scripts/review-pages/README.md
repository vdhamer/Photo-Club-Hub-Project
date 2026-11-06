# Review pages for Fotobond afdelingen

Three scripts that build the pages a Fotobond afdeling contact reviews (Data#68, Data#77), plus - for now - one page for the
Belgian clubs. Each writes one self-contained HTML file into `~/Desktop/review/`, which mirrors
`fcdegender.nl/hub/review/`: same folder and file names, so the whole tree can be uploaded manually over FTP in one go.

| Script | Usage | Writes |
|---|---|---|
| `review-page.py` | `python3 review-page.py <afdeling>`, e.g. `06` | `afd<NN>/afdeling<NN>.html`: map and table of one afdeling |
| `review-page.py` | `python3 review-page.py BE` | `belgie/belgie.html`: map and table of the Belgian clubs |
| `index-page.py` | `python3 index-page.py` | `index.html`: links to all 17 pages, with club counts, the Fotobond clubs' share and a bar chart per afdeling |
| `remarks-page.py` | `python3 remarks-page.py` | `clubs.html`: all clubs and their remarks, with topics |

Paths are relative to `~/Desktop/review/` and to `fcdegender.nl/hub/review/` alike. Run `index-page.py` last: it shows
when each page in the tree was last written.

`former.py` is not run by itself: it holds the former-club rule the three scripts share (see below).

## Data source

The scripts read `clubsNL<NN>.level1.json` and `clubsBE.level1.json` from the working tree of the iOS repo
(`~/Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON/`), which should match what is live on GitHub `main`.
The paths are those of one Mac, on purpose: these are personal tools, not part of a build.

## The pages

`AFDELINGEN` in `review-page.py` lists all 16 afdelingen (there is no 13): number and name as the Fotobond writes it.
`BELGIUM` holds the Belgian page's folder and file name.
`index-page.py` reads both from `review-page.py`, so they are written down in one place.

Belgium has no afdelingen-like hierarchy (here yet), so its page is named after the country rather than like an afdeling's page.
It has no Fotobond colors, column or count: its clubs get one color of their own.

Per page, where needed, there are entries in `NOTES` and `DOUBTS`, both keyed by page (afdeling number, or `BE`) and
then by the club's `nickName`.

- `NOTES` is the Opmerking column: why a name or town was chosen. It is not in the JSON and not shown in the apps.
- `DOUBTS` lists clubs whose afdeling is uncertain; they get a grey marker. Empty when nothing is in doubt.
- When a club moves to another afdeling or gets another `nickName`, re-key its entries, or they silently disappear
  from the page. `review-page.py` prints a warning for every entry whose club is not in the page's file.

Map colors come from the Okabe-Ito palette, which is safe for color blindness: green for a Fotobond club, orange for
another club, grey for an afdeling in doubt, blue for a Belgian club.
The legend shows only the colors that occur on the page.

## Former clubs

`former.py` applies the rule from Data#91 ("The spec"): in `optional.logbook`, the last log entry with `isFormerClub`
or `isFormerMuseum` decides, and without such a log entry the club is not former.
If one log entry has both keys, `isFormerClub` wins.

- `review-page.py` lists a former club, because the afdeling contact is the person most likely to know whether it
  really stopped. It is a ghost on the map, a dotted ring with a pale fill that lies under the other pins, labeled
  "Mogelijk opgeheven" (not "gestopt", which next to the Fotobond labels could read as having left the Fotobond).
  It comes last in the legend. The Opmerking column and the map tooltip give the `date` of the deciding log entry.
  The intro counts only the active clubs and adds one sentence on those that may have stopped.
  The Fotobond number stays visible. Every former club gets this one label, because the JSON doesn't record how sure
  we are, and the wording invites a correction.
- `index-page.py` leaves former clubs out of both counts, and `remarks-page.py` leaves them out of `clubs.html`:
  these pages describe the clubs the apps show, and the apps hide former clubs.
- The pages show the deciding log entry's `date`, but not its `text` or `author`. This is about audience, not secrecy:
  the JSON is public on GitHub. Data#91 meant the logbook for maintainers (editing software, the HTML app's
  investigation view), and its entries are English working notes. To tell a contact in Dutch why we doubt a club
  still exists, add a sentence to that club's `NOTES` entry (the Opmerking column), not to its remark, which
  describes the club itself.
- No page links `badWebsites`: the scripts only read `website`.

## Cautions

- Running `review-page.py` overwrites that page's file in `~/Desktop/review/`.
  Don't run it as a test for a finished afdeling unless the page is meant to be replaced.
- To test, run the scripts with `HOME` pointing at a scratch folder that holds a copy of
  `Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON/`; they then write to that folder's `Desktop/review/` instead.
- The Persoonlijk<NN> entries are listed as pseudo-clubs, as in the apps, so a count can be one higher than the
  Fotobond roster.
- Regenerate `index.html` and `clubs.html` after any data or page change.
