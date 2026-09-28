import sys
# Two families: cool blue-grey for what the project maintains, warm amber to brown for what the club maintains.
# Down the tree (club, member, photo) the colors get steadily darker.
# Checked with the dataviz skill's validator (2026-09-28): the club side is an ordinal one-hue ramp (monotone, visible
# steps, light end >= 2:1 on white); project blue vs club orange stays apart for color-blind readers (deutan dE 18.6).
# Photos get a neutral charcoal: they are the content itself and must not look owned by the project (blue).
CENTRAL,CLUB,MEMBER,PHOTO='#CDE2FB','#F0975F','#E0602C','#3B3B3F'
# The braces are neutral lines; their labels are filled with the color of the boxes they describe, like a legend.
T={
'en':dict(title="Photo Club Hub: who owns what (draft)",central="MAINTAINED BY THE PROJECT",own="MAINTAINED BY THE CLUB",clublist="Club list",club="Club",
 memlist="Club's member list",member="Member",portfolio="Member's portfolio",photo="Photo",points="points to",
 l1=["Level 1: the clubs","maintained by the project,","with a volunteer per region","lives on GitHub"],
 l2=["Level 2: the members","one list per club,","maintained by the club","lives on GitHub or the club's site"],
 l3=["Level 3: the photos","chosen by the club and its members,","rights stay with the photographer","lives on the club's own website"],
 nc1="photos are shown straight from",nc2="the club's website: ",nc3="no copies",
 app="The app",appsub="on iPhone and iPad",web="The web version",websub="in any browser, on any computer or phone"),
'nl':dict(title="Fotoclub Hub: wie is eigenaar van wat (concept)",central="BEHEERD DOOR HET PROJECT",own="BEHEERD DOOR DE CLUB",clublist="Clublijst",club="Club",
 memlist="Ledenlijst van de club",member="Lid",portfolio="Portfolio van het lid",photo="Foto",points="verwijst naar",
 l1=["Niveau 1: de clubs","bijgehouden door het project,","met een vrijwilliger per afdeling","staat op GitHub"],
 l2=["Niveau 2: de leden","één lijst per club,","bijgehouden door de club","staat op GitHub of de clubsite"],
 l3=["Niveau 3: de foto's","gekozen door de club en haar leden,","rechten blijven bij de fotograaf","staat op de eigen website van de club"],
 nc1="foto's komen rechtstreeks van",nc2="de website van de club: ",nc3="geen kopieën",
 app="De app",appsub="op iPhone en iPad",web="De webversie",websub="in elke browser, op elke computer of telefoon")}
lang,out=sys.argv[1],sys.argv[2]; t=T[lang]
esc=lambda x:x.replace("&","&amp;").replace("'","&#39;")
o=[]; a=o.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760" font-family="Helvetica, Arial, sans-serif">')
a(f'  <title>{esc(t["title"])}</title>')
a('  <!-- Generated from one script for both languages. Cool blue-grey: maintained by the project. Warm amber to brown:')
a('       maintained by the club, darker down the tree (club light, member mid, photo dark). The steps stay distinct in black and white. -->')
a('  <defs>\n    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker>')
a('    <symbol id="landscape" viewBox="0 0 40 26"><path d="M2,24 L13,9 L20,17 L26,11 L38,24 z" fill="#fff"/><circle cx="31" cy="5" r="3.5" fill="#fff"/></symbol>\n  </defs>')
a('  <rect width="1200" height="760" fill="#fff"/>')
def brace(x1,x2,y=67):
    # centered in the gap between the labels (bottom at y=38) and the tallest box stack (top at y=72)
    m=(x1+x2)/2
    return f'<path d="M{x1},{y} Q{x1},{y-12} {x1+14},{y-12} L{m-14},{y-12} Q{m},{y-12} {m},{y-24} Q{m},{y-12} {m+14},{y-12} L{x2-14},{y-12} Q{x2},{y-12} {x2},{y}"/>'
a('  <!-- ownership: curly braces above the columns -->')
a(f'  <g stroke="#333" stroke-width="2" fill="none">\n    {brace(60,310)}\n    {brace(420,1120)}\n  </g>')
def pill(cx,text,fill):
    # a label filled with exactly the color of the box it describes, so it reads as a legend
    w=len(text)*9.2+28
    return (f'  <rect x="{cx-w/2:.0f}" y="12" width="{w:.0f}" height="26" rx="13" fill="{fill}" stroke="#333" stroke-width="1.5"/>\n'
            f'  <text x="{cx}" y="30" font-size="13" font-weight="bold" fill="#222" letter-spacing="1" text-anchor="middle">{esc(text)}</text>')
a(pill(185,t["central"],CENTRAL))
a(pill(770,t["own"],CLUB))
ys=[135,179,223,267,311]
# column 1: the central club list, holding clubs
a('  <!-- column 1: club list (central) -->')
a(f'  <rect x="60" y="90" width="250" height="330" rx="8" fill="{CENTRAL}" stroke="#333" stroke-width="2.5"/>')
a(f'  <text x="185" y="116" font-size="16" font-weight="bold" fill="#222" text-anchor="middle">{esc(t["clublist"])}</text>')
for y in ys:
    a(f'  <rect x="95" y="{y}" width="180" height="36" rx="5" fill="{CLUB}" stroke="#333" stroke-width="1.5"/><text x="185" y="{y+24}" font-size="16" fill="#111" text-anchor="middle">{esc(t["club"])}</text>')
a('  <text x="185" y="378" font-size="22" fill="#555" text-anchor="middle">⋮</text>')
# column 2: member lists, owned by clubs
a('  <!-- column 2: one member list per club (club color), holding members -->')
for x,y,st,w in [(440,78,'#888','1.5'),(430,84,'#888','1.5'),(420,90,'#333','2.5')]:
    a(f'  <rect x="{x}" y="{y}" width="250" height="330" rx="8" fill="{CLUB}" stroke="{st}" stroke-width="{w}"/>')
