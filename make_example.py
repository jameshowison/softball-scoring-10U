#!/usr/bin/env python3
"""
Build the worked example for the tracks layout: a filled-in sheet with one
inning per team, drawn in "pen" over the real generated scoresheet.

Usage:
    python3 make_example.py            # writes example_tracks.html and example_tracks.png

The PNG is rendered with headless Chrome (path below); if Chrome isn't found,
open example_tracks.html in a browser instead.

Drawing conventions shown (see README, "Tracks variant"):
  - All of a batter's pitches go on their first row: strikes above the dashed
    line, balls below.
  - Plate holds only the batter's own result (x1, BB, circled outs).
    Runner actions (p, w, s) are written on the runner's line.
  - A runner leaves a base near the TOP of a row and arrives near the BOTTOM,
    so each move is a diagonal inside the row where it happened. Holding a base
    is a straight vertical line.
  - A dot marks each occupied base at the start of a new at-bat.
  - An L marks the continuation rows of an at-bat that runs over several rows.
"""

import json
import os
import re
import subprocess

import generate_scoresheet as g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, 'example_tracks.html')
OUT_PNG = os.path.join(HERE, 'example_tracks.png')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
INK = '#1a3fa0'
STRIKES = set("/'-")


def circ(text):
    """An out: circled."""
    return f'<span class="circ">{text}</span>'


# ── The game ──────────────────────────────────────────────────────────────────
# Each row: (batter, pitches, plate, {base_col: text}, inning_end)
#   batter/pitches only on an at-bat's first row; base_col 1-3 = 1B-3B, 4 = HOME.
# Each runner: on = row they reached 1B from Plate;
#   moves = [row, to_col, label, 'out'?]; through = last row to keep them on base.
# at_bats = (first row, last row).

AWAY = {
    'rows': [
        ('Ava #7', "./x",   'x1',        {},                 False),  # 0
        ('Bea #4', "..'..", '',          {},                 False),  # 1  Ava steals 2nd
        ('',       '',      'BB',        {},                 False),  # 2
        ('Cat #6', ".-/x",  '',          {},                 False),  # 3  passed ball
        ('',       '',      'x1',        {4: 'R1'},          False),  # 4
        ('Deb #8', "./.x",  '',          {4: 'R2'},          False),  # 5  wild pitch
        ('',       '',      circ('F8'),  {},                 False),  # 6
        ('Eve #2', "''/",   '',          {},                 False),  # 7  Cat steals 3rd
        ('',       '',      circ('K'),   {},                 False),  # 8
        ('Fay #5', ".x",    '',          {1: circ('6-3')},   True),   # 9  Cat stranded
        ('Gia #9', "....",  'BB',        {},                 False),  # 10
        ('Hal #3', ".'.",   '',          {2: circ('CS')},    False),  # 11 Gia caught stealing
    ],
    'runners': [
        {'on': 0,  'moves': [[1, 2, 's'], [3, 3, 'p'], [4, 4]]},              # Ava
        {'on': 2,  'moves': [[3, 2, 'p'], [4, 3], [5, 4, 'w']]},              # Bea
        {'on': 4,  'moves': [[5, 2, 'w'], [7, 3, 's']], 'through': 9},        # Cat
        {'on': 10, 'moves': [[11, 2, 's', 'out']]},                           # Gia
    ],
    'at_bats': [(0, 0), (1, 2), (3, 4), (5, 6), (7, 8), (9, 9), (10, 10), (11, 11)],
}

