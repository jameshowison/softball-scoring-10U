# Ongoing questions

## Merge Pitch and Plate column?

**Current:** Separate Plate column holds contact results, strikeouts, and runner-action codes.

**Finding:** Plate column is only load-bearing for contact results and strikeouts. Runner-action codes (WP, PB, SB, etc.) embed cleanly in the pitch string.

**Proposed change:** Remove Plate column. Widen Pitch column to ~1.5× current width (net space gain since Plate is eliminated).

**Encoding in pitch string:**
- Base hits: `x1`, `x2`, `x3`, `xHR`
- Strikeouts: `K` (looking) or `Ks` (swinging) — inferrable from last pitch mark but explicit is cleaner
- Runner actions: `....BB`, `./PB`, `..SB` etc.
- Contact outs: `xF8`, `xL3`, groundouts still resolve in base column as before

**Cell closure options for contact/strikeout results:**
- Fill remainder of pitch box with a line (`..x1——`) to visually separate pitch sequence from result
- Or just leave a small space (`..x1  `) — simpler but less distinct

**Open question:** Whether `xF8` reads comfortably enough in a wider pitch cell, or feels cramped.

## Completed tasks

### Light grey shading on 1B and 3B columns

Added `background-color: #f0f0f0` to the 1B and 3B data cells to visually distinguish them from 2B and HOME. Changes made in `generate_scoresheet.py`:

- Renamed the shared `col-b` CSS class to distinct `col-b1`, `col-b2`, `col-b3` classes so 1B and 3B can be targeted independently.
- Added classes to `td` elements in body rows (they previously had no class, so column-targeted CSS rules had no effect).
- Added CSS rule `td.col-b1, td.col-b3 { background-color: #f0f0f0; }`.
- Regenerated `scoresheet_letter_landscape.html` and `scoresheet_letter_portrait.html`.