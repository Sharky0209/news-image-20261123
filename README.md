# The World in One Image — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Sharky0209/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Sharky0209/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page summing up the world's news of
**Monday 23 November 2026** in a single 1024×1024 image:
six verified Monday stories, led by a dominant KOSPI story with a
hand-drawn intraday chart, three secondary stories in a row, and a
bottom strip with the two remaining stories, the day's also-rans,
and the sources line — every item dated to 23 November 2026.

## The day, in brief

- **Markets** — KOSPI dives over 5% intraday as Seoul vows to act.
- **Europe** — Kyiv region mourns as the Dymer rescue goes on.
- **Disaster** — Indonesia adviser says 24 dead in factory fire.
- **Security** — Kim says North Korea seeks security, not supremacy.
- **Diplomacy** — Nepal PM holds talks with Modi in Delhi.
- **Politics** — Burnham to defend "landmark" EU deal.

## How it is built

`build_entry.py` draws the whole page with Pillow and the system
DejaVu fonts — fixed strings and fixed geometry, no network, no
clock, no randomness. `main.py` is the entrypoint: standard library
only (`os`, `shutil`), it copies `entry.png` next to itself to
`/output/entry.png` and fails if the file is over the 1 MiB limit.

```sh
python3 build_entry.py   # writes entry.png (1024x1024)
python3 main.py          # copies entry.png to /output/entry.png
```

## Verification

Deterministic output — two runs write identical bytes:

```sh
python3 build_entry.py && sha256sum entry.png
python3 build_entry.py && sha256sum entry.png   # hashes match
```

## What changed in v7

v6 was six uniform small cards plus a footer — a wall of small text.
v7 keeps the six verified stories word for word and rebuilds the
layout to read at a glance: a dominant KOSPI lead story with a
hand-drawn intraday chart (previous close to the intraday low of
about −5.8%, no invented data points), three secondary cards
(Europe, Disaster, Security), and a bottom strip with the Diplomacy
and Politics stories, the ALSO line, and the sources line.

## Sources

Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera. All items
happened, or were first reported, on 23 November 2026.

## Bounty

[news-image-20261123 on make.fun](https://make.fun/bounty/news-image-20261123)

## License

MIT — see [LICENSE](LICENSE).
