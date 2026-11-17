# Created by Claude Code (guided by Peter van den Hamer) on 17/11/2026.

"""The banner at the bottom of every review page, shared by the review-page scripts: a plain-CSS lookalike of the
navigation bar on the pages that the HTML app generates, so a reader of the review mini-site can navigate
to the main site (fcdegender.nl/hub/nl/clubs and so on). And a reader of the review pages is aware that these pages
are part of the Photo Club Hub project.

The original is `SiteNavigationBar` in the HTML app (Photo Club Hub HTML/Ignite/SiteNavigationBar.swift), a Bootstrap
navbar built with Ignite. 
The copy here uses no Bootstrap: loading Bootstrap's CSS would restyle the whole review page, not only the banner.
The Documentatie menu at bottom right is an HTML <details> element, so it works without JavaScript.
When the app's menu changes, change it here too: nothing keeps the two in step.

Every URL is absolute, including the host, so the banner works both online and when a page is opened from
~/Desktop/review before uploading. The texts are currently in Dutch only, just like the rest of the review pages.

Put BANNER_CSS at the end of a page's <style> (it also adds room at the bottom of the page, so the fixed banner never
covers the last table rows) and BANNER_HTML just before </body>.
"""

HUB = "https://www.fcdegender.nl/hub"

# Colors as on the HTML app's pages: Ignite's antiqueWhite at 75% for the bar, Bootstrap's secondary grey for the
# app button, and Bootstrap's primary blue for the links.
BANNER_CSS = """
  body { padding-bottom: 96px; }
  .hub-banner { position: fixed; left: 0; right: 0; bottom: 0; z-index: 1030; box-sizing: border-box;
                display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 4px 12px;
                padding: 8px 12px; background: rgb(250 235 215 / 75%);
                font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  .hub-banner a { text-decoration: none; }
  .hub-brand { display: inline-flex; align-items: center; padding: 4px 8px; border-radius: 4px;
               background: #6c757d; color: #fff !important; font-size: 14px; }
  .hub-brand:hover { background: #5c636a; }
  .hub-brand img { width: 40px; padding-right: 15px; box-sizing: border-box; }
  .hub-links { display: flex; flex-wrap: wrap; align-items: center; list-style: none; margin: 0; padding: 0; }
  .hub-links > li > a, .hub-links summary { display: block; padding: 8px; }
  .hub-links > li > a { color: #0d6efd; }
  .hub-links > li > a:hover { text-decoration: underline; }
  .hub-links details { position: relative; }
  .hub-links summary { color: rgba(0, 0, 0, 0.65); cursor: pointer; list-style: none; white-space: nowrap; }
  .hub-links summary::-webkit-details-marker { display: none; }
  .hub-links summary::after { content: ""; display: inline-block; margin-left: 0.3em; vertical-align: 0.25em;
                              border-bottom: 0.3em solid; border-left: 0.3em solid transparent;
                              border-right: 0.3em solid transparent; }
  .hub-menu { position: absolute; right: 0; bottom: 100%; margin: 0 0 4px; padding: 8px 0; list-style: none;
              min-width: 10rem; white-space: nowrap; background: #fff; border: 1px solid rgba(0, 0, 0, 0.175);
              border-radius: 6px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }
  .hub-menu a { display: block; padding: 4px 16px; color: #212529; }
  .hub-menu a:hover { background: #e9ecef; }
  /* On a phone the app's navbar collapses into a menu button. Here the button keeps only its icon instead, and the
     links get smaller, so the banner stays one line high and covers little of the page. */
  @media (max-width: 600px) {
    body { padding-bottom: 64px; }
    .hub-banner { padding: 6px; gap: 4px; flex-wrap: nowrap; }
    .hub-brand { padding: 4px; }
    .hub-brand img { width: 25px; padding-right: 0; }
    .hub-brand span { display: none; }
    .hub-links { flex-wrap: nowrap; }
    .hub-links > li > a, .hub-links summary { padding: 6px 3px; font-size: 14px; }
  }
  @media print { .hub-banner { display: none; } body { padding-bottom: 0; } }
"""

BANNER_HTML = f"""<nav class="hub-banner" aria-label="Photo Club Hub">
<a class="hub-brand" href="{HUB}/"><img src="{HUB}/images/AppIcon.png" alt="" title="Fotoclub Hub netwerk"><span>Fotoclub Hub netwerk</span></a>
<ul class="hub-links">
<li><a href="{HUB}/nl/clubs">Fotoclubs</a></li>
<li><a href="{HUB}/nl/museums">Fotomusea</a></li>
<li><a href="{HUB}/nl/expertises/">Expertises</a></li>
<li><details><summary>Documentatie</summary><ul class="hub-menu">
<li><a href="https://github.com/vdhamer/Photo-Club-Hub/blob/main/.github/README.md#photo-club-hub">Photo Club Hub</a></li>
<li><a href="https://github.com/vdhamer/Photo-Club-Hub-HTML/blob/main/.github/README.md#photo-club-hub-html">Photo Club Hub HTML</a></li>
<li><a href="https://tinyurl.com/fchFAQnl">FAQ</a></li>
<li><a href="https://swiftpackageindex.com/twostraws/Ignite">Ignite package</a></li>
</ul></details></li>
</ul>
</nav>
"""
