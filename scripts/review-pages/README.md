# Review pages for Fotobond afdelingen

Three scripts that build the pages a Fotobond afdeling contact reviews (Data#68, Data#77). Each writes one
self-contained HTML file to `~/Desktop`; the files are uploaded to `fcdegender.nl/hub/review/` by hand over FTP.

| Script | Usage | Writes |
|---|---|---|
| `review-page.py` | `python3 review-page.py <afdeling>`, e.g. `06` | `~/Desktop/<region>/afdeling<NN>.html`: map and table of one afdeling |
| `index-page.py` | `python3 index-page.py` | `~/Desktop/review/index.html`: links to all afdeling pages |
| `remarks-page.py` | `python3 remarks-page.py` | `~/Desktop/review/clubs.html`: all clubs and their remarks, with topics |

## Data source

The scripts read `clubsNL<NN>.level1.json` from the working tree of the iOS repo
(`~/Developer/Xcode projects/SwiftUI/Photo Club Hub/JSON/`), which should match what is live on GitHub `main`.
The paths are those of one Mac, on purpose: these are personal tools, not part of a build.

## Adding an afdeling

In `review-page.py`: add a line to `AFDELINGEN` (number: region name, Desktop folder), and, where needed, entries
in `NOTES` and `DOUBTS`, both keyed by afdeling number and then by the club's `nickName`.
`index-page.py` reads `AFDELINGEN` from `review-page.py`, so it needs no change.

- `NOTES` is the Opmerking column: why a name or town was chosen. It is not in the JSON and not shown in the apps.
- `DOUBTS` lists clubs whose afdeling is uncertain; they get a grey marker. Empty when nothing is in doubt.
- A nick name is unique across all files, so a note follows its club when the club moves to another file. Remove
  or re-key the entry when the club moves to an afdeling with its own page.

## Cautions

- Running `review-page.py` overwrites that afdeling's Desktop page. Don't run it as a test for a finished afdeling
  unless the page is meant to be replaced.
- The Persoonlijk<NN> entries are listed as pseudo-clubs, as in the apps, so a count can be one higher than the
  Fotobond roster.
- Regenerate `index.html` and `clubs.html` after any data or page change.
