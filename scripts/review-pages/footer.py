# Created by Claude Code (guided by Peter van den Hamer) on 18/11/2026.

"""The footer at the bottom of every review page, shared by the review-page scripts: the sentence saying when the page
was generated, in the same words and date format as on the pages the HTML app generates (Project#28).

The original is `FooterText` in the HTML app (Photo Club Hub HTML/Ignite/FooterText.swift). It formats `Date.now` with
`Date.FormatStyle(date: .abbreviated, time: .shortened, locale: nl)` followed by `TimeZone.current.abbreviation()`,
giving e.g. "16 nov 2026, 22:51 GMT+1". This copy builds that string in plain Python, without locale settings, so the
output doesn't depend on the Mac's language. When the app's wording or format changes, change it here too: nothing
keeps the two implementations (in Swift, with a copy in Python) in step.

It is the generation time, not the time the clubs last changed: every run gives every page a new time.

Put FOOTER_CSS at the end of a page's <style> and footer_html() after the page's last content, just before
BANNER_HTML. The footer is in the normal page flow, so BANNER_CSS's bottom padding keeps it clear of the fixed banner.
Unlike the banner, the footer is printed.
"""

import datetime

# Apple's Dutch abbreviated month names, as Date.FormatStyle(date: .abbreviated) writes them for locale "nl":
# no trailing periods, and "mrt" for March.
MONTHS = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

# The app's footer is a Bootstrap alert without a color variant (so: no background or border, padding 1rem) with
# text-center. Its 3rem bottom margin is left out: BANNER_CSS already adds room below the page for the banner.
# max-width: none overrides the pages' own `p { max-width: 46em; }` (index.html), which would squeeze the footer into a
# narrower, off-center box and wrap it. Size and color are those of the pages' help text (15px, muted), so the footer
# doesn't stand out more than the notes above it. The timestamp never breaks inside, so a narrow screen wraps the
# sentence before the date, not before "GMT+1".
FOOTER_CSS = """
  .hub-footer { max-width: none; margin: 0.5rem 0 0; padding: 1rem; text-align: center; font-size: 15px;
                color: var(--muted, #555); }
  .hub-footer span { white-space: nowrap; }
"""


def footer_html(now=None):
    """The generation-time footer; `now` (an aware datetime) is only passed by a test."""
    now = now or datetime.datetime.now().astimezone()
    hours = int(now.utcoffset().total_seconds() // 3600)
    zone = "GMT" if hours == 0 else f"GMT{hours:+d}"  # as Foundation's abbreviation(): GMT+1 in winter, GMT+2 in summer
    # Day and hour without a leading zero, minutes with one, as Apple writes them: "6 nov 2026, 9:05".
    stamp = f"{now.day} {MONTHS[now.month - 1]} {now.year}, {now.hour}:{now.minute:02d} {zone}"
    return (f'<p class="hub-footer">Deze pagina is onderdeel van het Fotoclub Hub netwerk '
            f'en is gegenereerd op <span>{stamp}</span>.</p>\n')
