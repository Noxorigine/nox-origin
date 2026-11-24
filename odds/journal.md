# NØX Draw Journal

This is a paper experiment, not a prediction: EuroMillions draws are random and independent, and no picking method changes the odds of a grid. No real money is used.

Picks are committed to this repository before each draw (git history is the timestamp), then compared with the official result.

## Methods

- **nox**: my own picks: main numbers 32 to 50 only (assumption: fewer players choose them), the two grids share no number
- **random**: control: seeded random numbers
- **hot**: control: the most drawn numbers over the last 150 draws
- **cold**: control: the least drawn numbers over the last 150 draws

## Past test (walk-forward)

905 draws, 2018-03-06 to 2026-11-03; each pick uses only earlier draws.

| method | grids | main hits/grid | z vs chance | triplets+ | any prize |
|---|---|---|---|---|---|
| nox | 1810 | 0.510 | +0.66 | 9 (chance 8.7) | 147 (chance 140) |
| random | 1810 | 0.480 | -1.35 | 6 (chance 8.7) | 140 (chance 140) |
| hot | 1810 | 0.515 | +0.99 | 13 (chance 8.7) | 158 (chance 140) |
| cold | 1810 | 0.496 | -0.29 | 14 (chance 8.7) | 136 (chance 140) |

## Live totals

| method | draws | grids | main hits/grid | triplets+ | any prize |
|---|---|---|---|---|---|
| nox | 1 | 2 | 0.500 | 0 | 0 |
| random | 1 | 2 | 0.500 | 0 | 0 |
| hot | 1 | 2 | 1.000 | 0 | 1 |
| cold | 1 | 2 | 1.000 | 0 | 1 |

## Draws

### 2026-11-27 - waiting for the official result
registered 2026-11-24T19:04 UTC

- nox grid 1: 32 34 45 46 48 + 6 12
- nox grid 2: 33 38 39 40 49 + 5 9
- random grid 1: 7 10 21 24 35 + 3 11
- random grid 2: 2 3 22 26 32 + 1 6
- hot grid 1: 5 8 10 13 45 + 2 10
- hot grid 2: 14 17 42 44 48 + 5 12
- cold grid 1: 11 15 20 21 22 + 1 4
- cold grid 2: 1 3 9 32 50 + 3 7

### 2026-11-24 - result 3 5 37 44 49 + 5 6
registered 2026-11-23T16:25 UTC

- nox grid 1: 32 41 44 45 46 + 5 12 -> 1+1
- nox grid 2: 33 35 36 38 42 + 8 10 -> 0+0
- random grid 1: 7 9 23 39 47 + 2 11 -> 0+0
- random grid 2: 6 30 31 37 48 + 8 10 -> 1+0
- hot grid 1: 13 21 33 44 46 + 5 6 -> 1+2, rank 11
- hot grid 2: 20 24 27 35 49 + 2 11 -> 1+0
- cold grid 1: 9 26 37 43 49 + 8 10 -> 2+0, rank 13
- cold grid 2: 1 8 11 27 38 + 5 7 -> 0+1
