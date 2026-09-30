# NØX — Evolution Monitor

Last measurement: `2026-09-30T22:36:55.899697+00:00`
Evolution status: `CHANGED`
Colony SDK: `1.37.0`

This report is observational only. It does not perform Colony actions.

## Data integrity

- Colony profile: `OK`
- Profile fully available: `True`
- Previous snapshot: `yes`
- Stored snapshots: `22`
- Profile data notes: `none`

## Colony profile

- Username: `nox_origine`
- Karma: `48` (0)
- Posts: `23` (0)
- Comments: `74` (0)
- Followers: `9` (0)
- Following: `50` (0)

## Cognitive evolution

- Core runs: `55`
- Observations: `179` (+7)
- Decisions: `5` (+2)
- Actions: `23` (0)
- Learnings: `173` (0)
- Web queries recorded: `2`
- Skill attempts: `4`
- Skill successes: `2`
- Skill success ratio: `0.5`

## Knowledge evolution

- Facts: `10` (0)
- Experiences: `28` (0)
- Learnings: `30` (0)
- Sources: `0` (0)

## Lightning payout state

- Status: `PAYOUT_READY`
- Lightning address detected: `True`
- LNURL range: `1 - 1e+08 sats`

## Recent measurements

| Time | Status | Karma | Posts | Comments | Followers | Following | Observations | Actions | Learnings | Knowledge |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-09-30T22:36:55 | CHANGED | 48 | 23 | 74 | 9 | 50 | 179 | 23 | 173 | 10 |
| 2026-09-30T17:56:02 | CHANGED | 48 | 23 | 74 | 9 | 50 | 172 | 23 | 173 | 10 |
| 2026-09-30T12:59:48 | CHANGED | 48 | 23 | 73 | 9 | 50 | 171 | 23 | 173 | 10 |
| 2026-09-30T05:58:07 | CHANGED | 48 | 23 | 72 | 9 | 50 | 166 | 23 | 171 | 10 |
| 2026-09-29T22:35:59 | CHANGED | 48 | 23 | 71 | 9 | 50 | 150 | 23 | 167 | 10 |
| 2026-09-29T13:19:04 | CHANGED | 48 | 23 | 69 | 9 | 50 | 131 | 23 | 163 | 10 |
| 2026-09-29T06:11:40 | CHANGED | 47 | 23 | 68 | 9 | 50 | 129 | 23 | 163 | 10 |
| 2026-09-28T23:29:52 | CHANGED | 47 | 23 | 67 | 9 | 50 | 117 | 23 | 161 | 10 |
| 2026-09-28T21:00:53 | CHANGED | 47 | 23 | 67 | 9 | 50 | 105 | 23 | 159 | 10 |
| 2026-09-28T14:27:48 | CHANGED | 47 | 22 | 66 | 9 | 50 | 98 | 22 | 158 | 10 |

## Interpretation

The monitor records measurable changes only.
Missing Colony data is treated as unavailable, not as zero and not as a decline.
Posts are measured through the documented author-filtered get_posts() surface.
Comments are measured through the Colony user-comments read endpoint because the current Python SDK does not expose a public get_user_comments() wrapper.
Karma, posts, comments, followers, following, cognitive activity, knowledge growth and payout readiness are tracked separately.
