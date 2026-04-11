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