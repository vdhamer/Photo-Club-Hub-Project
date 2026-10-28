# Created by Claude Code (guided by Peter van den Hamer) on 05/11/2026.

"""Returns whether a club (or museum) in a Level 1 JSON file is former, by the rule in Data#91 ("The spec"),
shared by the review-page scripts.

In `optional.logbook`, the last log entry that has `isFormerClub` or `isFormerMuseum` decides; without such a log entry
the organization defaults to not-former. The two keys are aliases; if one log entry has both, `isFormerClub` wins.
A log entry's `date` plays no part in the decision.

The review pages these scripts build show the deciding log entry's `date`, but not its `text` or `author`: Data#91
meant the logbook for maintainers (editing software, the HTML app's investigation view), 
and its entries, somewhat technical working notes (in English).
To tell the reader of a review page in Dutch why we doubt a club still exists, add a sentence to that club's NOTES
entry in review-page.py, which fills the page's Opmerking column. That is not the club's remark, which describes the
club itself.
"""


def former_entry(organization):
    """The log entry that makes the organization former, or None if it is not former."""
    result = None
    for entry in organization.get("optional", {}).get("logbook", []):
        key = next((k for k in ("isFormerClub", "isFormerMuseum") if k in entry), None)
        if key:  # a log entry without either key has no opinion, so it leaves the result as it was
            result = entry if entry[key] is True else None
    return result
