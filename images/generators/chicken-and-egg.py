import sys
# Same families as who-owns-what: the circle in light blue-grey, our levers in the project's dark blue.
NODE,LEVER='#CDE2FB','#1C5CAB'
T={'en':dict(title="Photo Club Hub: breaking the chicken-and-egg problem (draft)",
   top=("Few clubs","take part"),right=("Little","to see"),bottom=("Few people","use it"),left=("Little reason for","a club to join"),
   center=("The chicken-and-egg","problem"),
   lev_r=["We put clubs on the map","in advance, so there is","something to see"],
   lev_l=["We simplify data entry to","check-and-correct, and split","the process into a few steps"]),
 'nl':dict(title="Fotoclub Hub: het kip-en-ei-probleem doorbreken (concept)",
   top=("Weinig clubs","doen mee"),right=("Weinig","te zien"),bottom=("Weinig mensen","gebruiken het"),left=("Weinig reden voor","een club om mee te doen"),
   center=("Het kip-en-ei-","probleem"),
   lev_r=["We zetten clubs vooraf","op de kaart, zodat er","iets te zien is"],
   lev_l=["We maken invoeren eenvoudiger:","alleen controleren en","verbeteren, in een paar stappen"])}
lang,out=sys.argv[1],sys.argv[2]; t=T[lang]
esc=lambda x:x.replace("&","&amp;").replace("'","&#39;")
W,H=920,600
nodes={'top':(460,150),'right':(730,330),'bottom':(460,510),'left':(190,330)}
bw,bh=236,60
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">',
 f'  <title>{esc(t["title"])}</title>',
 '  <!-- Generated from one script for both languages. Light boxes: the vicious circle. Dark blue-grey boxes: our levers. -->',
 '  <defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker></defs>',
 f'  <rect width="{W}" height="{H}" fill="#fff"/>']
def quad(p0,c,p2): return f'M{p0[0]},{p0[1]} Q{c[0]},{c[1]} {p2[0]},{p2[1]}'
def mid(p0,c,p2): return (0.25*p0[0]+0.5*c[0]+0.25*p2[0], 0.25*p0[1]+0.5*c[1]+0.25*p2[1])
edges={'tr':((578,150),(730,150),(730,296)),'rb':((730,364),(730,510),(582,510)),
       'bl':((338,510),(190,510),(190,364)),'lt':((190,296),(190,150),(338,150))}
o.append('  <!-- the vicious circle, clockwise -->')
for p0,c,p2 in edges.values():
    o.append(f'  <path d="{quad(p0,c,p2)}" stroke="#333" stroke-width="2.5" fill="none" marker-end="url(#arr)"/>')
for k,(cx,cy) in nodes.items():
    a,b=t[k]
    o.append(f'  <rect x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" rx="8" fill="{NODE}" stroke="#333" stroke-width="2.5"/>')
    o.append(f'  <text x="{cx}" y="{cy-4}" font-size="17" fill="#222" text-anchor="middle">{esc(a)}</text>')
    o.append(f'  <text x="{cx}" y="{cy+17}" font-size="17" fill="#222" text-anchor="middle">{esc(b)}</text>')
# a hatching chick with a piece of shell on its head: a chick and an egg at once (a generic motif, not a known character)
o.append('''  <!-- illustration: hatching chick -->
  <g stroke="#333" stroke-width="2.5" stroke-linejoin="round">
    <circle cx="460" cy="268" r="30" fill="#FFD34D"/>
    <circle cx="450" cy="264" r="3.8" fill="#222" stroke="none"/><circle cx="451.3" cy="262.7" r="1.2" fill="#fff" stroke="none"/>
    <circle cx="470" cy="264" r="3.8" fill="#222" stroke="none"/><circle cx="471.3" cy="262.7" r="1.2" fill="#fff" stroke="none"/>
    <path d="M454,274 L466,274 L460,283 Z" fill="#F08A24" stroke-width="1.5"/>
    <path d="M414,290 L425,280 L436,291 L447,280 L458,291 L469,280 L480,291 L491,280 L506,290 A46,40 0 0 1 414,290 Z" fill="#fff"/>
    <g transform="rotate(-12 460 240)">
      <path d="M418,254 L427,245 L436,254 L445,245 L454,254 L463,245 L472,254 L481,245 L490,254 L502,254 A42,34 0 0 0 418,254 Z" fill="#fff"/>
    </g>
  </g>''')
o.append(f'  <text x="460" y="372" font-size="20" font-weight="bold" fill="#222" text-anchor="middle">{esc(t["center"][0])}</text>')
o.append(f'  <text x="460" y="396" font-size="20" font-weight="bold" fill="#222" text-anchor="middle">{esc(t["center"][1])}</text>')
def cut(edge):
    # an interruption of the arc: a gap, closed off by a short bar across the arc at each end,
    # oriented along the arc's direction at its midpoint so it reads the same on every arc
    p0,c,p2=edge; x,y=mid(*edge)
    tx,ty=p2[0]-p0[0],p2[1]-p0[1]; n=(tx*tx+ty*ty)**0.5; tx,ty=tx/n,ty/n
    nx,ny=-ty,tx; g,h=9,13
    ax,ay,bx,by=x-tx*g,y-ty*g,x+tx*g,y+ty*g
    return (f'  <g stroke-linecap="round">\n'
            f'    <line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#fff" stroke-width="9"/>\n'
            f'    <line x1="{ax-nx*h:.1f}" y1="{ay-ny*h:.1f}" x2="{ax+nx*h:.1f}" y2="{ay+ny*h:.1f}" stroke="#333" stroke-width="3.5"/>\n'
            f'    <line x1="{bx-nx*h:.1f}" y1="{by-ny*h:.1f}" x2="{bx+nx*h:.1f}" y2="{by+ny*h:.1f}" stroke="#333" stroke-width="3.5"/>\n  </g>')
m_tr=mid(*edges['tr']); m_lt=mid(*edges['lt'])
o.append('  <!-- where the strategy breaks the circle -->'); o.append(cut(edges['tr'])); o.append(cut(edges['lt']))
def lever(x,y,w,lines,target):
    h=22*len(lines)+20
    s=[f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{LEVER}"/>']
    for i,l in enumerate(lines):
        s.append(f'  <text x="{x+w/2}" y="{y+28+22*i}" font-size="15" fill="#fff" text-anchor="middle">{esc(l)}</text>')
    s.append(f'  <path d="M{x+w/2},{y+h} L{target[0]:.0f},{target[1]-18:.0f}" stroke="#333" stroke-width="2.5" fill="none" marker-end="url(#arr)"/>')
    return '\n'.join(s)
o.append(lever(630,14,270,t['lev_r'],(m_tr[0]+8,m_tr[1])))
o.append(lever(20,14,270,t['lev_l'],(m_lt[0]-8,m_lt[1])))
o.append('</svg>\n')
open(out,'w',encoding='utf-8').write('\n'.join(o))
