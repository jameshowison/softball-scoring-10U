#!/usr/bin/env python3
"""
Build the small ink-style figures used in the README.

Usage:
    python3 make_readme_figures.py      # writes figures/<name>.png (needs Chrome)

Each figure is the top few rows of one team's tracks sheet, filled in "pen"
with the same drawing code as make_example.py (see that file and the README
for the conventions). Edit the FIGURES data below and rerun to change one.
"""

import json
import os
import re
import subprocess

import generate_scoresheet as g
from make_example import CHROME, CSS, DRAW_JS, INK, circ, fill_zone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, 'figures')
WIDTH = 620

# Data format is make_example.py's:
#   rows:    (batter, pitches, plate, {base_col: text}, inning_end)
#            base_col 1-3 = 1B-3B, 4 = HOME
#   runners: on = row the batter reached base; to = base reached (default 1B);
#            moves = [row, to_col, label, 'out' | 'join'?]; through = stranded, hold to that row
#   at_bats: (first row, last row)
#   summary: (row, text) written on that row's double line

FIGURES = {
    'first_inning': {
        'rows': [
            ('Ava #7', "..'//", 'K d3',      {},               False),
            ('Bea #4', "....",  'BB',        {},               False),
            ('Cat #6', "./x",   circ('F8'),  {},               False),
            ('Deb #8', "../",   circ('K'),   {},               False),
            ('Eve #2', "./x",   '',          {1: circ('4-3')}, True),
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2]], 'through': 4},   # Ava: safe on the dropped 3rd strike
            {'on': 1, 'moves': [], 'through': 4},         # Bea
        ],
        'at_bats': [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
        'summary': (4, 'O:3 H:0/0 R:0/0'),
    },
    'dropped_third': {
        'rows': [
            ('Bea #4', "''/",   circ('K d3'), {},               False),
            ('Cat #6', ".'-'",  'K d3',       {1: circ('2-3')}, False),
            ('Ava #7', "..'//", 'K d3',       {},               False),
        ],
        'runners': [
            {'on': 2, 'moves': []},
        ],
        'at_bats': [(0, 0), (1, 1), (2, 2)],
    },
    'home_run': {
        'rows': [
            ('Ava #7', ".x",   'x1', {},         False),
            ('Bea #4', "....", 'BB', {},         False),
            ('Cat #6', "/x",   'x4', {4: 'R1-3'}, False),
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2], [2, 2, '', 'join']]},   # Ava joins the batter's line in 2B
            {'on': 1, 'moves': [[2, 1, '', 'join']]},           # Bea joins it in 1B
            {'on': 2, 'to': 4, 'moves': []},
        ],
        'at_bats': [(0, 0), (1, 1), (2, 2)],
    },
    'passed_balls': {
        'rows': [
            ('Ava #7', "....",  'BB', {},        False),
            ('Bea #4', "././x", '',   {},        False),
            ('',       '',      '',   {},        False),
            ('',       '',      'x1', {4: 'R1'}, False),
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2, 'p'], [2, 3, 'p'], [3, 4]]},
            {'on': 3, 'moves': []},
        ],
        'at_bats': [(0, 0), (1, 3)],
    },
    'out_at_home': {
        'rows': [
            ('Ava #7', ".'/x",  'x3',       {},               False),
            ('Eve #2', "...'x", '',         {4: circ('2-1')}, False),
            ('',       '',      circ('F9'), {},               False),
        ],
        'runners': [
            {'on': 0, 'to': 3, 'moves': [[1, 4, 'w', 'out']]},
        ],
        'at_bats': [(0, 0), (1, 2)],
    },
    'chaos_inning': {
        'rows': [
            ('Ava #7', "....", 'BB', {},        False),
            ('Bea #4', "....", 'BB', {},        False),
            ('Cat #6', "....", 'BB', {},        False),
            ('Deb #8', "../x", 'x1', {4: 'R1'}, False),
            ('',       '',     '',   {4: 'R2'}, False),
            ('',       '',     '',   {4: 'R3'}, False),
            ('',       '',     '',   {4: 'R4'}, True),
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2], [2, 3], [3, 4]]},                         # Ava
            {'on': 1, 'moves': [[2, 2], [3, 3], [4, 4, 'e8']]},                   # Bea
            {'on': 2, 'moves': [[3, 2], [4, 3, 'e8'], [5, 4, 'e4']]},             # Cat
            {'on': 3, 'moves': [[4, 2, 'e8'], [5, 3, 'e4'], [6, 4, 'e1']]},       # Deb
        ],
        'at_bats': [(0, 0), (1, 1), (2, 2), (3, 6)],
        'summary': (6, 'O:0 H:1/1 R:4/4, RUN LIMIT'),
    },
    'medium_inning': {
        'rows': [
            ('Ava #7', "./x",    'x1', {},        False),  # 0
            ('Bea #4', "../'..", '',   {},        False),  # 1  Ava steals 2nd
            ('',       '',       'BB', {},        False),  # 2
            ('Cat #6', ".-/x",   '',   {},        False),  # 3  passed ball
            ('',       '',       'x1', {4: 'R1'}, False),  # 4
            ('Deb #8', "./x",    '',   {},        False),  # 5  passed ball
            ('',       '',       'x2', {4: 'R2'}, False),  # 6
            ('Eve #2', "..",     '',   {4: 'R3'}, False),  # 7  passed ball
            ('',       '',       '',   {4: 'R4'}, True),   # 8  passed ball
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2, 's'], [3, 3, 'p'], [4, 4]]},               # Ava
            {'on': 2, 'moves': [[3, 2, 'p'], [5, 3, 'p'], [6, 4]]},               # Bea
            {'on': 4, 'moves': [[5, 2, 'p'], [6, 3], [7, 4, 'p']]},               # Cat
            {'on': 6, 'to': 2, 'moves': [[7, 3, 'p'], [8, 4, 'p']]},              # Deb
        ],
        'at_bats': [(0, 0), (1, 2), (3, 4), (5, 6), (7, 8)],
        'summary': (8, 'O:0 H:3/3 R:4/4, RUN LIMIT'),
    },
    'steal_caught': {
        'rows': [
            ('Ava #7', "....",   'BB', {},              False),
            ('Bea #4', "./..'.", '',   {},              False),  # Ava steals 2nd
            ('',       '',       'BB', {},              False),
            ('Cat #6', ".'",     '',   {3: circ('CS')}, False),  # Ava caught stealing 3rd
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2, 's'], [3, 3, 's', 'out']]},
            {'on': 2, 'moves': [], 'through': 3},
        ],
        'at_bats': [(0, 0), (1, 2), (3, 3)],
    },
    'leaving_early': {
        'rows': [
            ('Ava #7', ".x",    'x2', {},              False),
            ('Bea #4', "./...", '',   {2: circ('LE')}, False),  # Ava out for leaving early; no pitch
            ('',       '',      'BB', {},              False),
        ],
        'runners': [
            {'on': 0, 'to': 2, 'moves': [[1, 2, '', 'out']]},
            {'on': 2, 'moves': []},
        ],
        'at_bats': [(0, 0), (1, 2)],
    },
    'sac_fly': {
        'rows': [
            ('Ava #7', "../x", 'x3',       {},        False),
            ('Bea #4', "../x", circ('F8'), {4: 'R1'}, False),
        ],
        'runners': [
            {'on': 0, 'to': 3, 'moves': [[1, 4, 'sf']]},
        ],
        'at_bats': [(0, 0), (1, 1)],
    },
    'double_play': {
        'rows': [
            ('Ava #7', "....", 'BB', {},                                 False),
            ('Dee #9', ".'x",  '',   {1: circ('6-3'), 2: circ('1-6')}, False),
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2, '', 'out']]},
        ],
        'at_bats': [(0, 0), (1, 1)],
    },
    'fielders_choice': {
        'rows': [
            ('Ava #7', "....", 'BB', {},               False),
            ('Bea #4', "/x",   'FC', {2: circ('6-4')}, False),
        ],
        'runners': [
            {'on': 0, 'moves': [[1, 2, '', 'out']]},
            {'on': 1, 'moves': []},
        ],
        'at_bats': [(0, 0), (1, 1)],
    },
}


