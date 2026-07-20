#!/usr/bin/env python3
"""Generates assets/pixel-banner.svg -- a hand-built pixel-art (5x7 bitmap font)
animated terminal banner in the amber/zinc cyberpunk theme, with a small
pixel rotary-telephone + rising smoke motif in the corner."""

FONT = {
    "S": ["01111","10000","10000","01110","00001","00001","11110"],
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "N": ["10001","11001","10101","10101","10011","10001","10001"],
    "G": ["01110","10001","10000","10111","10001","10001","01111"],
    "M": ["10001","11011","10101","10101","10001","10001","10001"],
    "D": ["11110","10001","10001","10001","10001","10001","11110"],
    "E": ["11111","10000","11110","10000","10000","10000","11111"],
    "V": ["10001","10001","10001","10001","10001","01010","00100"],
    "F": ["11111","10000","11110","10000","10000","10000","10000"],
    "U": ["10001","10001","10001","10001","10001","10001","01110"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    "T": ["11111","00100","00100","00100","00100","00100","00100"],
    "K": ["10001","10010","10100","11000","10100","10010","10001"],
    "C": ["01111","10000","10000","10000","10000","10000","01111"],
    "R": ["11110","10001","10001","11110","10100","10010","10001"],
    "I": ["11111","00100","00100","00100","00100","00100","11111"],
    "P": ["11110","10001","10001","11110","10000","10000","10000"],
    "B": ["11110","10001","10001","11110","10001","10001","11110"],
    "J": ["00111","00010","00010","00010","00010","10010","01100"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "W": ["10001","10001","10001","10101","10101","11011","10001"],
    ".": ["00000","00000","00000","00000","00000","00000","00100"],
    " ": ["00000","00000","00000","00000","00000","00000","00000"],
    "/": ["00001","00001","00010","00100","01000","10000","10000"],
    "-": ["00000","00000","00000","11111","00000","00000","00000"],
}

def render_word(word, x0, y0, px, color, id_prefix, glow=False):
    """Return list of <rect> strings for a word starting at x0,y0 using pixel size px."""
    rects = []
    cursor_x = x0
    for ch in word:
        bitmap = FONT.get(ch.upper())
        if bitmap is None:
            cursor_x += px * 6
            continue
        for row_i, row in enumerate(bitmap):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    rx = cursor_x + col_i * px
                    ry = y0 + row_i * px
                    rects.append(f'<rect x="{rx}" y="{ry}" width="{px}" height="{px}" fill="{color}"/>')
        cursor_x += px * 6  # 5 wide + 1 spacing
    return rects, cursor_x

def word_width(word, px):
    return len(word) * px * 6 - px  # remove trailing spacing

PX = 6
AMBER = "#F59E0B"
AMBER_DIM = "#B45309"
ZINC_BG = "#09090b"
ZINC_BORDER = "#27272a"
ZINC_TEXT = "#a1a1aa"

title1 = "SANGAM"
title2 = ".DEV"

w1 = word_width(title1, PX)
w2 = word_width(title2, PX)
total_title_w = w1 + PX * 3 + w2

svg_w = 900
svg_h = 220

title_x = (svg_w - total_title_w) // 2 - 40
title_y = 46

rects1, next_x = render_word(title1, title_x, title_y, PX, AMBER, "t1")
rects2, next_x2 = render_word(title2, next_x + PX * 3, title_y, PX, "#e4e4e7", "t2")

cursor_x = next_x2 + PX * 2
cursor_y = title_y

# subtitle typed line
SUB_PX = 3
subtitle = "FULL-STACK DEV / JAVA - SPRING BOOT - REACT"
sub_w = word_width(subtitle, SUB_PX)
sub_x = (svg_w - sub_w) // 2 - 40
sub_y = title_y + 7 * PX + 22
rects_sub, _ = render_word(subtitle, sub_x, sub_y, SUB_PX, AMBER_DIM, "sub")

# scanline pattern
scanlines = "\n".join(
    f'<rect x="0" y="{y}" width="{svg_w}" height="1" fill="#000000" opacity="0.06"/>'
    for y in range(0, svg_h, 4)
)

# pixel border frame (corner brackets, arcade style)
def corner(x, y, dx, dy):
    n = 5
    parts = []
    for i in range(n):
        parts.append(f'<rect x="{x + i*dx*PX}" y="{y}" width="{PX}" height="{PX}" fill="{AMBER}"/>')
    for i in range(n):
        parts.append(f'<rect x="{x}" y="{y + i*dy*PX}" width="{PX}" height="{PX}" fill="{AMBER}"/>')
    return parts

corners = []
m = 14
corners += corner(m, m, 1, 1)
corners += corner(svg_w - m - PX, m, -1, 1)
corners += corner(m, svg_h - m - PX, 1, -1)
corners += corner(svg_w - m - PX, svg_h - m - PX, -1, -1)

# pixel rotary telephone + smoke motif, bottom-right, small scale
phone_px = 5
phone_x = svg_w - 150
phone_y = svg_h - 78

PHONE_MAP = [
    "0011111100",
    "0111111110",
    "1111111111",
    "1100000011",
    "1100000011",
    "1111111111",
    "0001111000",
    "0001111000",
]
phone_rects = []
for r, row in enumerate(PHONE_MAP):
    for c, bit in enumerate(row):
        if bit == "1":
            phone_rects.append(
                f'<rect x="{phone_x + c*phone_px}" y="{phone_y + r*phone_px}" '
                f'width="{phone_px}" height="{phone_px}" fill="{AMBER}" opacity="0.9"/>'
            )

# rising smoke: 3 small pixel puffs, animate translateY + fade, staggered
smoke_x = phone_x + 44
smoke_y = phone_y - 6
smoke = []
for i in range(3):
    delay = i * 0.9
    sx = smoke_x + (i - 1) * 6
    smoke.append(f'''
  <rect x="{sx}" y="{smoke_y}" width="4" height="4" fill="#d4d4d8" opacity="0">
    <animate attributeName="opacity" values="0;0.8;0" dur="2.6s" begin="{delay}s" repeatCount="indefinite"/>
    <animate attributeName="y" values="{smoke_y};{smoke_y-34}" dur="2.6s" begin="{delay}s" repeatCount="indefinite"/>
    <animate attributeName="x" values="{sx};{sx + (6 if i%2==0 else -6)}" dur="2.6s" begin="{delay}s" repeatCount="indefinite"/>
  </rect>''')

svg = f'''<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .flicker {{ animation: flicker 5s infinite; }}
      @keyframes flicker {{
        0%, 92%, 100% {{ opacity: 0.06; }}
        93%, 96% {{ opacity: 0.12; }}
      }}
    </style>
  </defs>

  <rect width="{svg_w}" height="{svg_h}" fill="{ZINC_BG}"/>
  <rect x="2" y="2" width="{svg_w-4}" height="{svg_h-4}" fill="none" stroke="{ZINC_BORDER}" stroke-width="2"/>

  <g class="flicker">
    {scanlines}
  </g>

  {''.join(corners)}

  <g>
    {''.join(rects1)}
    {''.join(rects2)}
    <rect x="{cursor_x}" y="{cursor_y}" width="{PX}" height="{PX*7}" fill="{AMBER}">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <g>
    {''.join(rects_sub)}
  </g>

  <g>
    {''.join(phone_rects)}
    {''.join(smoke)}
  </g>

  <text x="{m+4}" y="{svg_h - m - 2}" font-family="monospace" font-size="10" fill="{ZINC_TEXT}">Tamil Nadu, IN :: building in public</text>
</svg>
'''

with open("assets/pixel-banner.svg", "w") as f:
    f.write(svg)

print("done", svg_w, svg_h, "title width", total_title_w)
