# The World in One Image — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Sharky0209/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Sharky0209/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A dense newspaper front page summing up the world's news of
**Monday 23 November 2026** in a single 1024×1024 image:
six main stories, a data band, a hand-drawn KOSPI intraday chart,
a by-the-numbers panel, seven more Monday-verified headlines,
and the day's also-rans — every item dated to 23 November 2026.

## The day, in brief

- **Markets** — KOSPI dives over 5% intraday as Seoul vows to act.
- **Europe** — Kyiv region mourns as the Dymer rescue goes on.
- **Disaster** — Indonesia adviser says 24 dead in factory fire.
- **Security** — Kim says North Korea seeks security, not supremacy.
- **Diplomacy** — Nepal PM holds talks with Modi in Delhi.
- **Politics** — Burnham to defend "landmark" EU deal.

## How it is built

`main.py` is the entrypoint: it calls `build_entry.py`, which draws the
whole page with a hand-rolled 5×7 bitmap font and a pure-Python PNG
encoder — standard library only, no network, no Pillow, no external
images. The program runs twice and writes byte-identical output.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## Verification

Deterministic output — two runs write identical bytes:

```sh
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum out1/entry.png out2/entry.png   # hashes match
```

Standard-library-only check (no third-party imports):

```sh
cd /tmp && MAKEFUN_OUTPUT_DIR=/tmp/v7std python3 -S /path/to/repo/main.py
```

## What changed in v7

v6 was six cards and three also-rans with too much white space. v7 keeps
the six verified stories word for word and adds: a hero treatment for the
KOSPI story with a hand-drawn intraday chart, a five-cell data band, a
by-the-numbers bar panel, and seven extra Monday-verified headlines
(Germany, Spain, Denmark, Iran, energy, Britain, Armenia).

## Sources

Yonhap, Reuters, CNA, BBC, Kyiv Independent, Al Jazeera — plus Reuters,
AFP, Bloomberg Tax and WION for the extra headlines. All items happened,
or were first reported, on 23 November 2026.

## Bounty

[news-image-20261123 on make.fun](https://make.fun/bounty/news-image-20261123)

## License

MIT — see [LICENSE](LICENSE).
