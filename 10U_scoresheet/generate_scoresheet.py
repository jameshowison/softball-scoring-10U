#!/usr/bin/env python3
"""
Generate 10U softball scoresheet HTML.

Usage:
    python3 generate_scoresheet.py --size letter --orientation landscape
    python3 generate_scoresheet.py --size letter --orientation portrait
    python3 generate_scoresheet.py --size a4 --orientation portrait
"""

import argparse
import math
import os

# ── Page sizes (mm, portrait convention: width × height) ──────────────────────
PAGE_SIZES = {
    'letter': (215.9, 279.4),
    'a4':     (210.0, 297.0),
}

# ── Column definitions: (css-class, header label, % of zone width) ────────────
COLUMNS = [
    ('col-ab',    'Batter',  22),
    ('col-p',     'Pitches', 15),
    ('col-plate', 'Plate',   12),
    ('col-b',     '1B',      12),
    ('col-b',     '2B',      12),
    ('col-b',     '3B',      12),
    ('col-home',  'HOME',    15),
]

# ── Layout constants ───────────────────────────────────────────────────────────
GAP_IN            = 0.25   # gap between the two zones (inches)
PX_PER_IN         = 96     # CSS reference pixels per inch
TOPLINE_HEIGHT_PX = 36     # topline div + margin-bottom (approximate)
THEAD_HEIGHT_PX   = 16     # single header row


def in_to_mm(inches):
    return inches * 25.4

def mm_to_px(mm):
    return mm / 25.4 * PX_PER_IN

def calculate_rows(page_h_mm, margin_mm, row_height_px):
    usable_px    = mm_to_px(page_h_mm - 2 * margin_mm)
    overhead_px  = TOPLINE_HEIGHT_PX + THEAD_HEIGHT_PX
    return math.floor((usable_px - overhead_px) / row_height_px)


def build_html(size, orientation, margin_in, row_height_px):
    pw_mm, ph_mm = PAGE_SIZES[size]
    if orientation == 'landscape':
        pw_mm, ph_mm = ph_mm, pw_mm

    margin_mm = in_to_mm(margin_in)
    rows      = calculate_rows(ph_mm, margin_mm, row_height_px)

    # ── CSS column rules (percentages, one rule per unique class) ─────────────
    seen = {}
    col_rules = []
    for cls, _, pct in COLUMNS:
        if cls not in seen:
            col_rules.append(f'  .{cls} {{ width: {pct}%; }}')
            seen[cls] = True
    col_css = '\n'.join(col_rules)

    # ── Table markup ──────────────────────────────────────────────────────────
    header_cells = ''.join(f'<th class="{cls}">{lbl}</th>' for cls, lbl, _ in COLUMNS)
    empty_cells  = ''.join('<td><div></div></td>' for _ in COLUMNS)
    data_row     = f'        <tr>{empty_cells}</tr>'
    tbody_rows   = '\n'.join(data_row for _ in range(rows))

    table = f'''\
    <table>
      <thead><tr>{header_cells}</tr></thead>
      <tbody>
{tbody_rows}
      </tbody>
    </table>'''

    # ── Page content (topline + two zones) ────────────────────────────────────
    page_block = f'''\
<div class="topline">
  <div class="header-field fixed-md"><label>AWAY</label><div class="underline"></div></div>
  <div class="header-field fixed-sm"><label>PITCHER</label><div class="underline"></div></div>
  <div class="game-details">
    <div class="header-field fixed-md"><label>DATE</label><div class="underline"></div></div>
    <div class="header-field fixed-sm"><label>FIELD</label><div class="underline"></div></div>
  </div>
  <div class="header-field fixed-sm"><label>PITCHER</label><div class="underline"></div></div>
  <div class="header-field fixed-md"><label>HOME</label><div class="underline"></div></div>
</div>
<div class="page">
  <div class="zone">
{table}
  </div>
  <div class="zone">
{table}
  </div>
</div>'''

    # ── Full HTML ──────────────────────────────────────────────────────────────
    html = f'''\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>10U Softball Scoresheet</title>
<style>
  @page {{ size: {size} {orientation}; margin: {margin_in}in; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: monospace;
    font-size: 8pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  /* ── Top line ── */
  .topline {{
    display: flex;
    align-items: flex-end;
    margin-bottom: 8px;
    gap: 0.15in;
  }}
  .topline .game-details {{
    display: flex;
    flex: 1;
    justify-content: center;
    gap: 0.2in;
    align-items: flex-end;
  }}
  .header-field {{ display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }}
  .header-field label {{ font-weight: bold; font-size: 7pt; color: #444; letter-spacing: 0.5px; }}
  .header-field .underline {{ border-bottom: 0.75pt solid #333; height: 14px; }}
  .header-field.fixed-sm .underline {{ width: 0.9in; }}
  .header-field.fixed-md .underline {{ width: 1.4in; }}
  .fillline {{
    display: inline-block;
    border-bottom: 0.75pt solid #333;
    vertical-align: baseline;
    margin-left: 3px;
  }}
  .fillline.short {{ width: 0.8in; }}

  /* ── Grids ── */
  .page  {{ display: flex; gap: {GAP_IN}in; width: 100%; }}
  .zone  {{ flex: 1; min-width: 0; }}
  table  {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}

  /* Column widths (% of zone) */
{col_css}

  th, td {{ border: 0.5pt solid #666; padding: 0; overflow: hidden; white-space: nowrap; }}
  td div  {{ height: {row_height_px}px; line-height: {row_height_px}px; }}
  th {{
    height: 16px;
    line-height: 16px;
    text-align: center;
    font-size: 7pt;
    font-weight: bold;
    background: #ccc;
  }}
  th.col-ab {{ text-align: left; padding-left: 3px; }}
  th.col-p  {{ text-align: left; padding-left: 3px; }}
  tr:nth-child(5n) td {{ background-color: #e8e8e8; }}

  .page-break {{ page-break-after: always; }}
</style>
</head>
<body>

{page_block}

<div class="page-break"></div>

{page_block}

</body>
</html>
'''
    return html, rows


def main():
    parser = argparse.ArgumentParser(description='Generate 10U softball scoresheet')
    parser.add_argument('--size',        choices=list(PAGE_SIZES.keys()), default='letter')
    parser.add_argument('--orientation', choices=['landscape', 'portrait'],  default='landscape')
    parser.add_argument('--margin',      type=float, default=0.4,  help='Margin in inches')
    parser.add_argument('--row-height',  type=int,   default=24,   help='Row height in px')
    args = parser.parse_args()

    html, rows = build_html(args.size, args.orientation, args.margin, args.row_height)

    outdir   = os.path.dirname(os.path.abspath(__file__))
    filename = f'scoresheet_{args.size}_{args.orientation}.html'
    outpath  = os.path.join(outdir, filename)

    with open(outpath, 'w') as f:
        f.write(html)

    print(f'Generated {filename}  ({rows} rows per zone)')


if __name__ == '__main__':
    main()