a(f'  <text x="545" y="116" font-size="16" font-weight="bold" fill="#111" text-anchor="middle">{esc(t["memlist"])}</text>')
for y in ys:
    a(f'  <rect x="455" y="{y}" width="180" height="36" rx="5" fill="{MEMBER}" stroke="#333" stroke-width="1.5"/><text x="545" y="{y+24}" font-size="16" fill="#111" text-anchor="middle">{esc(t["member"])}</text>')
a('  <text x="545" y="378" font-size="22" fill="#222" text-anchor="middle">⋮</text>')
# column 3: portfolios, owned by members
a('  <!-- column 3: one portfolio per member (member color), holding photos -->')
for x,y,st,w in [(870,72,'#999','1.5'),(860,78,'#888','1.5'),(850,84,'#888','1.5'),(840,90,'#333','2.5')]:
    a(f'  <rect x="{x}" y="{y}" width="250" height="330" rx="8" fill="{MEMBER}" stroke="{st}" stroke-width="{w}"/>')
a(f'  <text x="965" y="116" font-size="16" font-weight="bold" fill="#111" text-anchor="middle">{esc(t["portfolio"])}</text>')
for y in ys:
    a(f'  <rect x="885" y="{y}" width="160" height="36" rx="5" fill="{PHOTO}" stroke="#222" stroke-width="1"/>'
      f'<use href="#landscape" x="895" y="{y+5}" width="40" height="26"/>'
      f'<text x="950" y="{y+24}" font-size="16" fill="#fff">{esc(t["photo"])}</text>')
a('  <text x="965" y="378" font-size="22" fill="#222" text-anchor="middle">⋮</text>')
# links
a('  <!-- links: each item points to the next file -->')
a('  <path d="M275,153 L416,153" stroke="#333" stroke-width="2.5" fill="none" marker-end="url(#arr)"/>')
a(f'  <text x="366" y="144" font-size="13" fill="#333" text-anchor="middle">{esc(t["points"])}</text>')
for y in ys[1:]:
    a(f'  <path d="M275,{y+18} L318,{y+18}" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arr)"/>')
a('  <path d="M635,153 L836,153" stroke="#333" stroke-width="2.5" fill="none" marker-end="url(#arr)"/>')
a(f'  <text x="742" y="144" font-size="13" fill="#333" text-anchor="middle">{esc(t["points"])}</text>')
for y in ys[1:]:
    a(f'  <path d="M635,{y+18} L690,{y+18}" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arr)"/>')
# captions
a('  <!-- captions: what, who maintains it, where it lives -->')
for cx,l in [(185,t['l1']),(545,t['l2']),(965,t['l3'])]:
    a(f'  <text x="{cx}" y="452" font-size="16" font-weight="bold" fill="#222" text-anchor="middle">{esc(l[0])}</text>')
    a(f'  <text x="{cx}" y="474" font-size="14" fill="#222" text-anchor="middle">{esc(l[1])}</text>')
    a(f'  <text x="{cx}" y="492" font-size="14" fill="#222" text-anchor="middle">{esc(l[2])}</text>')
    bold=' font-weight="bold"' if cx==965 else ''
    a(f'  <text x="{cx}" y="514" font-size="14" fill="#444" text-anchor="middle"{bold}>{esc(l[3])}</text>')
# collector and devices
a('  <!-- what people see: every level feeds both ways of viewing -->')
a('  <g stroke="#333" stroke-width="2.5" fill="none">\n    <path d="M185,530 L185,572"/>\n    <path d="M545,530 L545,572"/>\n    <path d="M965,530 L965,572"/>\n    <path d="M185,572 L965,572"/>\n    <path d="M360,572 L360,610" marker-end="url(#arr)"/>\n    <path d="M840,572 L840,610" marker-end="url(#arr)"/>\n  </g>')
a(f'  <text x="1110" y="598" font-size="13" fill="#333" text-anchor="end">{esc(t["nc1"])}</text>')
a(f'  <text x="1110" y="615" font-size="13" fill="#333" text-anchor="end">{esc(t["nc2"])}<tspan font-weight="bold">{esc(t["nc3"])}</tspan></text>')
phone=lambda x,y: f'  <rect x="{x}" y="{y}" width="34" height="62" rx="6" fill="#fff" stroke="#333" stroke-width="2.5"/>\n  <rect x="{x+4}" y="{y+8}" width="26" height="46" rx="2" fill="{CENTRAL}" stroke="#999" stroke-width="1"/>'
a(phone(343,628))
a(f'  <text x="360" y="718" font-size="18" font-weight="bold" fill="#222" text-anchor="middle">{esc(t["app"])}</text>')
a(f'  <text x="360" y="740" font-size="14" fill="#444" text-anchor="middle">{esc(t["appsub"])}</text>')
a(f'  <rect x="775" y="624" width="70" height="46" rx="4" fill="#fff" stroke="#333" stroke-width="2.5"/>\n  <rect x="781" y="630" width="58" height="34" fill="{CENTRAL}" stroke="#999" stroke-width="1"/>\n  <path d="M770,678 L850,678 L858,690 L762,690 z" fill="#fff" stroke="#333" stroke-width="2.5"/>')
a(phone(878,628))
a(f'  <text x="840" y="718" font-size="18" font-weight="bold" fill="#222" text-anchor="middle">{esc(t["web"])}</text>')
a(f'  <text x="840" y="740" font-size="14" fill="#444" text-anchor="middle">{esc(t["websub"])}</text>')
a('</svg>\n')
open(out,'w',encoding='utf-8').write('\n'.join(o))
