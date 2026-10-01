"""Wrap the Platane/snk SVG in a light cream card so it matches the profile theme.

snk only supports a background colour for GIF output, so we post-process the SVG:
pad the viewBox and insert a rounded rectangle as the first child.

Usage: python3 .github/scripts/snake_card.py dist/github-contribution-grid-snake.svg
"""
import re
import sys
from pathlib import Path

PAD = 18
FILL, STROKE, RADIUS = "#faf9f5", "#e6dfd8", 18

path = Path(sys.argv[1])
svg = path.read_text()

m = re.search(r'viewBox="(-?[\d.]+) (-?[\d.]+) ([\d.]+) ([\d.]+)"', svg)
if not m:
    sys.exit("viewBox not found")
x, y, w, h = map(float, m.groups())
nx, ny, nw, nh = x - PAD, y - PAD, w + 2 * PAD, h + 2 * PAD

svg = svg.replace(m.group(0), f'viewBox="{nx:g} {ny:g} {nw:g} {nh:g}"', 1)
svg = re.sub(r'(<svg[^>]*?)width="[\d.]+" height="[\d.]+"', rf'\1width="{nw:g}" height="{nh:g}"', svg, count=1)

card = (f'<rect x="{nx + 0.5:g}" y="{ny + 0.5:g}" width="{nw - 1:g}" height="{nh - 1:g}" '
        f'rx="{RADIUS}" fill="{FILL}" stroke="{STROKE}"/>')
svg = re.sub(r'(<svg[^>]*>)', rf'\1{card}', svg, count=1)

path.write_text(svg)
print(f"wrapped {path} -> viewBox {nx:g} {ny:g} {nw:g} {nh:g}")
