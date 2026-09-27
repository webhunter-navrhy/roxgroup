#!/usr/bin/env python3
"""Generuje logo ROX GROUP jako čisté SVG křivky (písmo Archivo, OFL) + šestihranná matice místo „O“."""
import math, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

here = pathlib.Path(__file__).parent
YEL, INK, WHITE, STEEL = '#FFC21A', '#15171A', '#F4F4F1', '#8A9098'

def inst(wght, wdth):
    return instantiateVariableFont(TTFont(here / 'Archivo.ttf'), {'wght': wght, 'wdth': wdth})

heavy, mid = inst(820, 125), inst(600, 125)

def glyph(font, ch, x, y, scale=1.0):
    gs = font.getGlyphSet(); name = font.getBestCmap()[ord(ch)]
    pen = SVGPathPen(gs)
    gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
    bp = BoundsPen(gs); gs[name].draw(bp)
    return pen.getCommands(), gs[name].width * scale, bp.bounds

def text_path(font, s, x, y, size, tracking=0):
    sc = size / 1000; d = []; cx = x
    for ch in s:
        if ch == ' ': cx += 250 * sc + tracking; continue
        cmd, adv, _ = glyph(font, ch, cx, y, sc); d.append(cmd); cx += adv + tracking
    return ' '.join(d), cx - tracking - x

def hexagon(cx, cy, h, r_round=26):
    """Šestihran s plochou horní a dolní hranou, zaoblené rohy."""
    R = h / math.sqrt(3)  # vzdálenost středu od vrcholu (h = výška mezi plochami)
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    d = ''
    for i, p in enumerate(pts):
        prv, nxt = pts[i - 1], pts[(i + 1) % 6]
        def toward(a, b, dist):
            L = math.dist(a, b); return (a[0] + (b[0] - a[0]) * dist / L, a[1] + (b[1] - a[1]) * dist / L)
        p1, p2 = toward(p, prv, r_round), toward(p, nxt, r_round)
        d += ('M' if i == 0 else 'L') + f'{p1[0]:.1f} {p1[1]:.1f} Q{p[0]:.1f} {p[1]:.1f} {p2[0]:.1f} {p2[1]:.1f} '
    return d + 'Z', 2 * R

def circle(cx, cy, r):
    return f'M{cx - r:.1f} {cy:.1f} a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0 a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0Z'

CAP = 686  # výška verzálek Archiva v jednotkách písma

def rox(x0, base, fg, nut):
    """Vrátí SVG prvky slova R⬢X a jeho šířku."""
    r_cmd, r_adv, r_b = glyph(heavy, 'R', 0, 0)
    x_cmd, x_adv, x_b = glyph(heavy, 'X', 0, 0)
    gap = 62
    rx = x0 - r_b[0]
    r_cmd, _, _ = glyph(heavy, 'R', rx, base)
    r_right = rx + r_b[2]
    hx_d, hx_w = hexagon(0, 0, CAP)
    ncx = r_right + gap + hx_w / 2; ncy = base - CAP / 2
    hx_d, _ = hexagon(ncx, ncy, CAP)
    hole = circle(ncx, ncy, CAP * 0.265)
    xx = ncx + hx_w / 2 + gap - x_b[0]
    x_cmd, _, _ = glyph(heavy, 'X', xx, base)
    width = xx + x_b[2] - x0
    els = (f'<path d="{r_cmd}" fill="{fg}"/>'
           f'<path d="{hx_d} {hole}" fill="{nut}" fill-rule="evenodd"/>'
           f'<path d="{x_cmd}" fill="{fg}"/>')
    return els, width

def svg(w, h, body, title='ROX GROUP'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

out = here
for mode, fg, sub in [('light', INK, '#5B6168'), ('dark', WHITE, '#A7ADB4')]:
    # 1) hlavní logo: ROX + GROUP pod ním přes celou šířku
    pad = 60
    els, w = rox(pad, pad + CAP, fg, YEL)
    size = 200
    word, ww = text_path(mid, 'GROUP', 0, 0, size)
    track = (w - ww) / 4
    word, _ = text_path(mid, 'GROUP', pad, pad + CAP + 80 + size * 0.686, size, track)
    H = pad + CAP + 80 + size * 0.686 + pad
    (out / f'logo-{mode}.svg').write_text(svg(w + 2 * pad, H, els + f'<path d="{word}" fill="{sub}"/>'))

    # 2) horizontální (navigace): ROX | GROUP
    els, w = rox(0, CAP, fg, YEL)
    rule_x = w + 70
    size = 240
    g, gw = text_path(mid, 'GROUP', rule_x + 70, CAP / 2 + size * 0.686 / 2, size, 34)
    body = els + f'<rect x="{rule_x:.0f}" y="40" width="14" height="{CAP - 80}" fill="{sub}" opacity=".55"/>' + f'<path d="{g}" fill="{fg}"/>'
    (out / f'logo-horizontal-{mode}.svg').write_text(svg(rule_x + 70 + gw + 4, CAP, body))

# 3) symbol a favicon
hx, hw = hexagon(0, 0, CAP)
R = hw / 2
sym = svg(hw + 40, CAP + 40, f'<path d="{hexagon(R + 20, CAP / 2 + 20, CAP)[0]} {circle(R + 20, CAP / 2 + 20, CAP * 0.265)}" fill="{YEL}" fill-rule="evenodd"/>', 'ROX GROUP — symbol')
(out / 'symbol.svg').write_text(sym)
fav = svg(64, 64, f'<rect width="64" height="64" rx="14" fill="{INK}"/><path d="{hexagon(32, 32, 40, 2.4)[0]} {circle(32, 32, 10.6)}" fill="{YEL}" fill-rule="evenodd"/>', 'ROX GROUP')
(out / 'favicon.svg').write_text(fav)
print('ok')
