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

## Reducing row count: options within the action-centric layout

The sheet uses one row per runner event (PB, WP, SB) because each event forces a row break so the base columns can snapshot runner positions. In a chaotic inning this produces many rows where the Pitches box holds just a single pitch mark. Three approaches were identified.

### Option 1: Batch consecutive runner actions into one row

**Rule change:** Runner actions (PB, WP, SB, BLK) no longer force a row break on their own. Only batter results (hit, out, BB, K, HBP) end a row. Multiple runner actions accumulate in the Plate column; base columns show the cumulative final positions after all of them.

Before:
```
Bea#4  | .   | PB  |     | -->  |      |     |
       | /   | PB  |     |      | -->  |     |
       | ./x | 1B  | --> |      |      | --> R1
```

After:
```
Bea#4  | ././x | PB PB 1B | --> |      | --> | --> R1
```

**Savings:** In a 3-PB inning, 3 sparse rows collapse to 0.

**Cost:** Intermediate snapshots are lost. You can't tell from the base columns that the runner was at 2B between the two PBs — only that they ended at 3B. The Plate column needs a bit more width for entries like `PB PB` or `SB BB`.

**Precedent in the existing system:** Multi-base hits already skip intermediate bases in the base columns (a triple draws one line directly to 3B). Batching consecutive runner actions extends the same principle.

---

### Option 2: Inline runner event annotations on pitch marks

**Rule change:** Runner actions are encoded as annotations on the pitch mark where they occurred, rather than ending the row. The row only ends on a batter result. Base columns update only at the batter result.

Concept: a superscript or suffix notation on the pitch mark — e.g., `.↑` or `.pb` — signals that a passed ball happened on that pitch without consuming a new row.

**Savings:** Maximum. Runner events cost zero rows; only batter results consume rows.

**Cost:** Base columns no longer snapshot runner state at all during an at-bat — only the final state after the batter result is shown. Runner position mid-at-bat must be reconstructed by reading the pitch string annotations. Also requires agreeing on a notation that is fast to write by hand without ambiguity.

---

### Option 3: Physical row compression

**No logic change.** Reduce the printed row height so more rows fit per page.

**Savings:** Proportional to height reduction, without any change to the scoring rules.

**Cost:** Less writing space per row, which may matter for the Pitches box on long at-bats or for notes in the base columns.

---

### Comparison

| Option | Row savings | Intermediate snapshots | Notation change |
|--------|-------------|----------------------|-----------------|
| 1 — Batch runner actions | High | Lost (final state only) | Plate column wider |
| 2 — Inline annotations | Maximum | Lost entirely | New pitch annotation syntax |
| 3 — Physical compression | Medium | Preserved | None |

Options 1 and 2 are complementary to Option 3. The design question for 1 vs 2 is how much the per-event runner snapshot matters in practice — Option 1 preserves it across batter results; Option 2 abandons it entirely in favour of zero runner-event rows.

---

## One row per batter, multiple at-bats per row

**Concept:** Instead of one row per event, dedicate one row per batter and give each batter N fixed at-bat slots across the row (e.g. 4 columns, one per time through the order). The batter name is written once on the left; subsequent plate appearances reuse the same row.

**Savings:** Eliminates repeated batter-name writing for batters who come up multiple times. A typical 10U game has 10–12 batters cycling 2–3 times — that's 20–30 fewer name entries per team.

**Layout:** Could fit on portrait orientation with the sheet split horizontally — top half Away team, bottom half Home team. Each half would have a batter list on the left and 4 at-bat columns across. Within each at-bat cell, pitches and result are written compactly.

**Open questions:**
- Runner tracking is the hard part — there's no natural place for base-column snapshots mid-at-bat. Either lose runner tracking entirely (result-only) or add a small base diagram per at-bat cell (Reisner-style).
- Run limits and chaos innings: a single at-bat can span many runner events; the fixed cell size may not accommodate a long sequence.
- This trades the action-centric timeline (read top-to-bottom) for a batter-centric view (read across). Good for post-game stats lookup, worse for reconstructing inning sequence.

**Not yet implemented.**

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