HOME = {
    'rows': [
        ('Ivy #1', "....",  'BB',        {},                 False),  # 0
        ('Jo #2',  "..'..", 'BB',        {},                 False),  # 1
        ('Kim #3', ".-...", 'BB',        {},                 False),  # 2
        ('Lu #4',  "....",  'BB',        {4: 'R1'},          False),  # 3  run forced in
        ('Mae #5', "./'x",  '',          {4: 'R2'},          False),  # 4  Jo steals home
        ('',       '',      circ('F7'),  {},                 False),  # 5
        ('Nia #6', "..'//", '',          {},                 False),  # 6  passed ball
        ('',       '',      '',          {4: 'R3'},          False),  # 7  wild pitch
        ('',       '',      circ('K'),   {},                 False),  # 8
        ('Ola #7', "x",     '',          {1: circ('4-3')},   True),   # 9  Lu stranded
    ],
    'runners': [
        {'on': 0, 'moves': [[1, 2], [2, 3], [3, 4]]},                         # Ivy (forced home)
        {'on': 1, 'moves': [[2, 2], [3, 3], [4, 4, 's']]},                    # Jo (steals home)
        {'on': 2, 'moves': [[3, 2], [6, 3, 'p'], [7, 4, 'w']]},               # Kim
        {'on': 3, 'moves': [[6, 2, 'p'], [7, 3, 'w']], 'through': 9},         # Lu (stranded)
    ],
    'at_bats': [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 8), (9, 9)],
}


# ── HTML for filled rows ──────────────────────────────────────────────────────
def pitches_cell(seq):
    top = ''.join(f'<i>{c if c in STRIKES else "&nbsp;"}</i>' for c in seq)
    bot = ''.join(f'<i>{"&nbsp;" if c in STRIKES else c}</i>' for c in seq)
    return (f'<td class="col-p"><div class="trk trk-s ink">{top}</div>'
            f'<div class="trk trk-b ink">{bot}</div></td>')


def row_html(batter, seq, plate, marks, end):
    tds = [f'<td class="col-ab"><div class="ink name">{batter}</div></td>',
           pitches_cell(seq),
           f'<td class="col-plate"><div class="ink mk">{plate}</div></td>']
    for i, cls in enumerate(['col-b1', 'col-b2', 'col-b3', 'col-home'], start=1):
        tds.append(f'<td class="{cls}"><div class="ink mk">{marks.get(i, "")}</div></td>')
    attr = ' class="inning-end"' if end else ''
    return f'        <tr{attr}>{"".join(tds)}</tr>'


def fill_zone(html, zone_index, rows):
    """Replace the first len(rows) body rows of the given scoring table."""
    starts = [m.end() for m in re.finditer(r'      <tbody>\n', html)]
    i = starts[zone_index]
    lines = html[i:].split('\n')
    for n, r in enumerate(rows):
        lines[n] = row_html(*r)
    return html[:i] + '\n'.join(lines)


CSS = f'''
  .ink {{ font-family: "Bradley Hand", "Comic Sans MS", cursive; color: {INK}; font-size: 10.5pt; font-weight: bold; }}
  .name {{ padding-left: 4px; }}
  .mk   {{ padding-left: 5px; }}
  td.col-home .mk {{ padding-left: 40%; }}
  td.col-b1 .mk, td.col-b2 .mk {{ padding-left: 22%; }}
  .trk.ink {{ padding-left: 4px; font-size: 12pt; }}
  .trk i {{ display: inline-block; width: 10px; font-style: normal; text-align: center; }}
  .circ {{ border: 1.2pt solid {INK}; border-radius: 50%; padding: 0 4px; line-height: 14px;
           display: inline-block; background: #fff; position: relative; z-index: 3; }}
  tr.inning-end td {{ border-bottom: 3pt double #333; }}
  svg text.cause {{ font-family: "Bradley Hand", cursive; font-weight: bold; font-size: 10.5pt; fill: {INK};
                    paint-order: stroke; stroke: #fff; stroke-width: 3px; }}
  svg.overlay {{ position: absolute; left: 0; top: 0; pointer-events: none; }}
'''

