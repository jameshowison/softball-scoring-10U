# Scoring 10U Softball

## Why a Different Scoresheet?

10U softball is chaos. Walks load the bases, passed balls move everyone, overthrows score runs nobody earned. Standard scoresheets—built for tidy innings with outs—fall apart when an inning has twelve batters and four runs before anyone makes contact.

This repo contains a scoresheet adapted for the joys of 10U softball.  Sure, someone is probably poking at their phone with some online play by play tracking system, but paper is fun too.

In the repo is:
- a tutorial explanation of the scoring approach (rest of this README)
- a printable HTML file (portrait and landscape) that can be used (although see bottom for plain notepad paper approach)
- a script (Claude written) for creating the HTML file, could be used for customization

## How to use

This system is **action-centric**. Each row accumulates pitches until an action occurs that changes the game state — a batter action (a hit! an out!), or a runner movement (a steal, wild pitch, runs scored). It's 10U softball, so runners advancing on passed balls and overthrows are a big part of things, not to mention exciting tags at home (dropped 3rd strikes, anyone?)

You read actions downward through the game like a timeline, not around a diamond per batter.  But the columns help us know where runners are (before they steal again).

---

## Your First Inning

Here's a quiet inning. Three outs, no runs. Read it top to bottom:

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ..'''   | (K)    |       |       |       |
Bea#4    | ....    | BB     |-->    |       |       |
Cat#6    | ./x     |        | (4-3) |       |       |
Deb#8    | x       | (F8)   |       |       |       |
=== END INNING 1 — O:3 H:0/0 R:0/0 ===
```

Let's walk through each batter.

**Ava#7** sees five pitches: `.` (ball), `.` (ball), `'` (strike looking), `'` (strike looking), `'` (strike looking). That last pitch is strike three — she's called out. `(K)` in the Plate column records the strikeout. Parentheses always mean an out was recorded.

**Bea#4** sees four balls: `....` with `BB` in Plate. That's a walk. The `|-->` crossing into the 1B column means she arrives at first base. On paper you draw a short horizontal line from the Plate cell into 1B — it crosses the column boundary within the same row.

**Cat#6** sees a ball, a swinging strike, then makes contact: `./x`. The `x` is the pitch where bat hit ball — the result was an out. `(4-3)` in the 1B column tells you the second baseman (4) fielded it and threw to first (3). It's in the 1B column because that's the base where the out was recorded. The Plate column is blank because nothing happened at the plate — the play resolved at a base.

**Deb#8** swings at the first pitch and makes contact: `x` in Pitches. `(F8)` in Plate means a fly ball caught by the center fielder (8). Fly outs resolve at the plate/field — the batter never reaches a base — so they go in the Plate column, just like `(K)`.

Every batter here took one row. That's the simple case. Things get more interesting when runners move.

---

## The 10U Reality: Wild Pitches and Passed Balls

After that quiet inning, here's what 10U actually looks like. The two codes you'll write most often:

| Code | Meaning |
|------|---------|
| WP | Wild pitch — ball got past the catcher |
| PB | Passed ball — catcher should have had it |

Both are **runner action codes**. They end the current row (because runners moved) but the batter is still hitting. The at-bat (and pitch marks) continue on the next row.

Here's Ava on first when the catcher can't hold onto anything:

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ....    | BB     |-->    |       |       |
Bea#4    | .       | PB     |       |-->    |       |
         | /       | PB     |       |       |-->    |
         | ./x     | 1B     |-->    |       |       |-->  R1
```

Walk through it:

- Ava walks, arrives at 1B.
- Bea comes up. Ball, but the catcher misses it — `.` with `PB` in Plate. Ava advances to 2B. Row ends, Bea's at-bat continues.
- Swinging strike, but again the catcher can't handle it — `/` with `PB`. Ava advances to 3B. Row ends, Bea still hitting.
- Bea sees a ball and a strike, then singles — `./x` with `1B` in Plate. Bea to 1B, Ava scores (R1).

Notice Bea's accumulated pitch count across all three rows: `.` then `/` then `./` = 1-0, 1-1, 2-2 before the single. The count carries across rows because the at-bat never ended.

In text examples, `|-->` marks a runner arriving at a base. On paper, when a batter advances to first base, draw a short horizontal line from Plate to 1B. For doubles and triples, draw a horizontal line to the base, skipping intermediate bases just as the runner did. The longer lines are a visual celebration :)  

Once a runner is on base, when they advance the line on paper becomes diagonal. It runs from the base they were on to the base they get to, but it's also downward since other actions have happened, shifting us down rows. For multi-base advances — a runner scoring from 2B, for example — draw a diagonal line directly to the destination column, here Home. These lines can end up long, if the runner stayed on base for a while before advancing.

### When a Runner Doesn't Make It

Ava triples, and Eve comes up to bat. After a ball, we get a ball that is dropped. Ava heads for home, but the catcher recovers and throws to the pitcher covering home:

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | .'/x    | 3B     |       |       |-->    |
Eve#2    | ..      | WP     |       |       |       | (2-1)
         | .'x     | (F9)   |       |       |       |
```

`(2-1)` in the HOME column — the catcher (2) recovered the ball and threw to the pitcher (1) covering home for the tag. Parentheses mean an out was recorded. The notation goes in HOME because that's the base where the play happened. Eve's at-bat (and pitch marks) continue on the next row.

---

## The Sheet Layout

The sheet is portrait orientation with two identical scoring zones side by side.

The columns, left to right:

| Column | What Goes Here |
|--------|----------------|
| Batter | Player name and jersey number (e.g., `Ava#7`). Left blank on continuation rows for the same batter. |
| Pitches | Pitch marks only: `.` `/` `'` `-` `x` `~`. No spaces. |
| Plate | What happened: `(K)`, `BB`, `WP`, `PB`, `1B`, `(F8)`, etc. Think of it as base zero — the plate and the field around it. |
| 1B | Runner tracking at first base. Arrivals shown by `\|-->`. Outs marked with `(fielding)`. |
| 2B | Runner tracking at second base. |
| 3B | Runner tracking at third base. |
| HOME | Runners scoring. Run tally: R1, R2, etc. Inning summary goes here on the last row. |

The columns tell a spatial story: Plate → 1B → 2B → 3B → HOME. Every out goes where it happened.

---

## Pitch Codes: The Building Blocks

There are five pitch marks. They accumulate left to right in the Pitches cell:

| Symbol | Meaning | Visual Position |
|--------|---------|-----------------|
| `.` | Ball | sits low |
| `/` | Strike swinging | sits high, stop short by hand |
| `'` | Strike looking | sits high |
| `-` | Foul | written as a dash, visually distinct from ball (dot) and strike (slash/tick) |
| `x` | Contact (bat hit ball) | sits low/mid |

The vertical position is intentional: when writing by hand, keep balls low and strikes high. At a glance you can read the shape of a count before counting individual symbols.

A full count with two fouls looks like: `../'--`

Three balls: `...`

A first-pitch swinging strike then two balls: `/..`

These marks never cause a new row on their own. They just accumulate until something happens — and the result goes in the Plate column.

---

## How At-Bats End: Batter Results

These go in the Plate column and end the at-bat. After one of these, the next row starts a new batter.

**Strikeouts:** The third strike is the last pitch mark in the Pitches column. `(K)` goes in Plate. Whether it was looking or swinging, you can tell by looking at the last pitch:

- Looking: Pitches `'''` Plate `(K)` — the `'` tells you it was called
- Swinging: Pitches `../` Plate `(K)` — the `/` tells you she swung

