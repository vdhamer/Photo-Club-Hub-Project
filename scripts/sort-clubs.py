#!/usr/bin/env python3
"""Sort the clubs of each given Level 1 file by town, then fullName (both ignoring case), moving text blocks only.

Usage: python3 sort-clubs.py <file.level1.json> [...]
Formatting is untouched: only whole club objects move, separators stay in place.
Prints per file: clubs, entries out of place (the minimum number of moves), and whether the file changed.
"""

import bisect
import json
import re
import sys


def club_spans(text):
    """Text spans of the top-level objects in the "clubs" array; empty if the file has no clubs."""
    found = re.search(r'"clubs"\s*:', text)
    if not found:
        return []
    start = text.index("[", found.end())
    spans, depth, in_str, esc, obj_start = [], 0, False, False, None
    for i in range(start + 1, len(text)):
        ch = text[i]
        if in_str:
            esc = (ch == "\\") and not esc
            if ch == '"' and not esc:
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                obj_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                spans.append((obj_start, i + 1))
        elif ch == "]" and depth == 0:
            return spans
    return spans


def misplaced(keys):
    """Entries out of place: n minus the longest run that is already in order."""
    tails = []
    for k in keys:
        pos = bisect.bisect_right(tails, k)
        tails[pos:pos + 1] = [k]
    return len(keys) - len(tails)


def key(block):
    club = json.loads(block)["idPlus"]
    return club["town"].casefold(), club["fullName"].casefold()


if len(sys.argv) < 2:
    sys.exit("Usage: python3 sort-clubs.py <file.level1.json> [...]")

for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    old = json.loads(text)
    spans = club_spans(text)
    name = path.split("/")[-1]
    if len(spans) < 2:
        print(f"{name}\t{len(spans)}\t0\tunchanged")
        continue
    blocks = [text[a:b] for a, b in spans]
    ordered = sorted(blocks, key=key)
    seps = [text[spans[k][1]:spans[k + 1][0]] for k in range(len(spans) - 1)]
    new_text = (text[:spans[0][0]] + ordered[0] + "".join(s + b for s, b in zip(seps, ordered[1:]))
                + text[spans[-1][1]:])
    new = json.loads(new_text)
    assert {k: v for k, v in new.items() if k != "clubs"} == {k: v for k, v in old.items() if k != "clubs"}
    canon = lambda clubs: sorted(json.dumps(c, sort_keys=True) for c in clubs)
    assert canon(new["clubs"]) == canon(old["clubs"])
    if new_text != text:
        open(path, "w", encoding="utf-8").write(new_text)
    print(f"{name}\t{len(spans)}\t{misplaced([key(b) for b in blocks])}\t{'sorted' if new_text != text else 'unchanged'}")