# Pen strokes are drawn in the browser from the real cell positions.
DRAW_JS = r'''
const COLS = ["col-plate", "col-b1", "col-b2", "col-b3", "col-home"];
const TOP = 0.28, LOW = 0.72;   // leave a base near the top of a row, arrive near the bottom
const svgns = 'http://www.w3.org/2000/svg';
const svg = document.createElementNS(svgns, 'svg');
svg.setAttribute('class', 'overlay');
svg.setAttribute('width', document.body.scrollWidth);
svg.setAttribute('height', document.body.scrollHeight);
svg.innerHTML = '<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">'
  + '<path d="M0,0 L7,3.5 L0,7 z" fill="' + INK + '"/></marker></defs>';
document.body.appendChild(svg);
const sx = window.scrollX, sy = window.scrollY;
function el(tag, attrs) {
  const e = document.createElementNS(svgns, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  svg.appendChild(e); return e;
}
const tbodies = document.querySelectorAll('.zone tbody');
ZONES.forEach((z, zi) => {
  const trs = tbodies[zi].children;
  const pt = (r, col, frac) => {
    const d = trs[r].querySelector('td.' + COLS[col]).getBoundingClientRect();
    const x = col === 0 ? d.right - 6 : d.left + d.width * (col === 4 ? 0.25 : 0.5);
    return [x + sx, d.top + d.height * frac + sy];
  };
  const line = ([x1, y1], [x2, y2], arrow) => el('line', Object.assign(
    { x1, y1, x2, y2, stroke: INK, 'stroke-width': 1.5 }, arrow ? { 'marker-end': 'url(#ah)' } : {}));
  const starts = new Set(z.at_bats.map(([a]) => a));
  // L on the continuation rows of multi-row at-bats
  const pc = trs[0].querySelector('td.col-p').getBoundingClientRect();
  z.at_bats.filter(([a, b]) => b > a).forEach(([a, b]) => {
    const top = trs[a + 1].getBoundingClientRect().top + 3 + sy;
    const bot = trs[b].getBoundingClientRect().bottom - 2 + sy;
    const x0 = pc.left + 1 + sx, x1 = pc.left + pc.width * 0.6 + sx;
    el('polyline', { points: `${x0},${top} ${x0},${bot} ${x1},${bot}`, fill: 'none',
                     stroke: INK, 'stroke-width': 1.8, 'stroke-linecap': 'round' });
  });
  z.runners.forEach(rn => {
    let row = rn.on, col = 1, cur = pt(row, 1, LOW);
    line(pt(row, 0, LOW), cur, true);               // batter reaches 1B
    const holdTo = r => {                           // stay on base down to row r
      for (let rr = row + 1; rr <= r; rr++) {
        const nxt = pt(rr, col, TOP);
        line(cur, nxt, false);
        if (starts.has(rr)) el('circle', { cx: nxt[0], cy: nxt[1], r: 3.2, fill: INK });
        cur = nxt;
      }
      row = r;
    };
    rn.moves.forEach(([r, c, lbl, out]) => {
      holdTo(r);
      const to = pt(r, c, LOW);
      line(cur, to, !out);
      if (lbl) el('text', { x: (cur[0] + to[0]) / 2 + 4, y: (cur[1] + to[1]) / 2 - 3, class: 'cause' })
                 .textContent = lbl;
      cur = to; col = c;
    });
    if (rn.through) holdTo(rn.through);
  });
});
'''


def build():
    html, _ = g.build_html('letter', 'landscape', 0.4, g.TRACKS_ROW_PX, 'tracks')
    html = fill_zone(html, 0, AWAY['rows'])
    html = fill_zone(html, 1, HOME['rows'])
    zones = [{k: z[k] for k in ('runners', 'at_bats')} for z in (AWAY, HOME)]
    script = (f'<script>\nconst INK = "{INK}";\nconst ZONES = {json.dumps(zones)};\n'
              f'{DRAW_JS}</script>\n')
    html = html.replace('</style>', CSS + '</style>', 1).replace('</body>', script + '</body>', 1)
    with open(OUT_HTML, 'w') as f:
        f.write(html)
    print(f'Wrote {os.path.basename(OUT_HTML)}')

    if os.path.exists(CHROME):
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--window-size=1056,560', '--force-device-scale-factor=2',
                        f'--screenshot={OUT_PNG}', f'file://{OUT_HTML}'],
                       check=True, capture_output=True)
        print(f'Wrote {os.path.basename(OUT_PNG)}')
    else:
        print('Chrome not found; open example_tracks.html in a browser to view.')


if __name__ == '__main__':
    build()