def crop_css(n_rows):
    """Show only the first zone's header and first n_rows rows."""
    return f'''
  body {{ width: {WIDTH}px; padding: 2px 2px 26px 2px; background: #fff; }}
  .topline, .zone + .zone, .page-break, .page-break ~ .page {{ display: none; }}
  .zone tbody tr:nth-child(n+{n_rows + 1}) {{ display: none; }}
  td.col-home .mk {{ padding-left: 34%; }}
'''


MEASURE_JS = '''
document.body.setAttribute('data-h',
  Math.ceil(document.querySelector('.zone tbody').getBoundingClientRect().bottom + (ZONES[0].summary ? 30 : 6)));
'''


def build_page(fig):
    html, _ = g.build_html('letter', 'landscape', 0.4, g.TRACKS_ROW_PX, 'tracks')
    html = fill_zone(html, 0, fig['rows'])
    zone = {k: fig[k] for k in ('runners', 'at_bats', 'summary') if k in fig}
    script = (f'<script>\nconst INK = "{INK}";\nconst ZONES = {json.dumps([zone])};\n'
              f'{DRAW_JS}{MEASURE_JS}</script>\n')
    css = CSS + crop_css(len(fig['rows']))
    return html.replace('</style>', css + '</style>', 1).replace('</body>', script + '</body>', 1)


def chrome(*args):
    return subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', *args],
                          check=True, capture_output=True, text=True).stdout


def build():
    if not os.path.exists(CHROME):
        raise SystemExit('Chrome not found; it is needed to render the figures.')
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fig in FIGURES.items():
        html_path = os.path.join(OUT_DIR, f'{name}.html')
        png_path = os.path.join(OUT_DIR, f'{name}.png')
        with open(html_path, 'w') as f:
            f.write(build_page(fig))
        dom = chrome(f'--window-size={WIDTH + 4},2000', '--dump-dom', f'file://{html_path}')
        height = int(re.search(r'data-h="(\d+)"', dom).group(1))
        chrome(f'--window-size={WIDTH + 4},{height}', '--force-device-scale-factor=2',
               f'--screenshot={png_path}', f'file://{html_path}')
        os.remove(html_path)
        print(f'Wrote figures/{name}.png')


if __name__ == '__main__':
    build()
