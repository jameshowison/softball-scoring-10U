# Ongoing questions

## Why not a diamond-based scoresheet for 10U?

Traditional baseball scoresheets and the Reisner system both use a diamond cell per at-bat: one column per batter position, innings stacked in rows. The batter's result goes in the center of the diamond, and runner paths are traced by darkening the baselines. It's a proven format with decades of familiarity.

The question arose: could this sheet adopt a similar layout? Larger diamonds (to accommodate 10U chaos), with two vertical columns added inside each cell — one for pitches, one for runner events — inspired by the Reisner system's pitch-alignment approach.

### The line count problem

The current action-centric sheet uses one row per runner event (WP, PB, SB), because each event ends the current row so the base columns can capture a runner-position snapshot. In a chaotic inning with three passed balls and a stolen base before a batter result, that burns four rows — each with just one pitch in the pitch box. The diamond idea was explored partly as a fix: if each at-bat is bounded by a fixed cell, overflow rows disappear.

A Reisner-style vertical layout within each cell would add two narrow columns to the diamond:

```
┌──────────┬──────────────┬──────────────────┐
│ Pitches  │ Runner events│                  │
├──────────┼──────────────┤    Diamond       │
│    .     │              │       2B         │
│    .     │ PB: 1→2      │     /    \       │
│    /     │ PB: 2→3      │   3B      1B     │
│    .     │              │     \    /       │
│    x     │              │       H          │
├──────────┴──────────────┤   Result: 1B     │
└─────────────────────────┴──────────────────┘
```

Each pitch occupies exactly one row. The event aligned to that pitch sits beside it. You can see that pitch 2 produced a PB and pitch 3 produced another PB, which the current horizontal system loses when those events are batched.

### Where it breaks down: the diamond can't hold 10U runner paths

Traditional diamonds work because baseball runners typically advance once or twice per at-bat, and at most two or three runners are in motion. Each baseline segment carries one runner's path, and darkening it is unambiguous.

10U softball breaks this assumption. A routine chaotic at-bat — bases loaded, two passed balls, then a single — requires showing:

- Cat (was at 3B): one segment darkened (3B→H)
- Bea (was at 2B): two segments darkened (2B→3B→H)
- Ava (was at 1B): three segments darkened (1B→2B→3B→H)
- Batter (Eve): arrives at 1B

Every single baseline segment now carries two or three runner marks simultaneously. Even with runner numbers written along each segment, the 2B→3B segment reads "Bea, Ava" and the 3B→H segment reads "Cat, Bea." The visual power of the diamond — readable path lines — collapses into a tangle.

Two escape routes were considered:

**Option A: Diamond shows final state only.** Numbers at corners indicate where runners end up; scored runners are circled and removed. Clean, but the story of how runners got there is gone.

```
         [Bea]
        /      \
      ---        [Eve]
        \      /
     R1(Cat) R2(Ava)
```

**Option B: Diamond for batter only, events column carries runner tracking.** Clean diamond, text-based runner events. But now the diamond is decorative space for most of the action — a large fixed-size area mostly reserved for one player's three-base path.

### Why the action-centric layout is the right answer for 10U

The fundamental mismatch is that the diamond encodes runner movement as *spatial paths* — and spatial paths stop being legible when multiple runners make multi-base advances simultaneously. The diamond is optimized for the baseball case where at most one or two runners advance per at-bat, each advancing once.

The action-centric row-per-event layout encodes runner movement as *text in columns*, which scales linearly with complexity. Three runners advancing simultaneously costs three column entries, not three overlapping lines on a small diamond. There is no visual degradation — a bases-loaded passed ball is exactly as readable as a single runner stealing second.

The other key property is the timeline. Reading the action-centric sheet top to bottom reconstructs the inning in chronological order. Diamond sheets require reading across rows by batter and reconstructing the inning mentally. For 10U, where the story of the inning — not the per-batter stat line — is what matters, chronological flow is the right primary axis.

The line count problem (too many sparse rows) is real and worth solving, but the solution is to make runner events less row-hungry within the existing layout, not to abandon the layout for one that can't represent 10U chaos without becoming illegible.

---

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