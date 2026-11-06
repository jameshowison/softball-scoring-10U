#!/usr/bin/env python3
"""
Generate 10U softball scoresheet HTML.

Usage:
    python3 generate_scoresheet.py --size letter --orientation landscape
    python3 generate_scoresheet.py --size letter --orientation portrait
    python3 generate_scoresheet.py --size a4 --orientation portrait
    python3 generate_scoresheet.py --layout batter-rows --orientation landscape
    python3 generate_scoresheet.py --layout tracks --orientation landscape
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
    ('col-b1',    '1B',      12),
    ('col-b2',    '2B',      12),
    ('col-b3',    '3B',      12),
    ('col-home',  'HOME',    15),
]

# 2-up-landscape: narrow base cols, HOME = 2× 1B
COLUMNS_2UP = [
    ('col-ab',    'Batter',  28),
    ('col-p',     'Pitches', 22),
    ('col-plate', 'Plate',   14),
    ('col-b1',    '1B',       8),
    ('col-b2',    '2B',       8),
    ('col-b3',    '3B',       8),
    ('col-home',  'HOME',    12),
]

# tracks: one row per action, slightly taller rows; the batter's first row holds
# every pitch of the at-bat on two tracks (strikes above, balls below), so the
# Pitches column is wider. Runner-action rows leave Plate blank; p / w / s are
# written on the runner's line.
COLUMNS_TRACKS = [
    ('col-ab',    'Batter',  18),
    ('col-p',     'Pitches', 26),
    ('col-plate', 'Plate',   12),
    ('col-b1',    '1B',      10),
    ('col-b2',    '2B',      10),
    ('col-b3',    '3B',      10),
    ('col-home',  'HOME',    14),
]
TRACKS_ROW_PX = 30

# ── Layout constants ───────────────────────────────────────────────────────────
GAP_IN            = 0.125  # gap between zones within a mini-page (inches)
PAGE_GAP_IN       = 0.175  # gap between the two mini-pages in 2-up layout
PX_PER_IN         = 96     # CSS reference pixels per inch
TOPLINE_HEIGHT_PX    = 36  # topline div + margin-bottom (approximate)
TOPLINE_2UP_HEIGHT_PX = 48 # 2-up topline (~2 scoring rows)
THEAD_HEIGHT_PX      = 16  # single header row


def in_to_mm(inches):
    return inches * 25.4

def mm_to_px(mm):
    return mm / 25.4 * PX_PER_IN

# Measured in Chrome: the standard topline renders 51px + 6px margin, the header
# row 18px, and each body row prints ~1px taller than its div (cell borders).
STD_TOPLINE_PX = 57
STD_THEAD_PX   = 18

def calculate_rows(page_h_mm, margin_mm, row_height_px):
    usable_px    = mm_to_px(page_h_mm - 2 * margin_mm)
    overhead_px  = STD_TOPLINE_PX + STD_THEAD_PX
    return math.floor((usable_px - overhead_px) / (row_height_px + 1))


def build_html(size, orientation, margin_in, row_height_px, layout='standard'):
    columns = {'2up-landscape': COLUMNS_2UP, 'tracks': COLUMNS_TRACKS}.get(layout, COLUMNS)

    if layout == '2up-landscape':
        orientation = 'landscape'

    pw_mm, ph_mm = PAGE_SIZES[size]
    if orientation == 'landscape':
        pw_mm, ph_mm = ph_mm, pw_mm

    margin_mm = in_to_mm(margin_in)

    if layout == '2up-landscape':
        usable_px = mm_to_px(ph_mm - 2 * margin_mm)
        # subtract 2 rows as buffer — borders/rendering eat the theoretical 3px headroom
        rows = math.floor((usable_px - TOPLINE_2UP_HEIGHT_PX - THEAD_HEIGHT_PX) / row_height_px) - 2
    else:
        rows = calculate_rows(ph_mm, margin_mm, row_height_px)

    # ── CSS column rules (percentages, one rule per unique class) ─────────────
    seen = {}
    col_rules = []
    for cls, _, pct in columns:
        if cls not in seen:
            col_rules.append(f'  .{cls} {{ width: {pct}%; }}')
            seen[cls] = True
    col_css = '\n'.join(col_rules)

    # ── Table markup ──────────────────────────────────────────────────────────
    def header_label(cls, lbl):
        if layout == 'tracks' and cls == 'col-p':
            return 'Pitches <span class="hint">&#9650;strikes &#9660;balls</span>'
        return lbl
    header_cells = ''.join(f'<th class="{cls}">{header_label(cls, lbl)}</th>' for cls, lbl, _ in columns)
    def empty_cell(cls):
        if layout == 'tracks' and cls == 'col-p':
            return '<td class="col-p"><div class="trk trk-s"></div><div class="trk trk-b"></div></td>'
        return f'<td class="{cls}"><div></div></td>'
    empty_cells  = ''.join(empty_cell(cls) for cls, _, _ in columns)
    data_row     = f'        <tr>{empty_cells}</tr>'
    tbody_rows   = '\n'.join(data_row for _ in range(rows))

    table = f'''\
    <table>
      <thead><tr>{header_cells}</tr></thead>
      <tbody>
{tbody_rows}
      </tbody>
    </table>'''

    # ── Page content ──────────────────────────────────────────────────────────
    bs_2up_h = (TOPLINE_2UP_HEIGHT_PX - 10) // 2  # box-score row height inside 2up topline
    if layout == '2up-landscape':
        page_block = f'''\
<div class="topline-2up">
  <div class="tl2-half">
    <div class="tl2-field"><label>AWAY TEAM</label><div class="tl2-underline"></div></div>
    <div class="tl2-field"><label>PITCHER</label><div class="tl2-underline"></div></div>
    <div class="tl2-field tl2-narrow"><label>DATE</label><div class="tl2-underline"></div></div>
    <div class="tl2-field tl2-narrow"><label>FIELD</label><div class="tl2-underline"></div></div>
  </div>
  <div class="tl2-half">
    <div class="tl2-field"><label>HOME TEAM</label><div class="tl2-underline"></div></div>
    <div class="tl2-field"><label>PITCHER</label><div class="tl2-underline"></div></div>
    <div class="tl2-bs-outer">
      <div class="tl2-bs-labels"><div>Away</div><div>Home</div></div>
      <div class="tl2-bs-wrap">
        <table class="bs-table-2"><tbody>
          <tr><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td></tr>
          <tr><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td><td class="bs-cell-2"></td></tr>
        </tbody></table>
      </div>
    </div>
  </div>
</div>
<div class="page-2up">
  <div class="mini-page">
    <div class="zone">
{table}
    </div>
    <div class="zone">
{table}
    </div>
  </div>
  <div class="mini-page">
    <div class="zone">
{table}
    </div>
    <div class="zone">
{table}
    </div>
  </div>
</div>'''
    else:
        page_block = f'''\
<div class="topline">
  <div class="topline-zone">
    <div class="tl-col-batter">
      <div class="tl-field"><label>AWAY TEAM</label><div class="underline"></div></div>
    </div>
    <div class="tl-col-pitches">
      <div class="tl-field"><label>PITCHER</label><div class="underline"></div></div>
    </div>
    <div class="tl-skip"></div>
    <div class="tl-df-block">
      <div class="tl-field"><label>DATE</label><div class="underline"></div></div>
      <div class="tl-field"><label>FIELD</label><div class="underline"></div></div>
    </div>
  </div>
  <div class="topline-zone">
    <div class="tl-col-batter">
      <div class="tl-field"><label>HOME TEAM</label><div class="underline"></div></div>
    </div>
    <div class="tl-col-pitches">
      <div class="tl-field"><label>PITCHER</label><div class="underline"></div></div>
    </div>
    <div class="tl-skip"></div>
    <div class="tl-box-score">
      <table class="bs-table"><tbody>
        <tr><td class="bs-label">Away</td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td></tr>
        <tr><td class="bs-label">Home</td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td><td class="bs-cell"><div class="bs-inner"></div></td></tr>
      </tbody></table>
    </div>
  </div>
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
    if layout == '2up-landscape':
        extra_css = f'''\
  /* ── 2-up topline ── */
  .topline-2up   {{ display: flex; gap: {PAGE_GAP_IN}in; height: {TOPLINE_2UP_HEIGHT_PX}px; margin-bottom: 3px; padding-right: 2px; }}
  .tl2-half      {{ flex: 1; min-width: 0; display: flex; gap: 0.05in; align-items: stretch; }}
  .tl2-field     {{ flex: 1; min-width: 0; display: flex; flex-direction: column; }}
  .tl2-field label {{ font-weight: bold; font-size: 7pt; color: #444; letter-spacing: 0.5px; white-space: nowrap; padding-top: 2px; }}
  .tl2-underline {{ border-bottom: 0.75pt solid #333; flex: 0 0 {TOPLINE_2UP_HEIGHT_PX // 2}px; }}
  .tl2-narrow    {{ flex: 0 0 13%; }}
  .tl2-bs-outer  {{ flex: 0 0 34%; display: flex; gap: 3px; align-items: stretch; }}
  .tl2-bs-labels {{ display: flex; flex-direction: column; justify-content: space-around; font-size: 7pt; font-weight: bold; color: #444; white-space: nowrap; }}
  .tl2-bs-wrap   {{ flex: 1; }}
  .bs-table-2    {{ border-collapse: collapse; table-layout: fixed; width: 100%; height: 100%; }}
  .bs-cell-2     {{ border: 0.5pt solid #888; padding: 0; }}
  /* ── 2-up grid ── */
  .page-2up  {{ display: flex; gap: {PAGE_GAP_IN}in; width: 100%; padding-right: 1pt; }}
  .mini-page {{ flex: 1; min-width: 0; display: flex; gap: {GAP_IN}in; }}'''
    else:
        extra_css = f'''\
  /* ── Top line ── */
  .topline {{ display: flex; gap: {GAP_IN}in; margin-bottom: 6px; }}
  .topline-zone {{ flex: 1; min-width: 0; display: flex; align-items: stretch; }}
  /* each column slot matches the table column widths */
  .tl-col-batter  {{ width: 22%; flex-shrink: 0; padding-right: 0.04in; display: flex; }}
  .tl-col-pitches {{ width: 15%; flex-shrink: 0; padding-right: 0.04in; display: flex; }}
  /* Plate(12%) + 1B(12%) = 24% — empty spacer in left zone */
  .tl-skip {{ width: 24%; flex-shrink: 0; }}
  /* 2B+3B+HOME = 39% — date/field in left zone */
  .tl-df-block {{ width: 39%; flex-shrink: 0; display: flex; align-items: stretch; gap: 0.1in; }}
  /* remaining right zone space — box score (same flex technique as .zone) */
  .tl-box-score {{ flex: 1; min-width: 0; padding-right: 1pt; padding-top: 6px; }}
  .tl-field {{ display: flex; flex-direction: column; justify-content: space-between; flex: 1; min-width: 0; }}
  .tl-field label {{ font-weight: bold; font-size: 7pt; color: #444; letter-spacing: 0.5px; white-space: nowrap; padding-top: 6px; }}
  .tl-field .underline {{ border-bottom: 0.75pt solid #333; height: 14px; }}
  /* ── Box score — fixed layout + percentage widths, matching main table ── */
  .bs-table {{ border-collapse: collapse; table-layout: fixed; width: calc(100% - 2pt); }}
  .bs-label {{ width: 26%; font-size: 7pt; font-weight: bold; color: #444; padding-right: 3px; white-space: nowrap; border: none; text-align: right; vertical-align: middle; }}
  .bs-cell {{ border: 0.5pt solid #666; padding: 0; }}
  .bs-inner {{ height: {min(row_height_px, 24) - 3}px; line-height: {min(row_height_px, 24) - 3}px; display: block; }}
  /* ── Standard grid ── */
  .page  {{ display: flex; gap: {GAP_IN}in; width: 100%; padding-right: 1pt; }}'''

    tracks_css = ''
    if layout == 'tracks':
        tracks_css = f'''\
  /* pitches on two tracks: strikes & fouls above the line, balls below */
  td.col-p .trk   {{ height: {row_height_px / 2}px; line-height: {row_height_px / 2}px; }}
  td.col-p .trk-s {{ border-bottom: 0.5pt dashed #999; }}
  th .hint {{ font-weight: normal; font-size: 6pt; color: #444; }}
'''

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

{extra_css}

  /* ── Shared grid ── */
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
  td.col-b1, td.col-b3 {{ background-color: #f0f0f0; }}
  tr:nth-child(5n) td {{ background-color: #e8e8e8; }}

{tracks_css}  .page-break {{ page-break-after: always; }}
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


# ── Batter-rows layout: one row per plate appearance, three event sub-rows ────
# Each batter row is split into three sub-rows, used top to bottom as events
# happen during the at-bat. The Result column carries the same three slots:
# the top two for runner events (p w s E4 ...), the bottom one always for the
# batter's result (x1, BB, K ...). Pitches span the whole row on two tracks:
# strikes/fouls above the line, balls below. Runners are drawn diagonally from
# base to base as in the standard sheet, crossing sub-row and row boundaries.
COLUMNS_BATTER_ROWS = [
    # cls,          label,     landscape %, portrait %
    ('col-ab',     'Batter',       17, 17),
    ('col-p',      'Pitches',      34, 36),
    ('col-plate',  'Result',       13, 11),
    ('col-b1',     '1B',            9,  9),
    ('col-b2',     '2B',            9,  9),
    ('col-b3',     '3B',            9,  9),
    ('col-home',   'H',             9,  9),
]
SUBROW_PX = 16
SUBROW_COLS = ('col-plate', 'col-b1', 'col-b2', 'col-b3', 'col-home')


def build_batter_rows_html(size, orientation, margin_in, sub_px=SUBROW_PX):
    pw_mm, ph_mm = PAGE_SIZES[size]
    if orientation == 'landscape':
        pw_mm, ph_mm = ph_mm, pw_mm
    margin_mm = in_to_mm(margin_in)

    row_px     = sub_px * 3
    topline_px = 40   # page line (date / field / legend / box score)
    zonehdr_px = 22   # per-zone TEAM / PITCHER line
    usable_px  = mm_to_px(ph_mm - 2 * margin_mm)
    rows = math.floor((usable_px - topline_px - zonehdr_px - THEAD_HEIGHT_PX - 12) / row_px)

    pct_idx = 2 if orientation == 'landscape' else 3
    col_css = '\n'.join(f'  .{c[0]} {{ width: {c[pct_idx]}%; }}' for c in COLUMNS_BATTER_ROWS)

    def cell(cls):
        if cls == 'col-ab':
            return '<td class="col-ab"><div class="tall"></div></td>'
        if cls == 'col-p':
            return '<td class="col-p"><div class="trk trk-s"></div><div class="trk trk-b"></div></td>'
        subs = '<div class="sub"></div><div class="sub"></div><div class="sub sub-res"></div>'
        return f'<td class="{cls}">{subs}</td>'

    cells = ''.join(cell(c[0]) for c in COLUMNS_BATTER_ROWS)
    labels = {'col-p': 'Pitches <span class="hint">strikes &#9650; &middot; balls &#9660;</span>'}
    header = ''.join(f'<th class="{c[0]}">{labels.get(c[0], c[1])}</th>' for c in COLUMNS_BATTER_ROWS)
    body = '\n'.join(f'        <tr>{cells}</tr>' for _ in range(rows))

    def zone(team):
        return (
            '  <div class="zone">\n'
            '    <div class="zonehdr">\n'
            f'      <div class="zf zf-team"><label>{team}</label><div class="ul"></div></div>\n'
            '      <div class="zf"><label>PITCHER</label><div class="ul"></div></div>\n'
            '    </div>\n'
            '    <table>\n'
            f'      <thead><tr>{header}</tr></thead>\n'
            f'      <tbody>\n{body}\n      </tbody>\n'
            '    </table>\n'
            '  </div>'
        )

    def bs_row(lbl):
        return f'<tr><td class="bs-label">{lbl}</td>' + '<td class="bs-cell"></td>' * 7 + '</tr>'

    topline = (
        '<div class="br-top">\n'
        '  <div class="zf zf-narrow"><label>DATE</label><div class="ul"></div></div>\n'
        '  <div class="zf"><label>FIELD</label><div class="ul"></div></div>\n'
        '  <div class="legend">Sub-rows = events in order. Result: runner events (p w s E4) top, '
        'batter result (x1 BB K) bottom.<br>'
        'Runners: diagonal base to base on the event&rsquo;s sub-row &middot; circle outs &middot; R# in H</div>\n'
        f'  <table class="bs-table"><tbody>{bs_row("Away")}{bs_row("Home")}</tbody></table>\n'
        '</div>'
    )

    if orientation == 'landscape':
        page = f'{topline}\n<div class="page">\n{zone("AWAY TEAM")}\n{zone("HOME TEAM")}\n</div>'
        pages = f'{page}\n<div class="page-break"></div>\n{page}'
    else:
        pa = f'{topline}\n<div class="page">\n{zone("AWAY TEAM")}\n</div>'
        ph = f'{topline}\n<div class="page">\n{zone("HOME TEAM")}\n</div>'
        pages = f'{pa}\n<div class="page-break"></div>\n{ph}'

    css = f'''\
  @page {{ size: {size} {orientation}; margin: {margin_in}in; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: monospace; font-size: 8pt;
          -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

  /* ── page top line ── */
  .br-top {{ display: flex; gap: 0.12in; align-items: flex-end; height: {topline_px}px; margin-bottom: 4px; }}
  .zf {{ flex: 1; min-width: 0; display: flex; flex-direction: column; }}
  .zf label {{ font-weight: bold; font-size: 7pt; color: #444; letter-spacing: 0.5px; white-space: nowrap; }}
  .zf .ul {{ border-bottom: 0.75pt solid #333; height: 14px; }}
  .zf-narrow {{ flex: 0 0 10%; }}
  .legend {{ flex: 0 0 40%; font-size: 6pt; color: #555; line-height: 1.3; font-family: sans-serif; }}
  .bs-table {{ flex: 0 0 24%; border-collapse: collapse; table-layout: fixed; }}
  .bs-label {{ width: 14%; font-size: 7pt; font-weight: bold; color: #444; text-align: right;
               padding-right: 3px; border: none; }}
  .bs-cell  {{ border: 0.5pt solid #888; height: 17px; }}

  /* ── zones ── */
  .page  {{ display: flex; gap: {GAP_IN * 1.5}in; width: 100%; padding-right: 1pt; }}
  .zone  {{ flex: 1; min-width: 0; }}
  .zonehdr {{ display: flex; gap: 0.12in; height: {zonehdr_px}px; margin-bottom: 2px; }}
  .zf-team {{ flex: 1.4; }}

  table  {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
{col_css}

  th, td {{ border: 0.5pt solid #666; padding: 0; overflow: hidden; white-space: nowrap; }}
  tbody td {{ border-bottom: 1pt solid #333; }}
  th {{ height: {THEAD_HEIGHT_PX}px; line-height: {THEAD_HEIGHT_PX}px; font-size: 7pt; font-weight: bold;
        background: #ccc; text-align: left; padding-left: 3px; }}
  th .hint {{ font-weight: normal; font-size: 6pt; color: #444; }}
  .tall {{ height: {row_px}px; }}

  /* pitches: two tracks — strikes & fouls above the line, balls below */
  .trk   {{ height: {row_px // 2}px; }}
  .trk-s {{ border-bottom: 0.5pt dashed #999; }}

  /* event sub-rows */
  .sub {{ height: {sub_px}px; position: relative; }}
  .sub + .sub {{ border-top: 0.5pt dotted #aaa; }}
  td.col-plate .sub-res {{ border-top: 0.5pt solid #888; }}
  td.col-b1, td.col-b3 {{ background-color: #f0f0f0; }}
  td.col-home {{ background-color: #f7f7f7; }}

  .page-break {{ page-break-after: always; }}'''

    html = (
        '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n'
        '<title>10U Softball Scoresheet — Batter Rows</title>\n'
        f'<style>\n{css}\n</style>\n</head>\n<body>\n\n{pages}\n\n</body>\n</html>\n'
    )
    return html, rows


def main():
    parser = argparse.ArgumentParser(description='Generate 10U softball scoresheet')
    parser.add_argument('--size',        choices=list(PAGE_SIZES.keys()), default='letter')
    parser.add_argument('--orientation', choices=['landscape', 'portrait'],  default='landscape')
    parser.add_argument('--layout',      choices=['standard', '2up-landscape', 'batter-rows', 'tracks'], default='standard')
    parser.add_argument('--margin',      type=float, default=0.4,  help='Margin in inches')
    parser.add_argument('--row-height',  type=int,   default=None, help='Row height in px (default 24; 30 for tracks)')
    args = parser.parse_args()

    if args.layout == 'batter-rows':
        html, rows = build_batter_rows_html(args.size, args.orientation, args.margin)
    else:
        row_h = args.row_height or (TRACKS_ROW_PX if args.layout == 'tracks' else 24)
        html, rows = build_html(args.size, args.orientation, args.margin, row_h, args.layout)

    outdir   = os.path.dirname(os.path.abspath(__file__))
    if args.layout == '2up-landscape':
        filename = f'scoresheet_{args.size}_2up_landscape.html'
    elif args.layout == 'tracks':
        filename = f'scoresheet_{args.size}_tracks_{args.orientation}.html'
    elif args.layout == 'batter-rows':
        filename = f'scoresheet_{args.size}_batter_rows_{args.orientation}.html'
    else:
        filename = f'scoresheet_{args.size}_{args.orientation}.html'
    outpath  = os.path.join(outdir, filename)

    with open(outpath, 'w') as f:
        f.write(html)

    print(f'Generated {filename}  ({rows} rows per zone)')


if __name__ == '__main__':
    main()