Full at-bat example: ball, ball, strike looking, foul, strike looking for the K → Pitches `..'-'` Plate `(K)`

**Walks and hit-by-pitch:**

| Plate | Meaning |
|-------|---------|
| BB | Walk (four balls). Batter goes to 1B. |
| HBP | Hit by pitch. Batter goes to 1B. |

**Contact:** When `x` appears in Pitches, the Plate column shows the result:

| Plate | Meaning |
|-------|---------|
| 1B | Single |
| 2B | Double |
| 3B | Triple |
| HR | Home run |
| (F7) | Fly out to left field |
| (F8) | Fly out to center field |
| (F9) | Fly out to right field |
| (L3) | Line drive caught by first baseman |
| *(blank)* | Groundout — fielding notation goes in the base column where the out was recorded |

So "ball, then grounded to short" is: Pitches `.x` Plate *(blank)* 1B `(6-3)`.

A double on the first pitch: Pitches `x` Plate `2B`.

A fly out to left on a 1-1 count: Pitches `.'x` Plate `(F7)`.

**Dropped third strike:** The third strike is a pitch mark (`/` or `'`). `K d3` goes in Plate (it's a K for the pitcher but not an out, very strange, classic 10U.) If someone tags the runner before they leave the plate, circle the (d3).

| Situation | Pitches | Plate | 1B |
|-----------|---------|-------|----|
| Out at the plate | `'''` | `K (d3)` |   |
| Batter reaches 1B | `//'` | `K d3` | `\|-->` |
| Catcher throws out at 1B | `'''` | `K d3` | `(2-3)` |

`K (d3)` gets parentheses only when the out happens at the plate. `(2-3)` means catcher threw to first baseman for the out.

---

## Tracking Runners: The Arrow System

When a runner advances to a base, the arrival is shown by `|-->` crossing the column boundary in text. On paper, you draw a line from the runner's current position into the next base column — the line physically crosses the cell boundary.

- **Horizontal** — same-row arrival (BB, HBP, hit): the line crosses the column boundary within the row. On a home run, the batter draws a long horizontal line all the way from Plate to HOME; runners already on base draw diagonal lines that merge into it like tributaries joining a river:

```
         Pitches   Plate    1B     2B     3B       HOME
                     \
                      \    \
          -------------+----+---------->  R7,R8,R9
```
- **Diagonal (down-right)** — cross-row advancement (WP, PB, SB, etc.): the line crosses both the row boundary and the column boundary.
- The line terminates at HOME with a run label: R1, R2, R3, R4 (sequential within the inning).
- If the runner is out, `( )` with the fielding notation appears in the base column where the out happened, and the line stops there.

---

## Continuation Rows: When the Ball Stays Live

The `~` in the Pitches column means the ball is still live from the previous play — no new pitch was thrown. The ball is rolling around out there.

This almost always means an overthrow error. `~` rows are **indented** in the Pitches column to show they belong to the play above. Error codes (E1, E4, etc.) appear in the Plate column.

### The Chaos Inning

Four walks load the bases, then contact turns into a multi-run avalanche:

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ....    | BB     |-->    |       |       |
Bea#4    | ....    | BB     |-->    |-->    |       |
Cat#6    | ....    | BB     |-->    |-->    |-->    |
Deb#8    | ../x    | 1B     |-->    |-->    |-->    |-->  R1
         |   ~     |        |       |-->    |-->    |-->  R2
         |   ~     | E4     |       |       |-->    |-->  R3
         |   ~     | E1     |       |       |       |-->  R4
=== END INNING — O:0 H:1/1 R:4/4, RUN LIMIT ===
```

Deb singles — Ava scores, everyone advances. But the throw goes wild:

- `~` — ball still live, Deb advances to 2B, another runner scores
- `~ E4` — second baseman's overthrow toward third, another run scores
- `~ E1` — pitcher's overthrow at home, Deb scores

One swing of the bat, four runs, the agony of 10U! The `~` rows capture all of it without inventing phantom pitches.

---

## Mid-At-Bat Action: All Runner Action Codes

WP and PB are the most common, but there are other codes that go in Plate and end a row without ending the at-bat:

| Plate | Meaning |
|-------|---------|
| WP | Wild pitch — ball got past the catcher |
| PB | Passed ball — catcher should have had it |
| BLK | Balk — all runners advance one base |
| SB | Stolen base - (CS) goes at base if out|
| LE | Runner leaving early — record `(LE)` in the runner's base column too |

**CI** (catcher interference) is technically a batter action — it ends the at-bat and awards the batter first base. It's rare enough that you may never need it.

### A Medium Inning

Here's an inning with multiple runner actions — 4 runs, hit the run limit:

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ./x     | 1B     |-->    |       |       |
Bea#4    | ../'    | SB     |       |-->    |       |
         | ..      | BB     |-->    |       |       |
Cat#6    | .-      | PB     |       |-->    |-->    |
         | /x      | 1B     |-->    |       |       |-->  R1
Deb#8    | .       | PB     |       |-->    |-->    |
         | /x      | 2B     |       |-->    |       |-->  R2
Eve#2    | .       | PB     |       |       |-->    |-->  R3
         | .       | PB     |       |       |       |-->  R4
=== END INNING 2 — O:0 H:3/3 R:4/4, RUN LIMIT ===
```

Reading this pitch by pitch:

- **Ava#7** gets a single on the third pitch. One row, done.
- **Bea#4** is at bat. Two balls, a strike looking, then Ava steals — `../'` with `SB` in Plate. Ava moves to 2B. New row: two more balls, walk. Bea to 1B.
- **Cat#6** sees a ball and a foul, then a passed ball — `.-` with `PB`. Both runners advance (Bea to 2B, Ava to 3B). Next pitch, Cat singles. Cat to 1B, Ava scores (R1).
- **Deb#8**: ball, but the catcher misses it — `.` with `PB`. Cat to 2B, Bea to 3B. Next pitch, Deb doubles. Bea scores (R2). Deb to 2B.
- **Eve#2**: ball, passed ball — `.` with `PB`. Deb to 3B, Cat scores (R3). Then another passed ball — `.` in Pitches, `PB` in Plate. Deb scores (R4). Run limit hit.

Every row ends with something happening. No wasted rows.

You can create a pitch count for a pitcher by reading down the pitches column.

---

## Inning Boundaries and Summaries

When an inning ends, write a summary in the HOME column of the last row, then draw a double horizontal line across all columns.

**Summary format:** `O:2 H:3/5 R:1/4`

- O: outs this inning
- H: hits this inning / running game total
- R: runs this inning / running game total

**Boundary line format:**

```
=== P↓Tegan#7 --- END INNING 3 — O:2 H:1/6 R:4/8, RUN LIMIT ===
```

The left side shows the incoming pitcher for the next inning (as `P↓Name#N`). Leave it blank if the pitcher isn't changing or isn't known yet. The right side shows the inning number, outs, and runs.

---

## The Out Marker: Parentheses

Outs are marked by parentheses around the play — this mirrors the traditional convention of circling a play in a scorebook. They appear wherever the out was recorded:

| Location | Example | Meaning |
|----------|---------|---------|
| Plate | `(K)` | Strikeout |
| Plate | `K(d3)` | Dropped third strike, out at the plate |
| Plate | `(F7)` | Fly out to left field |
| Plate | `(F8)` | Fly out to center field |
| Plate | `(L3)` | Line drive caught by first baseman |
| 1B | `(4-3)` | Groundout, 2B to 1B |
| 1B | `(2-3)` | Runner thrown out at 1B (e.g., dropped 3rd strike) |
| any base | `(CS)` | Caught stealing |
| HOME | `(2-1)` | Runner thrown out at home |

---

## Fielder Position Numbers

```
    7  8  9           LF   CF   RF
  5  6  4  3         3B  SS  2B  1B
       1                    P
       2                    C
```

The numbering follows baseball convention. Note that SS is 6 (to the left of 2B who is 4) — this can feel counterintuitive at first. Apparently historically SS was once a sort of out fielder that came closer over time.

Common fielding notations:

| Code | Meaning |
|------|---------|
| (4-3) | Fielded by 2B, thrown to 1B |
| (6-3) | Fielded by SS, thrown to 1B |
| (F8) | Fly out to center field |
| (2-3) | Catcher threw to 1B |
| (2-1) | Catcher threw to pitcher at home |
| E4 | Error by 2B (no out — no parentheses) |
| E1 | Error by pitcher (no out) |

Errors never get parentheses. They appear in the Plate column on `~` continuation rows or in base columns to explain how a runner advanced.

---

## Advanced Plays

### Stolen Base

A steal happens on a pitch — the steal and the pitch are simultaneous. `SB` in Plate terminates the row (it's a runner action), and the at-bat continues.

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ....    | BB     |-->    |       |       |
Bea#4    | ../'    | SB     |       |-->    |       |
         | ..      | BB     |-->    |       |       |
```

**Caught stealing** uses the same row — `(CS)` in the destination base instead of an arrow:

```
Bea#4    | ../'    | SB     |       | (CS)  |       |
```

### Runner Leaving Early

In 10U, runners cannot leave the base until the ball crosses the plate. If an umpire calls a runner for leaving early, `LE` goes in the Plate column and `(LE)` goes in the base column where the runner was called. The runner is returned to their base, and the pitch is nullified — the at-bat resets for that pitch.

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Bea#4    | ./      | LE     |       | (LE)  |       |
         | # Ava#7 called for leaving early at 2B, returned
         | ...     | BB     |-->    |       |       |
```

Always add a `#` note explaining who left early and from which base, since LE doesn't capture those details on its own.

### Sacrifice Fly

The batter is out, but a runner tags up and scores. The batter gets the fielding out in Plate with no arrow. The scoring runner advances on a `~` row with `SF` in Plate.

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ../x    | 3B     |       |       |-->    |
Cat#6    | ../x    | (F8)   |       |       |       |
         |   ~     | SF     |       |       |       |-->  R1
```

Ava triples to 3B. Cat flies out to center — `(F8)` in Plate. On the `~` row, Ava tags and scores.

### Double Play

Use traditional fielding sequence notation starting in the 1B cell. Parentheses go around each fielder who recorded an out.

```
Dundon   | .'x     |        | 1-(6)-(3)     |       |
```

Pitcher fields it (1), throws to SS for the out at 2B (6), relay to 1B for the second out (3). The notation may spill across columns — that's fine. It reads left to right naturally.

### Fielder's Choice

Batter reaches safely while a different runner is retired. Both results on the same row:

```
Batter   | Pitches | Plate  | 1B    | 2B    | 3B    | HOME
---------+---------+--------+-------+-------+-------+------
Ava#7    | ....    | BB     |-->    |       |       |
Bea#4    | /x      |        |-->    | (6-4) |       |
```

Bea reaches 1B safely. Ava is out at 2B — SS to second baseman: `(6-4)`. Plate is blank — no plate event, the play resolved at the bases.

---

## Pitcher Tracking

Write the starting pitcher in the first row of the Batter column.

**At inning boundaries:** Write the incoming pitcher on the left side of the boundary line as `P↓Name#N`.

**Mid-inning changes:** Use a `PC` row at the point of change:

```
PC: Mia#3 |         |        |       |       |       |
```

If the pitcher doesn't change at an inning boundary, leave the pitcher field blank.

### Scorer Notes

Use `#` to add a short comment on its own line below any row:

```
         | # Ava#7 injured on play, replaced by Fay#10
```

---

## Batter Blocks

A batter block is all the rows belonging to one plate appearance. The rules:

1. The batter's name appears only on the **first row** of their block.
2. Subsequent rows within the same at-bat leave the Batter column blank.
3. The block ends on exactly one **batter result** in Plate (BB, HBP, hit type, (K), K d3, fielding out), plus any `~` continuation rows that follow.
4. **Runner actions** (WP, PB, SB, etc.) appear mid-block and do **not** end it.

---

## Reference

### Complete Symbol Table

| Symbol | Type | Meaning | Ends Row? | Ends At-Bat? |
|--------|------|---------|-----------|--------------|
| `.` | Pitch | Ball | No | No |
| `/` | Pitch | Strike swinging | No | No |
| `'` | Pitch | Strike looking | No | No |
| `-` | Pitch | Foul | No | No |
| `x` | Pitch | Contact (bat hit ball) | No | No |
| `~` | Pitch | Continuation — ball still live, no new pitch | No | No |
| WP | Plate | Wild pitch | Yes | No |
| PB | Plate | Passed ball | Yes | No |
| BLK | Plate | Balk — all runners advance one base | Yes | No |
| SB | Plate | Stolen base | Yes | No |
| CS | Plate | Caught stealing — `(CS)` in destination column | Yes | No |
| LE | Plate | Runner leaving early — `(LE)` in runner's base column, nullifies pitch | Yes | No |
| CI | Plate | Catcher interference — batter to 1B | Yes | Yes |
| (K) | Plate | Strikeout — last pitch was `/` (swinging) or `'` (looking) | Yes | Yes |
| K d3 | Plate | Dropped third strike, batter safe | Yes | Yes |
| K(d3) | Plate | Dropped third strike, batter out at plate | Yes | Yes |
| BB | Plate | Walk | Yes | Yes |
| HBP | Plate | Hit by pitch | Yes | Yes |
| 1B | Plate | Single (Pitches has `x`) | Yes | Yes |
| 2B | Plate | Double (Pitches has `x`) | Yes | Yes |
| 3B | Plate | Triple (Pitches has `x`) | Yes | Yes |
| HR | Plate | Home run (Pitches has `x`) | Yes | Yes |
| (F#) | Plate | Fly out to fielder # | Yes | Yes |
| (L#) | Plate | Line drive caught by fielder # | Yes | Yes |
| E# | Plate | Error by fielder at position # (no out, no parens) | — | — |
| SF | Plate | Sacrifice fly (on `~` row) | — | — |
| ( ) | Marker | Out recorded here | — | — |
| \|-->  | Marker | Runner arrives at this base (on paper: diagonal line crossing cell boundary) | — | — |
| R1–R4 | Marker | Run scored, sequential within inning | — | — |
| # | Note | Scorer comment on its own line | — | — |
| PC | Administrative | Pitcher change | — | — |

### Fielder Position Numbers

```
7    8    9        LF   CF   RF
  5  6  4  3         3B  SS  2B  1B
       1                  P
       2                  C
```

| # | Position | | # | Position |
|---|----------|-|---|----------|
| 1 | Pitcher | | 6 | Shortstop |
| 2 | Catcher | | 7 | Left Field |
| 3 | First Base | | 8 | Center Field |
| 4 | Second Base | | 9 | Right Field |
| 5 | Third Base | | | |

### Fielding Notation Quick Reference

Plate/field outs (batter never reached a base) go in the Plate column. Base outs go in the base column where the out was recorded.

| Code | Meaning | Location |
|------|---------|----------|
| (F7) | Fly out to LF | Plate |
| (F8) | Fly out to CF | Plate |
| (F9) | Fly out to RF | Plate |
| (L3) | Line drive caught by 1B | Plate |
| (4-3) | Groundout: 2B to 1B | 1B |
| (6-3) | Groundout: SS to 1B | 1B |
| (5-3) | Groundout: 3B to 1B | 1B |
| (1-3) | Groundout: Pitcher to 1B | 1B |
| (3) | Unassisted out at 1B | 1B |
| (2-3) | Catcher to 1B (e.g., dropped 3rd strike) | 1B |
| (2-1) | Catcher to Pitcher at home | HOME |
| (CS) | Caught stealing | destination base |
| (LE) | Runner leaving early | runner's base |
| 1-(6)-(3) | Double play: P to SS to 1B | 1B (may spill) |
| E# | Error by position # — no out, no parentheses | Plate or base column |

### Inning Summary Format

Written in the HOME column of the last row before the boundary line:

```
O:2  H:3/5  R:1/4
```

- **O:** outs this inning
- **H:** hits this inning / running game total
- **R:** runs this inning / running game total

### Inning Boundary Format

```
=== P↓Name#N --- END INNING # — O:# H:#/# R:#/#  ===
=== P↓Name#N --- END INNING # — O:# H:#/# R:#/#, RUN LIMIT ===
```

### Sheet Dimensions

- Portrait orientation
- Two identical scoring zones side by side
- Pitches column: ~7 characters wide
- Long games spill to a second sheet

---

## Scoring Without a Pre-Printed Sheet

Any lined notebook works. The horizontal lines become rows naturally. For columns, tear out a sheet and slide it behind the current page as a backer, rotated 90° so its lines run vertically through the page — they'll show through as column guides.

Approximate column widths in notebook lines (turned 90°):

| Batter | Pitches | Plate | 1B | 2B | 3B | HOME |
|--------|---------|-------|----|----|----|------|
| 2–3    | 2       | 2     | 1  | 1  | 1  | 2    |

You can leave the sheet behind, or if you have a ruler, you can draw light pencil lines at the column boundaries before the game starts. You should still be able to fit both teams side by side on larger note book, but otherwise one team per page is fine — use facing pages for the two teams.

If the paper is too thick for the lines to show through, you can still use them to create the layout by using the lines on the edge of the torn out page. Mark columns at top, middle, and bottom. With thick paper you might be able to use the edge of the torn out sheet to make a light column.

With smaller cells for bases, you might need to write fielding outs at bases `3-(4)` across multiple columns.

---

## Design Tradeoffs

### Why this layout works for 10U

- Handles high-chaos innings naturally — WP, PB, stolen bases, run limits all have clean representations
- Pitch sequence is fully visible for every at-bat, cleanly separated from the result
- Continuous flow handles batting order changes, pinch hitters, and free substitution without special machinery

### Where traditional scorebooks win

At higher levels where batting orders are stable, outs are frequent, and coaches want per-player stat lines after the game, the traditional diamond-per-batter layout is more practical. This layout is optimized for 10U conditions: continuous batting orders, free substitution, run limits, and base-path chaos.

### Known limitation

It's hard to tally per-batter results across a game. A traditional sheet lets you read horizontally to see "3 for 4, 1 BB, 2 RBI." Here you scan vertically for each name appearance. For 10U this is usually acceptable — game-level stats matter less than getting through the inning accurately.
