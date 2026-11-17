# Created by Claude Code (guided by Peter van den Hamer) on 17/11/2026.

"""Returns the clubs of a Level 1 file together with those of the files it includes, shared by the review-page scripts.

A Level 1 file can list other Level 1 files in `level1Header.level1URLIncludes`; the apps load those too. Since
clubsBE.level1.json moved the Antwerp clubs into clubsBE-Antwerpen.level1.json, reading only the file's own `clubs`
would drop most Belgian clubs from the pages. Each include is resolved by its file name in the same folder as the
including file (the iOS repo's JSON folder), not fetched from its URL, so the pages show the working tree.
A file that is included twice is read once. An include that is missing locally stops the script with a message,
because a page silently lacking that file's clubs would look complete.
"""

import json
from pathlib import Path
from urllib.parse import urlparse


def clubs_with_includes(path, _seen=None):
    """The clubs in the Level 1 file at `path`, followed by those of its includes, depth first."""
    seen = _seen if _seen is not None else set()
    path = Path(path)
    if path.name in seen:
        return []
    seen.add(path.name)
    data = json.loads(path.read_text(encoding="utf-8"))
    clubs = list(data.get("clubs", []))
    for url in data.get("level1Header", {}).get("level1URLIncludes", []):
        include = path.parent / Path(urlparse(url).path).name  # file name only, without any ?query or #fragment
        if not include.exists():
            raise SystemExit(f"{path.name} includes {include.name}, which is not in {path.parent}")
        clubs += clubs_with_includes(include, seen)
    return clubs
